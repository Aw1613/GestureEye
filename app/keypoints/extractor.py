"""MediaPipe Hand Landmark Extraction Module for SignBridge (Agent 1).

Uses the modern MediaPipe Tasks API.
Extracts 21 3D landmarks per detected hand (up to 2 hands) and returns
a standardized 126-dimensional normalized feature vector conforming to CONTRACTS.md.
"""

import os
from typing import Dict, Optional, Tuple, Any
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from app.keypoints.preprocessing import (
    LANDMARKS_PER_HAND,
    COORDS_PER_LANDMARK,
    FEATURE_DIM,
    assemble_feature_vector,
)


class HandKeypointExtractor:
    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        model_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "hand_landmarker.task"
        )
        
        if not os.path.exists(model_path):
            print(f"Error: Could not find model at {model_path}")
            self.detector = None
            return

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_num_hands,
            min_hand_detection_confidence=min_detection_confidence,
            min_hand_presence_confidence=min_tracking_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # Drawing utilities for visualization
        self.mp_drawing = mp.solutions.drawing_utils if hasattr(mp, "solutions") else None
        self.mp_hands = mp.solutions.hands if hasattr(mp, "solutions") else None

    def extract_keypoints(
        self, frame: np.ndarray, draw: bool = False
    ) -> Tuple[np.ndarray, Dict[str, Any], np.ndarray]:
        
        if frame is None or frame.size == 0 or self.detector is None:
            return np.zeros(FEATURE_DIM, dtype=np.float32), {"left_detected": False, "right_detected": False, "hands_count": 0}, frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = self.detector.detect(mp_image)
        annotated_frame = frame.copy() if draw else frame
        
        left_hand, right_hand = None, None
        left_detected, right_detected = False, False
        hands_count = 0

        if detection_result.hand_landmarks:
            hands_count = len(detection_result.hand_landmarks)
            for idx in range(hands_count):
                hand_landmarks = detection_result.hand_landmarks[idx]
                handedness = detection_result.handedness[idx][0].category_name
                
                coords = np.array(
                    [[lm.x, lm.y, lm.z] for lm in hand_landmarks],
                    dtype=np.float32,
                )
                
                if handedness == "Left" and not left_detected:
                    left_hand = coords
                    left_detected = True
                elif handedness == "Right" and not right_detected:
                    right_hand = coords
                    right_detected = True
                elif not left_detected:
                    left_hand = coords
                    left_detected = True
                elif not right_detected:
                    right_hand = coords
                    right_detected = True
                
                # Manual drawing since new API doesn't have a direct draw method that matches old styles perfectly
                if draw:
                    for lm in hand_landmarks:
                        x = int(lm.x * frame.shape[1])
                        y = int(lm.y * frame.shape[0])
                        cv2.circle(annotated_frame, (x, y), 5, (0, 255, 0), -1)

        feature_vector = assemble_feature_vector(left_hand, right_hand)
        info = {
            "left_detected": left_detected,
            "right_detected": right_detected,
            "hands_count": hands_count,
        }
        return feature_vector, info, annotated_frame

    def close(self) -> None:
        if self.detector:
            self.detector.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
