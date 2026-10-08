"""Unit tests for SignBridgeApp (Agent 4 - UI & Integration)."""

import numpy as np
import pytest
from app.ui.app import SignBridgeApp


@pytest.fixture
def headless_app():
    """Create a headless SignBridgeApp with mock camera for testing."""
    app = SignBridgeApp(mock_camera=True, headless=True, tts_enabled=False, stability_window=5)
    yield app
    app.close()


def test_app_initialization(headless_app):
    """Verify application initializes all subsystems properly."""
    assert headless_app.mock_camera is True
    assert headless_app.headless is True
    assert headless_app.camera is not None
    assert headless_app.model is not None
    assert headless_app.pred_filter is not None
    assert headless_app.sentence_builder is not None
    assert headless_app.tts is not None
    assert headless_app.renderer is not None


def test_app_contract_g_schema(headless_app):
    """Verify get_ui_state strictly matches Contract G schema."""
    state = headless_app.get_ui_state()

    # Required top-level keys
    assert "current_sign" in state
    assert "confidence" in state
    assert "recognized_words" in state
    assert "sentence" in state
    assert "status" in state

    # Subsystem status keys
    status = state["status"]
    assert "camera" in status
    assert "model" in status
    assert "speech" in status
    assert isinstance(status["camera"], bool)
    assert isinstance(status["model"], bool)
    assert isinstance(status["speech"], bool)


def test_app_step_execution(headless_app):
    """Verify step() runs a frame and produces valid canvas and state."""
    canvas, state, should_continue = headless_app.step()

    assert should_continue is True
    assert isinstance(canvas, np.ndarray)
    assert canvas.shape == (680, 1000, 3)
    assert canvas.dtype == np.uint8
    assert "sentence" in state


def test_app_prediction_injection(headless_app):
    """Verify simulated prediction injection produces stable words and sentences."""
    # Inject 4 frames (should not stabilize yet)
    for _ in range(4):
        event = headless_app.inject_prediction("hello", confidence=0.88)
        assert event is None

    # 5th frame stabilizes
    event = headless_app.inject_prediction("hello", confidence=0.90)
    assert event is not None
    assert event["word"] == "hello"

    state = headless_app.get_ui_state()
    assert state["recognized_words"] == ["hello"]
    assert state["sentence"] == "Hello."


def test_app_keyboard_controls(headless_app):
    """Verify keyboard event handlers for backspace, clear, mock toggle, and quick signs."""
    # 1. Inject two words
    for _ in range(5):
        headless_app.inject_prediction("hello", confidence=0.85)
    for _ in range(5):
        headless_app.inject_prediction("water", confidence=0.90)

    state = headless_app.get_ui_state()
    assert len(state["recognized_words"]) == 2

    # 2. Test Backspace ('\b')
    res = headless_app.handle_key(ord('\b'))
    assert res is True
    assert headless_app.sentence_builder.get_words() == ["hello"]

    # 3. Test Clear ('c')
    res = headless_app.handle_key(ord('c'))
    assert res is True
    assert headless_app.sentence_builder.get_words() == []

    # 4. Test Demo Quick Signs ('1' for hello)
    res = headless_app.handle_key(ord('1'))
    assert res is True
    assert "hello" in headless_app.sentence_builder.get_words()

    # 5. Test Quit ('q')
    res = headless_app.handle_key(ord('q'))
    assert res is False


def test_app_reset(headless_app):
    """Verify reset() clears word buffer, filter state, and sequence buffer."""
    for _ in range(5):
        headless_app.inject_prediction("help", confidence=0.90)

    assert len(headless_app.sentence_builder.get_words()) == 1

    headless_app.reset()
    state = headless_app.get_ui_state()
    assert state["current_sign"] is None
    assert state["confidence"] == 0.0
    assert state["recognized_words"] == []
    assert state["sentence"] == ""


def test_app_headless_run(headless_app):
    """Verify app.run() executes specified number of frames in headless mode."""
    headless_app.run(max_frames=5)
    assert headless_app.is_running is False


def test_app_target_fps_configuration():
    """Verify target_fps configuration and pacing initialization."""
    app = SignBridgeApp(mock_camera=True, headless=True, target_fps=60)
    assert app.target_fps == 60
    app.close()
