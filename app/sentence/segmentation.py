"""
Sign Segmentation Module (Agent 3 - Milestone M3)
Implements temporal heuristics to detect sign boundaries and transitions.
"""

import time
from typing import Optional, Dict, Any


class SignSegmenter:
    """
    Heuristic segmenter that tracks frame-to-frame sign states,
    detects transitions between signs, and identifies pauses/cooldowns.
    """

    def __init__(self, pause_threshold_frames: int = 5, min_confidence: float = 0.60):
        """
        Args:
            pause_threshold_frames: Number of consecutive low-confidence/neutral frames
                                    required to consider a sign fully ended (pause/rest).
            min_confidence: Threshold above which a frame is considered an active sign.
        """
        self.pause_threshold_frames = pause_threshold_frames
        self.min_confidence = min_confidence

        self.consecutive_idle_frames = 0
        self.last_active_label: Optional[str] = None
        self.in_sign = False
        self.sign_start_time: Optional[float] = None
        self.sign_end_time: Optional[float] = None

    def update(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the segmentation state with the latest prediction.

        Args:
            prediction: Dict with 'label', 'confidence', and optional 'timestamp'.

        Returns:
            Dict containing segmentation status:
                - is_active_sign (bool): True if current frame has high confidence.
                - sign_transition (bool): True if sign changed from previous active sign.
                - pause_detected (bool): True if a pause/rest boundary is established.
                - active_label (str or None): Currently detected label if active.
        """
        label = prediction.get("label")
        confidence = float(prediction.get("confidence", 0.0))
        timestamp = float(prediction.get("timestamp", time.time()))

        is_active = confidence >= self.min_confidence and label not in (None, "", "unknown")
        sign_transition = False
        pause_detected = False

        if is_active:
            self.consecutive_idle_frames = 0
            if not self.in_sign:
                self.in_sign = True
                self.sign_start_time = timestamp

            if self.last_active_label is not None and self.last_active_label != label:
                sign_transition = True

            self.last_active_label = label
            self.sign_end_time = timestamp
        else:
            self.consecutive_idle_frames += 1
            if self.in_sign and self.consecutive_idle_frames >= self.pause_threshold_frames:
                self.in_sign = False
                pause_detected = True

        return {
            "is_active_sign": is_active,
            "sign_transition": sign_transition,
            "pause_detected": pause_detected,
            "active_label": label if is_active else None,
            "consecutive_idle_frames": self.consecutive_idle_frames
        }

    def reset(self):
        """Reset segmenter internal state."""
        self.consecutive_idle_frames = 0
        self.last_active_label = None
        self.in_sign = False
        self.sign_start_time = None
        self.sign_end_time = None
