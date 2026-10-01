"""Webcam and Video Frame Capture Module for SignBridge (Agent 1).

Responsible for:
- Continuous frame capture from webcam (or video file / test stream)
- Resolution and frame-rate configuration
- Safe resource management and error reporting
"""

import time
import threading
from typing import Optional, Tuple
import cv2
import numpy as np


class CameraCapture:
    """Wrapper around OpenCV VideoCapture for robust webcam streaming."""

    def __init__(
        self,
        device_index: int = 0,
        width: int = 640,
        height: int = 480,
        fps: int = 30,
        mock: bool = False,
    ):
        """Initialize the camera capture instance.

        Args:
            device_index: Camera index (default 0) or path to video file.
            width: Desired frame width in pixels.
            height: Desired frame height in pixels.
            fps: Target frames per second.
            mock: If True, generates synthetic frames for automated testing.
        """
        self.device_index = device_index
        self.width = width
        self.height = height
        self.fps = fps
        self.mock = mock

        self.cap: Optional[cv2.VideoCapture] = None
        self._is_opened: bool = False
        self._latest_frame: Optional[np.ndarray] = None
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._thread_running: bool = False

        if not self.mock:
            self._open_camera()
        else:
            self._is_opened = True

    def _open_camera(self) -> bool:
        """Open the video capture device and start background reader thread."""
        try:
            # On Windows, try CAP_DSHOW first for lowest latency and direct driver access
            if hasattr(cv2, "CAP_DSHOW"):
                self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(self.device_index)

            if not self.cap or not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.device_index)

            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self._is_opened = True

                # Start background thread to continuously grab latest frames
                self._thread_running = True
                self._thread = threading.Thread(target=self._capture_worker, daemon=True)
                self._thread.start()

                # Wait briefly for first frame to arrive
                for _ in range(25):
                    with self._lock:
                        if self._latest_frame is not None:
                            break
                    time.sleep(0.02)

                return True
            else:
                self._is_opened = False
                return False
        except Exception as e:
            print(f"[CameraCapture Error] Could not open camera {self.device_index}: {e}")
            self._is_opened = False
            return False

    def _capture_worker(self) -> None:
        """Background thread worker to keep camera buffer flushed and provide freshest frame."""
        while self._thread_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                if frame.shape[1] != self.width or frame.shape[0] != self.height:
                    frame = cv2.resize(frame, (self.width, self.height))
                with self._lock:
                    self._latest_frame = frame
            else:
                time.sleep(0.005)

    def is_opened(self) -> bool:
        """Return whether the camera capture device is actively opened."""
        if self.mock:
            return self._is_opened
        return self.cap is not None and self.cap.isOpened()

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """Read a single video frame.

        Returns:
            Tuple of (success: bool, frame: np.ndarray or None)
        """
        if not self.is_opened():
            return False, None

        if self.mock:
            # Generate a 640x480 black image with a colored test rectangle
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            cv2.putText(
                frame,
                "SignBridge Mock Camera",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
            )
            time.sleep(1.0 / max(1, self.fps))
            return True, frame

        with self._lock:
            if self._latest_frame is not None:
                return True, self._latest_frame.copy()

        # Fallback if worker thread has not grabbed a frame yet
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                if frame.shape[1] != self.width or frame.shape[0] != self.height:
                    frame = cv2.resize(frame, (self.width, self.height))
                return True, frame

        return False, None

    def start(self) -> bool:
        """Start or verify the camera stream."""
        if not self.is_opened() and not self.mock:
            return self._open_camera()
        return self.is_opened()

    def get_frame(self) -> Optional[np.ndarray]:
        """Convenience method returning the frame directly or None."""
        ret, frame = self.read()
        return frame if ret else None

    def release(self) -> None:
        """Release camera hardware resources."""
        self._thread_running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.5)
            self._thread = None

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        with self._lock:
            self._latest_frame = None

        self._is_opened = False

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.release()
