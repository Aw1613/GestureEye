"""Visual Demo for Member 1: Live Webcam & MediaPipe Hand Tracking.

Run this script to see your webcam open with live hand landmark tracking
and sequence buffer accumulation in real time.

Usage:
    .venv/bin/python scripts/demo_keypoints.py
    Press 'q' on your keyboard to close the window.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
from app.capture.camera import CameraCapture
from app.keypoints.extractor import HandKeypointExtractor
from app.keypoints.buffer import SequenceBuffer
from app.keypoints.preprocessing import FEATURE_DIM


def main():
    print("=" * 60)
    print("🎥 Starting SignBridge Member 1 Live Camera & Keypoint Test")
    print("👉 Show your hands to the webcam.")
    print("👉 Press 'q' in the camera window to quit.")
    print("=" * 60)

    cam = CameraCapture(device_index=0, width=640, height=480, fps=30)
    extractor = HandKeypointExtractor()
    buffer = SequenceBuffer(sequence_length=30, feature_dim=FEATURE_DIM)

    if not cam.is_opened():
        print("❌ Could not open webcam (index 0). Is another app using it?")
        return

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            # Flip frame horizontally for natural mirror feel
            frame = cv2.flip(frame, 1)

            # Extract landmarks and draw skeleton on frame
            feat_vec, info, annotated = extractor.extract_keypoints(frame, draw=True)
            buffer.append(feat_vec)

            # Display status on the screen
            left_status = "DETECTED" if info["left_detected"] else "NOT DETECTED"
            right_status = "DETECTED" if info["right_detected"] else "NOT DETECTED"
            buffer_status = f"{len(buffer)}/30 frames"
            if buffer.is_ready():
                buffer_status += " [READY FOR MODEL]"

            # Draw status HUD
            cv2.rectangle(annotated, (10, 10), (380, 110), (0, 0, 0), -1)
            cv2.putText(
                annotated,
                f"Left Hand : {left_status}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0) if info["left_detected"] else (0, 0, 255),
                2,
            )
            cv2.putText(
                annotated,
                f"Right Hand: {right_status}",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0) if info["right_detected"] else (0, 0, 255),
                2,
            )
            cv2.putText(
                annotated,
                f"Buffer    : {buffer_status}",
                (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
            )
            cv2.putText(
                annotated,
                "Press 'q' to quit",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (200, 200, 200),
                1,
            )

            cv2.imshow("SignBridge - Member 1 Hand Tracking Test", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        extractor.close()
        cv2.destroyAllWindows()
        print("Camera released. Demo closed cleanly.")


if __name__ == "__main__":
    main()
