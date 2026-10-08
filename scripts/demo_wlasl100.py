"""Live Real-Time Demo for Pretrained WLASL-100 Sign Language Recognition.

Recognizes 100 word-level American Sign Language (ASL) signs using:
- MediaPipe Holistic (13 upper body + 21 left hand + 21 right hand = 55 keypoints)
- Pretrained WLASL-100 TGCN (Temporal Graph Convolutional Network)
- Real-time HUD displaying Top-1, Top-5 alternatives, and sentence buffer.

Usage:
    python scripts/demo_wlasl100.py
    python scripts/demo_wlasl100.py --mock
"""

import argparse
import collections
import os
import sys
import time
import cv2
import numpy as np

# Ensure project root is in python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.recognition.wlasl_inference import WLASLInference, MediaPipeHolisticExtractor
from app.sentence.builder import SentenceBuilder


def run_demo(mock: bool = False, buffer_size: int = 50, confidence_threshold: float = 0.55):
    print("=" * 65)
    print("  Pretrained WLASL-100 Sign Language Recognition System")
    print("=" * 65)
    print("Loading MediaPipe Holistic tracker and WLASL-100 TGCN model...")

    inference = WLASLInference(num_frames=buffer_size)
    sentence_builder = SentenceBuilder()

    print(f"Model loaded successfully! Vocabulary size: {inference.num_classes} ASL words.")
    print("Sample vocabulary: book, drink, computer, before, chair, go, clothes, who, candy, cousin, etc.")
    print("=" * 65)

    if mock:
        print("\nRunning in MOCK mode (synthetic sequences)...")
        dummy_seq = np.random.randn(buffer_size, 55, 2).astype(np.float32) * 0.2
        t0 = time.perf_counter()
        result = inference.predict_sequence(dummy_seq)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        print(f"Inference Latency: {latency_ms:.2f} ms")
        print(f"Top-1 Prediction: {result['label']} ({result['confidence'] * 100:.1f}%)")
        print("Top-5 Candidates:")
        for rank, cand in enumerate(result["top_5"], 1):
            print(f"  {rank}. {cand['label']:<15} {cand['confidence'] * 100:.1f}%")
        print("\nMock test finished successfully!")
        return

    extractor = MediaPipeHolisticExtractor()
    buffer = collections.deque(maxlen=buffer_size)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera. Falling back to mock test.")
        extractor.close()
        run_demo(mock=True)
        return

    print("\nOpening camera... Sign with your hands and body in frame.")
    print("Press 'c' to clear sentence, 'q' or ESC to exit.\n")

    current_label = "Waiting for motion..."
    current_conf = 0.0
    top_5 = []
    sentence_words = []
    last_added_word = None
    last_word_time = 0.0

    frame_count = 0
    fps = 0.0
    last_fps_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Mirror image for natural self-view
            frame = cv2.flip(frame, 1)

            # Extract 55 keypoints and draw skeleton
            keypoints, annotated = extractor.extract(frame, draw=True)
            buffer.append(keypoints)

            # FPS calculation
            frame_count += 1
            now = time.time()
            if now - last_fps_time >= 1.0:
                fps = frame_count / (now - last_fps_time)
                frame_count = 0
                last_fps_time = now

            # Predict when buffer is full (every 3 frames for high responsiveness)
            if len(buffer) == buffer_size and frame_count % 3 == 0:
                seq_np = np.array(buffer)
                pred = inference.predict_sequence(seq_np)
                current_label = pred["label"]
                current_conf = pred["confidence"]
                top_5 = pred["top_5"]

                # Word lock & sentence building
                if current_conf >= confidence_threshold:
                    if current_label != last_added_word or (now - last_word_time > 2.5):
                        sentence_builder.add_word(current_label)
                        sentence_words.append(current_label)
                        last_added_word = current_label
                        last_word_time = now

            # Draw HUD Overlays
            h, w = annotated.shape[:2]

            # Top bar
            cv2.rectangle(annotated, (0, 0), (w, 85), (20, 20, 20), -1)

            # Display prediction
            if len(buffer) < buffer_size:
                status_txt = f"Buffering gesture: {len(buffer)}/{buffer_size} frames..."
                cv2.putText(annotated, status_txt, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2)
            else:
                color = (0, 255, 0) if current_conf >= confidence_threshold else (200, 200, 200)
                pred_txt = f"Sign: {current_label.upper()} ({current_conf * 100:.1f}%)"
                cv2.putText(annotated, pred_txt, (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)

            sub_txt = f"FPS: {fps:.1f} | 55 Keypoints Active | Pretrained WLASL-100"
            cv2.putText(annotated, sub_txt, (20, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (160, 160, 160), 1)

            # Bottom bar: Sentence construction
            cv2.rectangle(annotated, (0, h - 60), (w, h), (15, 15, 15), -1)
            full_sentence = sentence_builder.get_sentence()
            if not full_sentence:
                sentence_display = "Sentence: [Perform signs to construct words]"
            else:
                sentence_display = f"Sentence: {full_sentence}"
            cv2.putText(annotated, sentence_display, (20, h - 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Top-5 side panel
            if top_5:
                cv2.rectangle(annotated, (w - 220, 95), (w - 10, 235), (20, 20, 20), -1)
                cv2.putText(annotated, "Top Candidates:", (w - 210, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)
                for idx, c in enumerate(top_5):
                    c_txt = f"{idx+1}. {c['label'][:10]:<10} {c['confidence']*100:.0f}%"
                    cv2.putText(annotated, c_txt, (w - 210, 138 + idx * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1)

            cv2.imshow("WLASL-100 Sign Language Recognition", annotated)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('c'):
                sentence_builder.clear()
                sentence_words.clear()
                last_added_word = None

    finally:
        cap.release()
        extractor.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WLASL-100 Sign Recognition Demo")
    parser.add_argument("--mock", action="store_true", help="Run with mock inputs instead of webcam")
    args = parser.parse_args()
    run_demo(mock=args.mock)
