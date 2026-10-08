"""Zero-training Pretrained MediaPipe Gesture Recognizer module.

Uses Google's official gesture_recognizer.task bundle to perform instant,
zero-training gesture recognition directly on image frames.
"""

import os
import time
from typing import Dict, List, Optional, Any, Tuple
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class MediaPipeGestureRecognizer:
    """Zero-training gesture recognizer using MediaPipe's pretrained task."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        num_hands: int = 2,
        min_hand_detection_confidence: float = 0.5,
        min_hand_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        if model_path is None:
            model_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "models", "gesture_recognizer.task"
            )
        
        self.model_path = os.path.abspath(model_path)
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"MediaPipe gesture recognizer model not found at {self.model_path}."
            )

        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            num_hands=num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def recognize_frame(self, frame_bgr: np.ndarray) -> Dict[str, Any]:
        """Recognize hand gestures in a standard BGR image frame (e.g., from OpenCV/webcam).

        Args:
            frame_bgr: BGR image frame as numpy array of shape (H, W, 3).

        Returns:
            dict containing:
                - label: Highest confidence gesture name, or "None"
                - confidence: Confidence score (float, 0.0 to 1.0)
                - gestures: List of recognized gestures per hand
                - handedness: List of handedness strings ("Left", "Right")
                - timestamp: Epoch timestamp
        """
        if frame_bgr is None or frame_bgr.size == 0:
            return {
                "label": "None",
                "confidence": 0.0,
                "gestures": [],
                "handedness": [],
                "timestamp": time.time(),
            }

        # MediaPipe expects RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        result = self.recognizer.recognize(mp_image)

        recognized_gestures = []
        handedness_list = []
        top_label = "None"
        top_score = 0.0

        if result.gestures:
            for hand_idx, gesture_list in enumerate(result.gestures):
                if gesture_list:
                    top_category = gesture_list[0]
                    cat_name = top_category.category_name
                    score = float(top_category.score)

                    # Determine handedness
                    handedness_str = "Unknown"
                    if result.handedness and hand_idx < len(result.handedness):
                        handedness_str = result.handedness[hand_idx][0].category_name

                    recognized_gestures.append({
                        "hand_index": hand_idx,
                        "handedness": handedness_str,
                        "gesture": cat_name,
                        "score": score,
                    })

                    if score > top_score and cat_name != "None":
                        top_score = score
                        top_label = cat_name

        return {
            "label": top_label,
            "confidence": top_score,
            "gestures": recognized_gestures,
            "hand_landmarks": result.hand_landmarks if hasattr(result, "hand_landmarks") else [],
            "timestamp": time.time(),
        }
