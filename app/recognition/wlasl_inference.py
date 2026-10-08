"""WLASL-100 Pretrained Sign Language Inference Engine.

Extracts 55 keypoints (13 upper body + 21 left hand + 21 right hand)
over a 50-frame buffer and classifies real ASL signs using the pretrained TGCN model.
"""

import os
import json
import time
from typing import Dict, List, Optional, Any, Tuple
import cv2
import numpy as np
import torch
import mediapipe as mp

from app.recognition.wlasl_model import WLASLTGCN


class MediaPipeHolisticExtractor:
    """Extracts 55 keypoints per frame (13 upper body + 21 left hand + 21 right hand)."""

    # 13 upper body landmark indices from MediaPipe Pose (33 points)
    # Corresponding to: [Nose, L_Shoulder, R_Shoulder, L_Elbow, R_Elbow, L_Wrist, R_Wrist,
    #                   L_Hip, R_Hip, L_Eye, R_Eye, L_Ear, R_Ear]
    POSE_UPPER_BODY_INDICES = [0, 11, 12, 13, 14, 15, 16, 23, 24, 2, 5, 7, 8]

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            smooth_landmarks=True,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def extract(self, frame_bgr: np.ndarray, draw: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """Extracts (55, 2) keypoints from a single frame.

        Returns:
            keypoints_55x2: np.ndarray of shape (55, 2) normalized to [-1, 1].
            annotated_frame: frame with skeletal landmarks drawn (if draw=True).
        """
        if frame_bgr is None or frame_bgr.size == 0:
            return np.zeros((55, 2), dtype=np.float32), frame_bgr

        annotated_frame = frame_bgr.copy() if draw else frame_bgr
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(frame_rgb)

        keypoints = np.zeros((55, 2), dtype=np.float32)

        # 1. Upper Body Pose (13 points -> indices 0..12)
        if results.pose_landmarks:
            for out_idx, mp_idx in enumerate(self.POSE_UPPER_BODY_INDICES):
                lm = results.pose_landmarks.landmark[mp_idx]
                # Center around 0: [-1.0, 1.0]
                keypoints[out_idx, 0] = (lm.x - 0.5) * 2.0
                keypoints[out_idx, 1] = (lm.y - 0.5) * 2.0

            if draw and self.mp_drawing:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.pose_landmarks,
                    self.mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style(),
                )

        # 2. Left Hand (21 points -> indices 13..33)
        if results.left_hand_landmarks:
            for idx, lm in enumerate(results.left_hand_landmarks.landmark):
                keypoints[13 + idx, 0] = (lm.x - 0.5) * 2.0
                keypoints[13 + idx, 1] = (lm.y - 0.5) * 2.0

            if draw and self.mp_drawing:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.left_hand_landmarks,
                    self.mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_hand_landmarks_style(),
                )

        # 3. Right Hand (21 points -> indices 34..54)
        if results.right_hand_landmarks:
            for idx, lm in enumerate(results.right_hand_landmarks.landmark):
                keypoints[34 + idx, 0] = (lm.x - 0.5) * 2.0
                keypoints[34 + idx, 1] = (lm.y - 0.5) * 2.0

            if draw and self.mp_drawing:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    results.right_hand_landmarks,
                    self.mp_holistic.HAND_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_hand_landmarks_style(),
                )

        return keypoints, annotated_frame

    def close(self):
        if self.holistic:
            self.holistic.close()


class WLASLInference:
    """Pretrained WLASL-100 TGCN inference engine."""

    def __init__(
        self,
        weights_path: Optional[str] = None,
        labels_path: Optional[str] = None,
        num_frames: int = 50,
        device: Optional[str] = None,
    ):
        base_dir = os.path.dirname(__file__)
        if weights_path is None:
            weights_path = os.path.abspath(
                os.path.join(base_dir, "..", "..", "models", "wlasl100_tgcn.pth")
            )
        if labels_path is None:
            labels_path = os.path.abspath(
                os.path.join(base_dir, "..", "..", "models", "wlasl100_labels.json")
            )

        self.weights_path = weights_path
        self.labels_path = labels_path
        self.num_frames = num_frames

        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # Load labels mapping
        if not os.path.exists(self.labels_path):
            raise FileNotFoundError(f"Labels file not found at {self.labels_path}")
        with open(self.labels_path, "r") as f:
            self.id_to_label = json.load(f)

        self.num_classes = len(self.id_to_label)

        # Initialize and load model
        self.model = WLASLTGCN(
            input_feature=self.num_frames * 2,
            hidden_feature=64,
            num_class=self.num_classes,
            p_dropout=0.0,
            num_stage=20,
        ).to(self.device)

        if not os.path.exists(self.weights_path):
            print(f"Weights not found at {self.weights_path}. Downloading from Hugging Face...")
            os.makedirs(os.path.dirname(self.weights_path), exist_ok=True)
            import urllib.request
            url = "https://huggingface.co/sharonn18/tgcn-wlasl/resolve/main/checkpoints/asl100/pytorch_model.bin"
            urllib.request.urlretrieve(url, self.weights_path)
            print("Download completed successfully!")

        checkpoint = torch.load(self.weights_path, map_location=self.device)
        state_dict = checkpoint.get("state_dict", checkpoint)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict_sequence(self, sequence: np.ndarray) -> Dict[str, Any]:
        """Predicts sign word from a sequence of 55-keypoint frames.

        Args:
            sequence: Numpy array of shape (50, 55, 2) or (num_frames, 55, 2).

        Returns:
            dict containing top-1 label, confidence, and top-5 alternatives.
        """
        # Resample or pad if sequence length != self.num_frames
        seq_len = len(sequence)
        if seq_len != self.num_frames:
            indices = np.linspace(0, seq_len - 1, self.num_frames, dtype=int)
            sequence = sequence[indices]

        # Convert (50, 55, 2) to input shape (1, 55, 100)
        # Transpose to (55, 50, 2) then flatten last two dims to 100
        tensor_in = torch.tensor(sequence, dtype=torch.float32)  # (50, 55, 2)
        tensor_in = tensor_in.permute(1, 0, 2).reshape(1, 55, self.num_frames * 2)  # (1, 55, 100)
        tensor_in = tensor_in.to(self.device)

        with torch.no_grad():
            logits = self.model(tensor_in)
            probabilities = torch.softmax(logits, dim=1)[0]

            # Top-5 predictions
            top5_conf, top5_idx = torch.topk(probabilities, 5)

            top5_results = []
            for conf, idx in zip(top5_conf, top5_idx):
                idx_str = str(idx.item())
                top5_results.append({
                    "label": self.id_to_label.get(idx_str, "unknown"),
                    "confidence": float(conf.item()),
                })

            top_label = top5_results[0]["label"]
            top_conf = top5_results[0]["confidence"]

        return {
            "label": top_label,
            "confidence": top_conf,
            "top_5": top5_results,
            "timestamp": time.time(),
        }
