"""Unit tests for timing gap (cooldown) between consecutive sign fetches.

Verifies:
1. 0.5s timing gap between two consecutive signs to fetch.
2. If signs are the same within the timing gap, do not enter fetch mode.
3. If signs are different within the timing gap, display only and nothing else (sentence buffer unchanged).
4. After 0.5s timing gap elapses, stabilized different sign is fetched into sentence buffer.
"""

import time
import pytest
from app.sentence.filter import PredictionFilter
from app.ui.app import SignBridgeApp


def test_filter_timing_gap_blocks_early_different_sign():
    """Verify PredictionFilter suppresses fetching a new sign if within timing_gap (0.5s)."""
    filter_engine = PredictionFilter(
        confidence_threshold=0.60,
        stability_window=3,
        timing_gap=0.5,
    )

    t0 = 1000.0
    # 1. Accept first sign: "hello" at t0
    for i in range(3):
        ev = filter_engine.process_prediction({
            "label": "hello",
            "confidence": 0.90,
            "timestamp": t0 + 0.05 * i,  # 1000.0, 1000.05, 1000.10
        })
    assert ev is not None
    assert ev["word"] == "hello"

    # 2. Within timing gap (< 0.5s since last fetch at 1000.10): stream different sign "water"
    # Timestamps: 1000.20, 1000.25, 1000.30 (all within 0.20s of last fetch)
    water_event = None
    for i in range(3):
        res = filter_engine.process_prediction({
            "label": "water",
            "confidence": 0.92,
            "timestamp": 1000.20 + 0.05 * i,
        })
        if res:
            water_event = res

    # Must NOT be emitted during timing gap
    assert water_event is None

    # 3. After timing gap (t >= 1000.10 + 0.5 = 1000.60):
    # Stream "water" frame at 1000.65
    res = filter_engine.process_prediction({
        "label": "water",
        "confidence": 0.92,
        "timestamp": 1000.65,
    })
    assert res is not None
    assert res["word"] == "water"


def test_filter_timing_gap_same_sign_no_fetch_mode():
    """Verify that within timing gap, same sign does not go into fetch mode."""
    filter_engine = PredictionFilter(
        confidence_threshold=0.60,
        stability_window=3,
        timing_gap=0.5,
    )

    t0 = 2000.0
    # 1. Accept "help"
    for i in range(3):
        filter_engine.process_prediction({
            "label": "help",
            "confidence": 0.95,
            "timestamp": t0 + 0.05 * i,
        })

    # 2. Continue signing "help" during and after timing gap
    for i in range(10):
        ev = filter_engine.process_prediction({
            "label": "help",
            "confidence": 0.95,
            "timestamp": t0 + 0.20 + 0.1 * i,
        })
        # Should never re-emit because it is the same sign
        assert ev is None


def test_app_timing_gap_display_only_behavior():
    """Verify SignBridgeApp displays different sign during 0.5s gap without fetching into sentence."""
    app = SignBridgeApp(
        mock_camera=True,
        headless=True,
        tts_enabled=False,
        stability_window=3,
        fetch_gap=0.5,
    )

    try:
        t_base = 5000.0

        # 1. First sign: "hello" stabilized and fetched
        for i in range(3):
            app.inject_prediction("hello", confidence=0.90, timestamp=t_base + 0.05 * i)

        assert app.sentence_builder.get_words() == ["hello"]
        assert app.current_sign == "hello"

        # 2. Within 0.5s gap (e.g. t_base + 0.2s):
        # A different sign "water" is detected
        for i in range(3):
            app.inject_prediction("water", confidence=0.88, timestamp=t_base + 0.20 + 0.02 * i)

        # CURRENT SIGN is updated to "water" (displayed only!)
        assert app.current_sign == "water"
        # BUT sentence words buffer is untouched (NOT fetched!)
        assert app.sentence_builder.get_words() == ["hello"]
        # Fetch mode is False (display-only mode)
        assert app.is_fetch_mode is False

        ui_state = app.get_ui_state()
        assert ui_state["current_sign"] == "water"
        assert ui_state["recognized_words"] == ["hello"]
        assert ui_state["is_fetch_mode"] is False

        # 3. After timing gap elapses (t_base + 0.65s >= last_fetch + 0.5s):
        app.inject_prediction("water", confidence=0.92, timestamp=t_base + 0.65)

        # Now "water" is fetched into the sentence!
        assert app.sentence_builder.get_words() == ["hello", "water"]
        assert app.current_sign == "water"

    finally:
        app.close()


def test_app_reset_clears_timing_gap_state():
    """Verify reset() clears timing gap state."""
    app = SignBridgeApp(
        mock_camera=True,
        headless=True,
        tts_enabled=False,
        stability_window=3,
        fetch_gap=0.5,
    )
    try:
        app.inject_prediction("hello", confidence=0.90, timestamp=100.0)
        app.inject_prediction("hello", confidence=0.90, timestamp=100.1)
        app.inject_prediction("hello", confidence=0.90, timestamp=100.2)

        assert app.last_fetch_time is not None
        assert app.last_fetched_sign == "hello"

        app.reset()

        assert app.last_fetch_time is None
        assert app.last_fetched_sign is None
        assert app.is_fetch_mode is True
        assert app.sentence_builder.get_words() == []
    finally:
        app.close()
