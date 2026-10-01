"""
Demo Script for Agent 3 (Sentence Logic & Text-to-Speech)
Demonstrates the full pipeline from Contract C predictions
to stable words (Contract D), smoothed sentences (Contract E), and speech (Contract F).
"""

import sys
import os
import time
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.sentence.filter import PredictionFilter
from app.sentence.builder import SentenceBuilder
from app.tts.speech import TextToSpeech

def run_demo():
    print("=" * 60)
    print("  SIGN-BRIDGE: AGENT 3 (LOGIC + SPEECH) DEMO")
    print("=" * 60)

    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)
    builder = SentenceBuilder()
    tts = TextToSpeech(enabled=True)

    print("\n[Init] PredictionFilter, SentenceBuilder, and TextToSpeech initialized.")

    # Simulated incoming stream of predictions from Agent 2
    # Signs: "hello" (stable), pause, "water" (stable), "please" (stable)
    sign_phases = [
        ("hello", 7, 0.88),       # 7 frames of "hello" (should accept at frame 5, suppress 6-7)
        ("unknown", 4, 0.20),     # low-confidence transition/pause
        ("water", 6, 0.92),       # 6 frames of "water"
        ("unknown", 3, 0.30),     # pause
        ("please", 5, 0.85),      # 5 frames of "please"
    ]

    timestamp = time.time()
    print("\n--- STREAMING PREDICTIONS (CONTRACT C -> CONTRACT D & E) ---\n")

    for sign_label, frame_count, conf in sign_phases:
        for i in range(frame_count):
            pred = {
                "label": sign_label,
                "confidence": conf,
                "timestamp": timestamp
            }
            timestamp += 0.05
            time.sleep(0.04)

            # 1. Prediction Filter (Contract C -> Contract D)
            stable_event = filter_engine.process_prediction(pred)

            if stable_event:
                print(f"[Contract D - Stable Sign Event Detected!]")
                print(json.dumps(stable_event, indent=2))

                # 2. Word Buffer & Sentence Builder (Contract D -> Contract E)
                sentence_obj = builder.add_word(stable_event)
                print(f"\n[Contract E - Running Sentence Object]")
                print(json.dumps(sentence_obj, indent=2))
                print("-" * 50)

    # 3. Finalize sentence and speak via TTS (Contract F)
    final_sentence = builder.finalize_sentence()
    print("\n" + "=" * 60)
    print(f"  FINAL SMOOTHED SENTENCE (Contract E): \"{final_sentence['text']}\"")
    print(f"  RECOGNIZED WORDS: {final_sentence['words']}")
    print("=" * 60)

    print("\n[Agent 3 TTS] Speaking sentence asynchronously without blocking camera...")
    t0 = time.time()
    tts.speak_sentence(final_sentence)
    queue_time = time.time() - t0
    print(f"[Agent 3 TTS] speak_sentence returned in {queue_time:.4f}s (Non-blocking verified!)")

    print("[Agent 3 TTS] Waiting for speech playback to finish...")
    tts.wait_until_done(timeout=4.0)
    print("[Agent 3 TTS] Playback complete.")

    tts.shutdown()
    print("\nAgent 3 demo finished successfully.")

if __name__ == "__main__":
    run_demo()
