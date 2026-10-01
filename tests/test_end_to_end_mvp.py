"""End-to-End MVP Integration Tests (Milestone M5 - Agent 1 + 2 + 3 + 4).

Validates the full pipeline flow:
Camera -> Keypoint Extraction -> Sequence Buffer -> Model Inference ->
Prediction Filter -> Sentence Builder -> Async TTS -> UI Dashboard & Contract G.
"""

import time
import numpy as np
import pytest
from app.ui.app import SignBridgeApp


def test_full_pipeline_end_to_end():
    """Verify frames flow seamlessly through all 4 agents in real-time."""
    app = SignBridgeApp(
        mock_camera=True,
        headless=True,
        tts_enabled=True,
        confidence_threshold=0.50,
        stability_window=3,
    )

    try:
        # Step through 35 frames:
        # Frames 1-29 fill the sequence buffer (Agent 1)
        # Frame 30+ triggers model inference (Agent 2) & prediction filter (Agent 3)
        # All frames render Contract G state & composite UI canvas (Agent 4)
        for frame_idx in range(35):
            canvas, ui_state, should_continue = app.step()
            assert should_continue is True
            assert isinstance(canvas, np.ndarray)
            assert canvas.shape == (680, 1000, 3)

            # Contract G assertion
            assert "current_sign" in ui_state
            assert "confidence" in ui_state
            assert "recognized_words" in ui_state
            assert "sentence" in ui_state
            assert "status" in ui_state
            assert ui_state["status"]["camera"] is True
            assert ui_state["status"]["model"] is True

        # After 30 frames, sequence buffer is ready
        assert app.seq_buffer.is_ready() is True
        # Model should have predicted at least once
        assert app.current_sign is not None

        # Verify speech invocation works non-blocking
        app.sentence_builder.add_word("thank_you")
        start_t = time.time()
        res = app.handle_key(ord('s'))
        duration = time.time() - start_t

        assert res is True
        # Must return in under 5ms (non-blocking)
        assert duration < 0.05

        # Verify clearing works
        app.handle_key(ord('c'))
        assert app.sentence_builder.get_words() == []

    finally:
        app.close()
