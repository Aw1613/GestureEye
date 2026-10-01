"""
Unit tests for TextToSpeech (Agent 3 - Contract F)
"""

import time
import pytest
from app.tts.speech import TextToSpeech


def test_tts_non_blocking_call():
    """speak() must return immediately (< 50ms) to ensure camera capture is not frozen."""
    tts = TextToSpeech(enabled=False)
    try:
        t0 = time.time()
        success = tts.speak("Hello this is a real-time sentence test")
        elapsed = time.time() - t0

        assert success is True
        # Must return virtually instantly
        assert elapsed < 0.05, f"speak() took {elapsed:.4f}s, which would block real-time loop"
    finally:
        tts.shutdown()


def test_tts_speak_sentence_dict():
    """speak_sentence must accept Contract E / F dictionary schemas."""
    tts = TextToSpeech(enabled=False)
    try:
        contract_f = {"text": "Hello, thank you for the water."}
        success = tts.speak_sentence(contract_f)
        assert success is True

        tts.wait_until_done(timeout=2.0)
        assert "Hello, thank you for the water." in tts.spoken_history
    finally:
        tts.shutdown()


def test_tts_stop_clears_queue():
    """stop() must empty pending queue items."""
    tts = TextToSpeech(enabled=False)
    try:
        for i in range(5):
            tts.speak(f"Message {i}")

        tts.stop()
        assert tts._queue.empty()
    finally:
        tts.shutdown()


def test_tts_empty_and_invalid_inputs():
    """Empty strings and invalid types should return False gracefully."""
    tts = TextToSpeech(enabled=False)
    try:
        assert tts.speak("") is False
        assert tts.speak("   ") is False
        assert tts.speak(None) is False
        assert tts.speak_sentence({}) is False
    finally:
        tts.shutdown()
