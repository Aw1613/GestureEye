"""Unit tests for Keypoints Extractor, Preprocessing, and Sequence Buffer (Agent 1)."""

import unittest
import numpy as np
from app.keypoints.preprocessing import (
    LANDMARKS_PER_HAND,
    COORDS_PER_LANDMARK,
    FEATURE_DIM,
    normalize_hand_landmarks,
    assemble_feature_vector,
)
from app.keypoints.extractor import HandKeypointExtractor
from app.keypoints.buffer import SequenceBuffer


class TestKeypointPreprocessing(unittest.TestCase):
    """Test suite for preprocessing and normalization."""

    def test_normalize_hand_landmarks(self):
        """Verify that normalization shifts wrist to (0,0,0) and bounds values in [-1, 1]."""
        # Create fake hand landmarks where wrist is at (10, 20, 30)
        raw = np.random.uniform(low=0.0, high=100.0, size=(21, 3)).astype(np.float32)
        raw[0] = [10.0, 20.0, 30.0]

        normalized = normalize_hand_landmarks(raw)

        self.assertEqual(normalized.shape, (21, 3))
        # Wrist must be at origin (0, 0, 0)
        np.testing.assert_allclose(normalized[0], [0.0, 0.0, 0.0], atol=1e-5)
        # All values must be bounded within [-1.0, 1.0]
        self.assertTrue(np.all(np.abs(normalized) <= 1.0 + 1e-5))

    def test_assemble_feature_vector_shapes(self):
        """Verify vector shape is exactly (126,) for one-hand, two-hand, and missing hands."""
        left = np.random.uniform(size=(21, 3)).astype(np.float32)
        right = np.random.uniform(size=(21, 3)).astype(np.float32)

        # Case 1: Both hands present
        both_vec = assemble_feature_vector(left, right)
        self.assertEqual(both_vec.shape, (FEATURE_DIM,))
        self.assertEqual(both_vec.dtype, np.float32)

        # Case 2: Only right hand present (left hand should be all 0.0)
        right_only_vec = assemble_feature_vector(None, right)
        self.assertEqual(right_only_vec.shape, (126,))
        self.assertTrue(np.all(right_only_vec[:63] == 0.0))
        self.assertFalse(np.all(right_only_vec[63:] == 0.0))

        # Case 3: No hands present (all 0.0)
        none_vec = assemble_feature_vector(None, None)
        self.assertEqual(none_vec.shape, (126,))
        self.assertTrue(np.all(none_vec == 0.0))


class TestKeypointExtractor(unittest.TestCase):
    """Test suite for MediaPipe HandKeypointExtractor."""

    def test_extract_from_blank_frame(self):
        """Verify extractor returns zeros and false flags on a blank frame without error."""
        extractor = HandKeypointExtractor(static_image_mode=True)
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        vector, info, annotated = extractor.extract_keypoints(blank_frame, draw=True)

        self.assertEqual(vector.shape, (126,))
        self.assertEqual(vector.dtype, np.float32)
        self.assertTrue(np.all(vector == 0.0))
        self.assertFalse(info["left_detected"])
        self.assertFalse(info["right_detected"])
        self.assertEqual(info["hands_count"], 0)
        self.assertEqual(annotated.shape, (480, 640, 3))
        extractor.close()


class TestSequenceBuffer(unittest.TestCase):
    """Test suite for rolling SequenceBuffer."""

    def test_buffer_sliding_window(self):
        """Verify buffer readiness and sequence output shape."""
        buffer = SequenceBuffer(sequence_length=30, feature_dim=126)

        # Initially empty
        self.assertFalse(buffer.is_ready())
        self.assertIsNone(buffer.get_sequence())
        self.assertEqual(len(buffer), 0)

        # Add 29 frames (not yet full)
        for i in range(29):
            buffer.append(np.ones(126, dtype=np.float32) * i)
            self.assertFalse(buffer.is_ready())

        # Add 30th frame
        buffer.append(np.ones(126, dtype=np.float32) * 29)
        self.assertTrue(buffer.is_ready())
        seq = buffer.get_sequence()
        self.assertIsNotNone(seq)
        self.assertEqual(seq.shape, (30, 126))
        self.assertEqual(seq.dtype, np.float32)
        self.assertEqual(seq[0, 0], 0.0)
        self.assertEqual(seq[29, 0], 29.0)

        # Add 31st frame (sliding window test)
        buffer.append(np.ones(126, dtype=np.float32) * 30)
        self.assertEqual(len(buffer), 30)
        seq2 = buffer.get_sequence()
        self.assertEqual(seq2[0, 0], 1.0)
        self.assertEqual(seq2[29, 0], 30.0)

        # Reset
        buffer.reset()
        self.assertFalse(buffer.is_ready())
        self.assertEqual(len(buffer), 0)


if __name__ == "__main__":
    unittest.main()
