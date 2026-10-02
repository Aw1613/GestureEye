"""Interactive Training Data Collection Utility for SignBridge (Agent 1).

Allows a user to record sign gesture samples from their webcam.
Saves extracted normalized keypoint sequences (30 frames x 126 features)
into data/raw/<label>/sample_<timestamp>.npy.

Usage:
    python scripts/collect_data.py --sign hello --samples 15
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add project root to sys.path so 'app' can be imported anywhere
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np

from app.capture.camera import CameraCapture
from app.keypoints.extractor import HandKeypointExtractor
from app.keypoints.buffer import SequenceBuffer
from app.keypoints.preprocessing import FEATURE_DIM

DEFAULT_SEQ_LEN = 30


def collect_data(
    sign_label: str,
    num_samples: int = 10,
    seq_length: int = DEFAULT_SEQ_LEN,
    camera_index: int = 0,
    output_dir: str = "data/raw",
    countdown: int = 3,
):
    """Collect keypoint sequences for a given sign label."""
    label_dir = os.path.join(output_dir, sign_label)
    os.makedirs(label_dir, exist_ok=True)

    print("=" * 60)
    print(f"🎬 SignBridge Data Collection for sign: '{sign_label}'")
    print(f"📁 Target directory: {label_dir}")
    print(f"🎯 Target samples: {num_samples}")
    print("=" * 60)
    print("Instructions:")
    print("1. Stand/sit in front of your webcam with hands visible.")
    print("2. When prompted, perform the sign during the 30-frame capture window.")
    print("3. Press 'q' at any time to exit.")
    print("=" * 60)

    cam = CameraCapture(device_index=camera_index, width=640, height=480, fps=30)
    extractor = HandKeypointExtractor()
    buffer = SequenceBuffer(sequence_length=seq_length, feature_dim=FEATURE_DIM)

    if not cam.is_opened():
        print(f"❌ Error: Cannot open webcam at index {camera_index}.")
        return

    try:
        sample_count = 0
        while sample_count < num_samples:
            # Countdown before starting capture
            for remaining in range(countdown, 0, -1):
                start_cd = time.time()
                while time.time() - start_cd < 1.0:
                    ret, frame = cam.read()
                    if not ret:
                        continue
                    display = frame.copy()
                    cv2.putText(
                        display,
                        f"Sign: '{sign_label}' (Sample {sample_count + 1}/{num_samples})",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 0),
                        2,
                    )
                    cv2.putText(
                        display,
                        f"Get Ready: {remaining}...",
                        (200, 240),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        3,
                    )
                    cv2.imshow("SignBridge Data Collector", display)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        print("User aborted collection.")
                        return

            # Capture 30 frames
            buffer.reset()
            frame_idx = 0
            while frame_idx < seq_length:
                loop_start = time.time()
                
                ret, frame = cam.read()
                if not ret:
                    continue

                feat_vector, info, annotated = extractor.extract_keypoints(frame, draw=True)
                buffer.append(feat_vector)
                frame_idx += 1

                # Visual feedback
                cv2.putText(
                    annotated,
                    f"RECORDING [{frame_idx}/{seq_length}]",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 0),
                    3,
                )
                cv2.imshow("SignBridge Data Collector", annotated)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("User aborted collection.")
                    return
                    
                # ENFORCE 30 FPS PACING so it captures exactly 1 second of motion
                elapsed = time.time() - loop_start
                if elapsed < (1.0 / 30.0):
                    time.sleep((1.0 / 30.0) - elapsed)

            seq = buffer.get_sequence()
            if seq is not None and seq.shape == (seq_length, FEATURE_DIM):
                timestamp = int(time.time() * 1000)
                file_path = os.path.join(label_dir, f"sample_{timestamp}.npy")
                np.save(file_path, seq)
                sample_count += 1
                print(f"✅ Saved sample {sample_count}/{num_samples}: {file_path}")

            time.sleep(0.5)

        print("\n🎉 Collection finished successfully!")
    finally:
        cam.release()
        extractor.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SignBridge Keypoint Dataset Collector")
    parser.add_argument("--sign", type=str, required=True, help="Name of the sign label")
    parser.add_argument("--samples", type=int, default=10, help="Number of samples to record")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index")
    args = parser.parse_args()

    collect_data(sign_label=args.sign, num_samples=args.samples, camera_index=args.camera)

