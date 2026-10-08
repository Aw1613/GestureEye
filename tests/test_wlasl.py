"""Unit tests for Pretrained WLASL-100 Sign Language Recognition System."""

import os
import numpy as np
import pytest
import torch

from app.recognition.wlasl_model import WLASLTGCN
from app.recognition.wlasl_inference import WLASLInference, MediaPipeHolisticExtractor


def test_wlasl_model_forward():
    """Verify WLASLTGCN forward pass with correct output shape."""
    model = WLASLTGCN(
        input_feature=100,
        hidden_feature=64,
        num_class=100,
        p_dropout=0.0,
        num_stage=20,
    )
    model.eval()

    # Input: (batch=2, keypoints=55, features=100)
    x = torch.randn(2, 55, 100)
    out = model(x)

    assert out.shape == (2, 100)


def test_wlasl_inference_initialization():
    """Verify WLASLInference loads weights and 100 gloss vocabulary."""
    inference = WLASLInference(num_frames=50)

    assert inference.num_classes == 100
    assert len(inference.id_to_label) == 100
    assert "0" in inference.id_to_label
    assert inference.id_to_label["0"] == "book"


def test_wlasl_predict_sequence():
    """Verify predict_sequence returns valid top-1 and top-5 schemas."""
    inference = WLASLInference(num_frames=50)
    dummy_seq = np.zeros((50, 55, 2), dtype=np.float32)

    result = inference.predict_sequence(dummy_seq)

    assert "label" in result
    assert "confidence" in result
    assert "top_5" in result
    assert "timestamp" in result
    assert isinstance(result["label"], str)
    assert 0.0 <= result["confidence"] <= 1.0
    assert len(result["top_5"]) == 5
    for cand in result["top_5"]:
        assert "label" in cand
        assert "confidence" in cand
        assert 0.0 <= cand["confidence"] <= 1.0


def test_holistic_extractor_blank_frame():
    """Verify MediaPipeHolisticExtractor processes blank frame without crashing."""
    extractor = MediaPipeHolisticExtractor()
    blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    keypoints, annotated = extractor.extract(blank_frame, draw=False)

    assert keypoints.shape == (55, 2)
    assert np.all(keypoints == 0.0)  # No body detected in blank frame
    extractor.close()
