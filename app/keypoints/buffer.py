"""Rolling Sequence Buffer Module for SignBridge (Agent 1).

Maintains a fixed-size temporal window of normalized keypoint feature vectors
conforming to CONTRACTS.md Contract B: shape (SEQUENCE_LENGTH, FEATURE_DIM).
"""

from collections import deque
from typing import Optional
import numpy as np

from app.keypoints.preprocessing import FEATURE_DIM

DEFAULT_SEQUENCE_LENGTH = 30


class SequenceBuffer:
    """Sliding window buffer for temporal keypoint sequences."""

    def __init__(
        self,
        sequence_length: int = DEFAULT_SEQUENCE_LENGTH,
        feature_dim: int = FEATURE_DIM,
    ):
        """Initialize the rolling buffer.

        Args:
            sequence_length: Number of consecutive frames required for one sequence (default 30).
            feature_dim: Dimensionality of each frame's feature vector (default 126).
        """
        self.sequence_length = sequence_length
        self.feature_dim = feature_dim
        self._buffer: deque = deque(maxlen=sequence_length)

    def append(self, feature_vector: np.ndarray) -> None:
        """Append a new frame's feature vector to the buffer.

        Args:
            feature_vector: np.ndarray of shape (feature_dim,).
        """
        if feature_vector is None or feature_vector.shape != (self.feature_dim,):
            # Fallback to zero vector if invalid
            feature_vector = np.zeros(self.feature_dim, dtype=np.float32)

        self._buffer.append(feature_vector.astype(np.float32))

    def is_ready(self) -> bool:
        """Return True if the buffer contains a full temporal sequence."""
        return len(self._buffer) == self.sequence_length

    def get_sequence(self) -> Optional[np.ndarray]:
        """Return the current sequence window if full, or None if still accumulating.

        Returns:
            np.ndarray of shape (sequence_length, feature_dim) and dtype float32,
            or None if fewer than sequence_length frames are buffered.
        """
        if not self.is_ready():
            return None
        return np.array(self._buffer, dtype=np.float32)

    def reset(self) -> None:
        """Clear all stored frames in the buffer."""
        self._buffer.clear()

    def __len__(self) -> int:
        """Return the current number of frames in the buffer."""
        return len(self._buffer)
