"""Unit tests for UIOverlayRenderer (Agent 4 - Contract G Dashboard)."""

import numpy as np
import pytest
from app.ui.overlay import UIOverlayRenderer


def test_renderer_initialization():
    """Verify renderer dimensions and defaults."""
    renderer = UIOverlayRenderer(canvas_width=1000, canvas_height=680)
    assert renderer.canvas_width == 1000
    assert renderer.canvas_height == 680


def test_render_empty_state():
    """Verify rendering with empty state and no camera feed."""
    renderer = UIOverlayRenderer()
    ui_state = {
        "current_sign": None,
        "confidence": 0.0,
        "recognized_words": [],
        "sentence": "",
        "status": {"camera": False, "model": True, "speech": True},
    }

    canvas = renderer.render(
        camera_frame=None,
        ui_state=ui_state,
        fps=30.0,
        toast_message=None,
        stability_count=0,
        stability_target=5,
    )

    assert isinstance(canvas, np.ndarray)
    assert canvas.shape == (680, 1000, 3)
    assert canvas.dtype == np.uint8


def test_render_active_predictions_and_sentence():
    """Verify rendering with detected sign, confidence, word buffer, and sentence."""
    renderer = UIOverlayRenderer()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    ui_state = {
        "current_sign": "thank_you",
        "confidence": 0.92,
        "recognized_words": ["hello", "thank_you"],
        "sentence": "Hello, thank you.",
        "status": {"camera": True, "model": True, "speech": True},
    }

    canvas = renderer.render(
        camera_frame=dummy_frame,
        ui_state=ui_state,
        fps=28.5,
        toast_message="Accepted: thank_you",
        stability_count=5,
        stability_target=5,
        is_mock_camera=False,
        is_speaking=True,
    )

    assert canvas.shape == (680, 1000, 3)


def test_render_confidence_threshold_colors():
    """Verify rendering does not crash for different confidence tiers."""
    renderer = UIOverlayRenderer()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    for conf in [0.15, 0.45, 0.85]:
        ui_state = {
            "current_sign": "water",
            "confidence": conf,
            "recognized_words": ["water"],
            "sentence": "Water.",
            "status": {"camera": True, "model": True, "speech": True},
        }
        canvas = renderer.render(
            camera_frame=dummy_frame,
            ui_state=ui_state,
            fps=30.0,
        )
        assert canvas.shape == (680, 1000, 3)


def test_render_with_error_and_toast():
    """Verify rendering displays toast message and error alert cleanly."""
    renderer = UIOverlayRenderer()
    ui_state = {
        "current_sign": None,
        "confidence": 0.0,
        "recognized_words": [],
        "sentence": "",
        "status": {"camera": False, "model": False, "speech": False},
    }

    canvas = renderer.render(
        camera_frame=None,
        ui_state=ui_state,
        toast_message="Action Completed",
        error_message="Camera not found",
    )
    assert canvas.shape == (680, 1000, 3)
