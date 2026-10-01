"""Demo Script for Agent 4 (UI & Full System Integration).

Demonstrates the real-time live dashboard overlay, contract compliance,
interactive controls, and end-to-end integration across all 4 agents.

Usage:
    python scripts/demo_agent4.py              # Runs interactive demo with mock camera
    python scripts/demo_agent4.py --live       # Runs with physical webcam
    python scripts/demo_agent4.py --headless   # Runs in headless benchmark mode
"""

import sys
import os
import time
import argparse

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.ui.app import SignBridgeApp


def run_demo():
    parser = argparse.ArgumentParser(description="SignBridge Agent 4 Live Integration Demo")
    parser.add_argument("--live", action="store_true", help="Use live webcam instead of mock camera")
    parser.add_argument("--headless", action="store_true", help="Run without opening GUI window")
    parser.add_argument("--auto-simulate", action="store_true", default=True, help="Automatically inject demo signs")
    parser.add_argument("--frames", type=int, default=120, help="Number of frames for automated demo")
    args = parser.parse_args()

    use_mock = not args.live

    print("=" * 65)
    print("   SIGN-BRIDGE: AGENT 4 (UI & INTEGRATION) LIVE DEMO         ")
    print("=" * 65)
    print(f" Camera Source: {'MOCK CAMERA (Synthetic Feed)' if use_mock else 'LIVE WEBCAM'}")
    print(f" GUI Window:    {'DISABLED (Headless Benchmark)' if args.headless else 'ENABLED'}")
    print(" Controls:       [S] Speak | [C] Clear | [Backspace] Undo | [M] Toggle Mock | [Q] Quit")
    print(" Quick Signs:    [1] Hello | [2] Thank You | [3] Please | [4] Water | [5] Help")
    print("=" * 65)

    app = SignBridgeApp(
        mock_camera=use_mock,
        headless=args.headless,
        tts_enabled=True,
    )

    print("\n[Init] Initialized end-to-end SignBridge application.")
    print("[Pipeline] Agent 1 (Video) -> Agent 2 (Inference) -> Agent 3 (Logic+TTS) -> Agent 4 (UI)")

    # In automated demo mode, inject sample signs at specific intervals
    auto_signs = [
        (15, "hello"),
        (45, "water"),
        (75, "please"),
    ]

    frame_count = 0
    try:
        target_frame_time = 1.0 / 30.0
        while frame_count < (args.frames if args.headless else 999999):
            frame_start = time.perf_counter()
            frame_count += 1

            # Auto inject signs during demo if requested
            for trigger_frame, sign in auto_signs:
                if frame_count == trigger_frame:
                    print(f"\n[Demo Automation] Injecting stable sign: '{sign}'...")
                    for _ in range(5):
                        app.inject_prediction(sign, confidence=0.92)

            canvas, ui_state, should_continue = app.step()
            if not should_continue:
                break

            # Print status periodically
            if frame_count in (25, 55, 85):
                print(f"[Frame {frame_count}] Contract G UI State:")
                print(f"  Current Sign:     {ui_state['current_sign']}")
                print(f"  Confidence:       {ui_state['confidence']}")
                print(f"  Recognized Words: {ui_state['recognized_words']}")
                print(f"  Smoothed Text:    '{ui_state['sentence']}'")

            # At frame 90, speak the sentence automatically
            if frame_count == 90:
                print("\n[Demo Automation] Speaking smoothed sentence via TTS (Contract F)...")
                app.handle_key(ord('s'))

            elapsed = time.perf_counter() - frame_start
            if not args.headless:
                import cv2
                cv2.imshow("SignBridge Live Demo (Agent 4)", canvas)
                remaining_ms = max(1, int((target_frame_time - elapsed) * 1000))
                key = cv2.waitKey(remaining_ms)
                if not app.handle_key(key):
                    break
            else:
                sleep_time = max(0.001, target_frame_time - elapsed)
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[Demo] Interrupted by user.")
    finally:
        app.close()
        print("\n[Demo] SignBridge Application cleanly shut down.")
        print("Agent 4 Live Integration Demo completed successfully.")


if __name__ == "__main__":
    run_demo()
