"""Landmark Preprocessing and Normalization Module for SignBridge (Agent 1).

Complies strictly with CONTRACTS.md Contract A:
- Left hand (21 landmarks x 3 coords = 63 floats)
- Right hand (21 landmarks x 3 coords = 63 floats)
- Total feature vector: 126 floats (float32)
- Wrist-relative translation normalization
- Maximum-absolute-coordinate scale normalization
- Missing hand padding with zeros (0.0)
"""

from typing import Optional, List, Dict
import numpy as np

LANDMARKS_PER_HAND = 21
COORDS_PER_LANDMARK = 3
HAND_FEATURE_DIM = LANDMARKS_PER_HAND * COORDS_PER_LANDMARK  # 63
FEATURE_DIM = HAND_FEATURE_DIM * 2  # 126


def normalize_hand_landmarks(landmarks_array: np.ndarray) -> np.ndarray:
    """Normalize a single hand's landmarks (21, 3) relative to the wrist.

    Args:
        landmarks_array: numpy array of shape (21, 3) representing (x, y, z)
                         coordinates for 21 hand landmarks.

    Returns:
        Normalized numpy array of shape (21, 3), where wrist is at (0, 0, 0)
        and coordinate scale is normalized to [-1.0, 1.0].
    """
    if landmarks_array is None or landmarks_array.shape != (LANDMARKS_PER_HAND, COORDS_PER_LANDMARK):
        return np.zeros((LANDMARKS_PER_HAND, COORDS_PER_LANDMARK), dtype=np.float32)

    # Wrist is landmark index 0
    wrist = landmarks_array[0].copy()

    # Step 1: Translation invariance - shift wrist to origin (0, 0, 0)
    shifted = landmarks_array - wrist

    # Step 2: Scale invariance - divide by the maximum absolute coordinate value
    max_val = np.max(np.abs(shifted))
    if max_val > 1e-6:
        normalized = shifted / max_val
    else:
        normalized = shifted

    return normalized.astype(np.float32)


def assemble_feature_vector(
    left_hand: Optional[np.ndarray],
    right_hand: Optional[np.ndarray],
) -> np.ndarray:
    """Combine normalized left and right hand landmarks into a (126,) vector.

    Args:
        left_hand: (21, 3) raw or normalized array for left hand, or None if not detected.
        right_hand: (21, 3) raw or normalized array for right hand, or None if not detected.

    Returns:
        numpy array of shape (126,) and dtype float32 conforming to Contract A.
    """
    # Process left hand
    if left_hand is not None:
        norm_left = normalize_hand_landmarks(left_hand).flatten()
    else:
        norm_left = np.zeros(HAND_FEATURE_DIM, dtype=np.float32)

    # Process right hand
    if right_hand is not None:
        norm_right = normalize_hand_landmarks(right_hand).flatten()
    else:
        norm_right = np.zeros(HAND_FEATURE_DIM, dtype=np.float32)

    # Concatenate Left [0:63] and Right [63:126]
    vector = np.concatenate([norm_left, norm_right], axis=0).astype(np.float32)
    return vector


class KeypointPreprocessor:
    """Class wrapper for landmark preprocessing conforming to Contract A."""

    @staticmethod
    def normalize_hand(landmarks: np.ndarray) -> np.ndarray:
        return normalize_hand_landmarks(landmarks)

    @staticmethod
    def normalize(landmarks: np.ndarray) -> np.ndarray:
        """Pass through already normalized feature vectors or normalize single hand."""
        if landmarks is None:
            return np.zeros(FEATURE_DIM, dtype=np.float32)
        if landmarks.shape == (FEATURE_DIM,):
            return landmarks
        return normalize_hand_landmarks(landmarks)

    @staticmethod
    def assemble(left: Optional[np.ndarray], right: Optional[np.ndarray]) -> np.ndarray:
        return assemble_feature_vector(left, right)

