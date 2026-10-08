"""Live Demo Script for Pretrained MediaPipe Zero-Training Gesture Recognizer.

Recognizes hand gestures (Thumb_Up, Victory, Open_Palm, Closed_Fist, Pointing_Up, etc.)
in real-time from the webcam without requiring any training dataset.

Usage:
    python scripts/demo_pretrained_mediapipe.py
    python scripts/demo_pretrained_mediapipe.py --mock
"""

import argparse
import os
import sys
import time
import cv2
import numpy as np

# Ensure project root is in python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.recognition.mediapipe_recognizer import MediaPipeGestureRecognizer


def run_demo(mock: bool = False, max_frames: int = 150):
    print("=" * 60)
    print(" MediaPipe Pretrained Gesture Recognizer (Zero-Training)")
    print("=" * 60)
    print("Loading gesture_recognizer.task...")

    recognizer = MediaPipeGestureRecognizer()
    print("Recognizer loaded successfully!")
    print("\nSupported Out-of-the-Box Gestures:")
    print(" - Thumb_Up, Thumb_Down")
    print(" - Victory (Peace / V-sign)")
    print(" - Open_Palm (Wave / Stop)")
    print(" - Closed_Fist")
    print(" - Pointing_Up")
    print(" - ILoveYou")
    print("=" * 60)

    if mock:
        print("\nRunning in MOCK mode (synthetic frames)...")
        for i in range(1, 11):
            dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            t0 = time.perf_counter()
            result = recognizer.recognize_frame(dummy_frame)
            latency_ms = (time.perf_counter() - t0) * 1000.0
            print(f"Frame {i:02d} | Latency: {latency_ms:.1f}ms | Label: {result['label']} | Confidence: {result['confidence']:.2f}")
            time.sleep(0.05)
        print("\nMock run completed successfully.")
        return

    print("\nOpening camera... Press 'q' or ESC in the preview window to exit.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera. Falling back to mock test.")
        run_demo(mock=True)
        return

    frame_count = 0
    fps = 0.0
    last_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame from webcam.")
                break

            # Mirror for natural user interaction
            frame = cv2.flip(frame, 1)

            t0 = time.perf_counter()
            result = recognizer.recognize_frame(frame)
            latency_ms = (time.perf_counter() - t0) * 1000.0

            # Calculate FPS
            frame_count += 1
            now = time.time()
            if now - last_time >= 1.0:
                fps = frame_count / (now - last_time)
                frame_count = 0
                last_time = now

            # Overlay info
            top_label = result["label"]
            confidence = result["confidence"]

            # Header panel
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (w, 80), (25, 25, 25), -1)

            color = (0, 255, 0) if top_label != "None" else (180, 180, 180)
            text = f"Gesture: {top_label} ({confidence * 100:.1f}%)" if top_label != "None" else "Gesture: None"
            cv2.putText(frame, text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 2, cv2.LINE_AA)

            stats = f"Latency: {latency_ms:.1f}ms | FPS: {fps:.1f} | MediaPipe Zero-Shot"
            cv2.putText(frame, stats, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

            # Details per hand
            y_offset = 110
            for g in result["gestures"]:
                hand_text = f"[{g['handedness']} Hand] {g['gesture']} ({g['score'] * 100:.1f}%)"
                cv2.putText(frame, hand_text, (20, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
                y_offset += 30

            cv2.imshow("MediaPipe Zero-Training Gesture Recognizer", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediaPipe Gesture Recognizer Demo")
    parser.add_argument("--mock", action="store_true", help="Run with mock frames instead of webcam")
    args = parser.parse_args()
    run_demo(mock=args.mock)
