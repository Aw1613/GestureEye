"""
Unit tests for PredictionFilter (Agent 3 - Contract D)
"""

import time
import pytest
from app.sentence.filter import PredictionFilter


def test_filter_requires_stability_window():
    """Verify exactly 5 consecutive agreeing predictions above 0.60 confidence are required."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)

    base_time = 1727721.0
    predictions = [
        {"label": "hello", "confidence": 0.85, "timestamp": base_time + 0.1 * i}
        for i in range(4)
    ]

    # First 4 frames: should NOT emit an event
    for p in predictions:
        event = filter_engine.process_prediction(p)
        assert event is None

    # 5th frame: should emit Contract D event
    p5 = {"label": "hello", "confidence": 0.90, "timestamp": base_time + 0.5}
    event = filter_engine.process_prediction(p5)

    assert event is not None
    assert event["word"] == "hello"
    assert event["confidence"] >= 0.60
    assert event["start_time"] == base_time
    assert event["end_time"] == base_time + 0.5
    # Verify Contract D keys
    for key in ["word", "confidence", "start_time", "end_time"]:
        assert key in event


def test_filter_rejects_low_confidence():
    """Predictions below 0.60 confidence must not trigger sign acceptance and reset count."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)

    # 3 valid predictions
    for i in range(3):
        assert filter_engine.process_prediction({"label": "water", "confidence": 0.75, "timestamp": i}) is None

    # 1 low confidence prediction (< 0.60)
    assert filter_engine.process_prediction({"label": "water", "confidence": 0.45, "timestamp": 3.0}) is None

    # 2 more valid predictions: total consecutive is now only 2, so should still be None
    assert filter_engine.process_prediction({"label": "water", "confidence": 0.80, "timestamp": 4.0}) is None
    assert filter_engine.process_prediction({"label": "water", "confidence": 0.82, "timestamp": 5.0}) is None


def test_duplicate_suppression_holding_sign():
    """Holding a sign for 10 frames emits only once at frame 5, not at frames 6-10."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)

    emitted_events = []
    for i in range(10):
        pred = {"label": "thank_you", "confidence": 0.90, "timestamp": 100.0 + i}
        event = filter_engine.process_prediction(pred)
        if event is not None:
            emitted_events.append(event)

    assert len(emitted_events) == 1
    assert emitted_events[0]["word"] == "thank_you"


def test_filter_sign_transition():
    """Switching to a new sign emits the new sign after 5 consecutive agreeing frames."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)

    # Emit "hello"
    for i in range(5):
        filter_engine.process_prediction({"label": "hello", "confidence": 0.85, "timestamp": float(i)})

    # Transition to "water"
    water_events = []
    for i in range(5, 10):
        ev = filter_engine.process_prediction({"label": "water", "confidence": 0.92, "timestamp": float(i)})
        if ev:
            water_events.append(ev)

    assert len(water_events) == 1
    assert water_events[0]["word"] == "water"


def test_filter_pause_allows_repeating_same_sign():
    """After a pause/rest period, the user can sign the same word again."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5, pause_threshold_frames=5)

    # 1. Sign "help" -> emits event
    ev1 = None
    for i in range(5):
        ev1 = filter_engine.process_prediction({"label": "help", "confidence": 0.88, "timestamp": float(i)}) or ev1
    assert ev1 is not None and ev1["word"] == "help"

    # 2. 5 frames of low confidence / idle pause
    for i in range(5, 10):
        ev = filter_engine.process_prediction({"label": "unknown", "confidence": 0.10, "timestamp": float(i)})
        assert ev is None

    # 3. Sign "help" again for 5 frames -> must emit again
    ev2 = None
    for i in range(10, 15):
        ev2 = filter_engine.process_prediction({"label": "help", "confidence": 0.89, "timestamp": float(i)}) or ev2
    assert ev2 is not None
    assert ev2["word"] == "help"


def test_filter_reset():
    """Calling reset() clears all internal state."""
    filter_engine = PredictionFilter(confidence_threshold=0.60, stability_window=5)
    for i in range(4):
        filter_engine.process_prediction({"label": "food", "confidence": 0.85, "timestamp": float(i)})

    filter_engine.reset()
    status = filter_engine.get_status()
    assert status["current_candidate"] is None
    assert status["consecutive_count"] == 0
    assert status["last_accepted_word"] is None
