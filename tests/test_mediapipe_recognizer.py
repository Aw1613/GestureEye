"""Tests for Pretrained MediaPipe Zero-Training Gesture Recognizer."""

import os
import numpy as np
import pytest
from app.recognition.mediapipe_recognizer import MediaPipeGestureRecognizer


def test_mediapipe_recognizer_init():
    """Verify recognizer loads the model asset successfully."""
    recognizer = MediaPipeGestureRecognizer()
    assert recognizer.recognizer is not None
    assert os.path.exists(recognizer.model_path)


def test_mediapipe_recognizer_blank_frame():
    """Verify recognition on a blank image returns valid output schema."""
    recognizer = MediaPipeGestureRecognizer()
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    result = recognizer.recognize_frame(dummy_frame)

    assert "label" in result
    assert "confidence" in result
    assert "gestures" in result
    assert "timestamp" in result
    assert result["label"] == "None"
    assert result["confidence"] == 0.0
    assert result["gestures"] == []


def test_mediapipe_recognizer_empty_frame():
    """Verify graceful handling of None or empty frame input."""
    recognizer = MediaPipeGestureRecognizer()
    result = recognizer.recognize_frame(None)

    assert result["label"] == "None"
    assert result["confidence"] == 0.0
