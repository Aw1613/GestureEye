"""MediaPipe Hand Landmark Extraction Module for SignBridge (Agent 1).

Extracts 21 3D landmarks per detected hand (up to 2 hands) and returns
a standardized 126-dimensional normalized feature vector conforming to CONTRACTS.md.
"""

from typing import Dict, Optional, Tuple, Any
import cv2
import numpy as np
import mediapipe as mp

from app.keypoints.preprocessing import (
    LANDMARKS_PER_HAND,
    COORDS_PER_LANDMARK,
    FEATURE_DIM,
    assemble_feature_vector,
)


class HandKeypointExtractor:
    """Wrapper around MediaPipe Hands for extracting normalized keypoint features."""

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """Initialize MediaPipe Hands model.

        Args:
            static_image_mode: Whether to treat each image independently.
            max_num_hands: Maximum number of hands to detect (default 2).
            min_detection_confidence: Minimum detection confidence threshold.
            min_tracking_confidence: Minimum tracking confidence threshold.
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract_keypoints(
        self, frame: np.ndarray, draw: bool = False
    ) -> Tuple[np.ndarray, Dict[str, Any], np.ndarray]:
        """Extract hand landmarks from a BGR video frame.

        Args:
            frame: OpenCV BGR image frame (H, W, 3).
            draw: If True, draws landmarks on a copy of the frame.

        Returns:
            Tuple of:
            - feature_vector: np.ndarray of shape (126,), dtype float32
            - info: dict with detection status: {"left_detected": bool, "right_detected": bool, "hands_count": int}
            - annotated_frame: frame with landmarks drawn (or original frame if draw=False)
        """
        if frame is None or frame.size == 0:
            empty_vector = np.zeros(FEATURE_DIM, dtype=np.float32)
            info = {"left_detected": False, "right_detected": False, "hands_count": 0}
            return empty_vector, info, frame

        annotated_frame = frame.copy() if draw else frame

        # MediaPipe expects RGB images
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        left_hand: Optional[np.ndarray] = None
        right_hand: Optional[np.ndarray] = None

        left_detected = False
        right_detected = False
        hands_count = 0

        if results.multi_hand_landmarks and results.multi_handedness:
            hands_count = len(results.multi_hand_landmarks)

            for hand_landmarks, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                # Extract classification label: 'Left' or 'Right'
                label = handedness.classification[0].label

                # Convert landmark list to (21, 3) numpy array [x, y, z]
                coords = np.array(
                    [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark],
                    dtype=np.float32,
                )

                if label == "Left" and left_hand is None:
                    left_hand = coords
                    left_detected = True
                elif label == "Right" and right_hand is None:
                    right_hand = coords
                    right_detected = True
                elif left_hand is None:
                    # Fallback if both labeled same
                    left_hand = coords
                    left_detected = True
                elif right_hand is None:
                    right_hand = coords
                    right_detected = True

                # Draw landmarks if requested
                if draw:
                    self.mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style(),
                    )

        # Assemble into canonical (126,) feature vector
        feature_vector = assemble_feature_vector(left_hand, right_hand)

        info = {
            "left_detected": left_detected,
            "right_detected": right_detected,
            "hands_count": hands_count,
        }

        return feature_vector, info, annotated_frame

    def close(self) -> None:
        """Release MediaPipe resources."""
        if hasattr(self, "hands") and self.hands:
            self.hands.close()

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
