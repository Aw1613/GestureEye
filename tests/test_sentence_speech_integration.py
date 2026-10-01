"""
Integration test: Contract C (Agent 2) -> Contract D & E (Agent 3) -> Contract F (TTS)
"""

import time
import pytest
from app.sentence.filter import PredictionFilter
from app.sentence.builder import SentenceBuilder
from app.tts.speech import TextToSpeech


def test_end_to_end_agent3_pipeline():
    """
    Test streaming predictions from Agent 2 into Agent 3 filter,
    building a sentence, and queuing TTS output.
    """
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)
    builder = SentenceBuilder()
    tts = TextToSpeech(enabled=False)

    try:
        # 1. Stream signs: "hello", "thank_you", "water"
        signs_stream = ["hello"] * 7 + ["thank_you"] * 6 + ["water"] * 5
        timestamp = 1727721.0

        for sign in signs_stream:
            pred = {
                "label": sign,
                "confidence": 0.88,
                "timestamp": timestamp
            }
            timestamp += 0.05
            stable_event = filter_engine.process_prediction(pred)
            if stable_event is not None:
                # Passes Contract D to SentenceBuilder
                builder.add_word(stable_event)

        # 2. Check Contract E output
        sentence_obj = builder.build_sentence()
        assert sentence_obj["words"] == ["hello", "thank_you", "water"]
        assert sentence_obj["text"] == "Hello, thank you for the water."

        # 3. Pass Contract E to TTS (Contract F)
        success = tts.speak_sentence(sentence_obj)
        assert success is True

        tts.wait_until_done(timeout=2.0)
        assert "Hello, thank you for the water." in tts.spoken_history

    finally:
        tts.shutdown()
