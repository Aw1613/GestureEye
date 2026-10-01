"""
Prediction Filter Module (Agent 3 - Milestone M3)
Implements temporal stability filtering, confidence thresholding,
and duplicate suppression to convert raw model predictions (Contract C)
into stable sign events (Contract D).
"""

import time
from typing import Optional, Dict, Any, List
from app.sentence.segmentation import SignSegmenter


class PredictionFilter:
    """
    Filters raw model predictions to require consecutive agreeing predictions
    above a confidence threshold before accepting a sign.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.60,
        stability_window: int = 5,
        pause_threshold_frames: int = 5
    ):
        """
        Args:
            confidence_threshold: Minimum confidence required per frame (default: 0.60).
            stability_window: Number of consecutive agreeing predictions required (default: 5).
            pause_threshold_frames: Number of idle/low-confidence frames to trigger a pause
                                   and clear the duplicate lock for repeated signs (default: 5).
        """
        self.confidence_threshold = confidence_threshold
        self.stability_window = stability_window
        self.segmenter = SignSegmenter(
            pause_threshold_frames=pause_threshold_frames,
            min_confidence=confidence_threshold
        )

        # Internal state
        self.current_candidate: Optional[str] = None
        self.consecutive_count: int = 0
        self.window_confidences: List[float] = []
        self.candidate_start_time: Optional[float] = None
        self.candidate_end_time: Optional[float] = None

        self.last_accepted_word: Optional[str] = None
        self.accepted_emitted: bool = False

    def process_prediction(self, prediction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a single prediction event conforming to Contract C:
            {"label": "hello", "confidence": 0.85, "timestamp": 1727721.4}

        Returns:
            Stable sign event dict conforming to Contract D if accepted, else None:
            {
                "word": "hello",
                "confidence": 0.88,
                "start_time": 1727634567.0,
                "end_time": 1727634568.5
            }
        """
        if not isinstance(prediction, dict):
            return None

        label = prediction.get("label")
        raw_confidence = prediction.get("confidence", 0.0)
        try:
            confidence = float(raw_confidence)
        except (ValueError, TypeError):
            confidence = 0.0

        timestamp = float(prediction.get("timestamp", time.time()))

        # Update segmentation heuristic
        seg_info = self.segmenter.update(prediction)

        # If a pause was detected, reset duplicate lock so the same word can be re-signed
        if seg_info["pause_detected"]:
            self.last_accepted_word = None

        # Check confidence threshold
        if confidence < self.confidence_threshold or label in (None, "", "unknown"):
            # Low confidence resets the current stability run
            self._reset_candidate()
            return None

        # Check candidate consistency
        if label == self.current_candidate:
            self.consecutive_count += 1
            self.window_confidences.append(confidence)
            self.candidate_end_time = timestamp
        else:
            # New candidate label encountered
            self.current_candidate = label
            self.consecutive_count = 1
            self.window_confidences = [confidence]
            self.candidate_start_time = timestamp
            self.candidate_end_time = timestamp
            self.accepted_emitted = False

        # Check if stability window reached
        if self.consecutive_count >= self.stability_window:
            # Check duplicate suppression: don't re-emit if already accepted consecutively
            if not self.accepted_emitted and self.current_candidate != self.last_accepted_word:
                # Calculate average confidence over stability window
                avg_confidence = float(
                    sum(self.window_confidences[-self.stability_window:]) / self.stability_window
                )

                event = {
                    "word": self.current_candidate,
                    "confidence": round(avg_confidence, 4),
                    "start_time": self.candidate_start_time,
                    "end_time": self.candidate_end_time
                }

                self.last_accepted_word = self.current_candidate
                self.accepted_emitted = True
                return event

        return None

    def add_prediction(self, prediction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Alias for process_prediction."""
        return self.process_prediction(prediction)

    def _reset_candidate(self):
        """Reset the current candidate window tracking."""
        self.current_candidate = None
        self.consecutive_count = 0
        self.window_confidences = []
        self.candidate_start_time = None
        self.candidate_end_time = None
        self.accepted_emitted = False

    def reset(self):
        """Full reset of filter state."""
        self._reset_candidate()
        self.last_accepted_word = None
        self.segmenter.reset()

    def get_status(self) -> Dict[str, Any]:
        """Return diagnostic status of the filter."""
        return {
            "current_candidate": self.current_candidate,
            "consecutive_count": self.consecutive_count,
            "stability_window": self.stability_window,
            "confidence_threshold": self.confidence_threshold,
            "last_accepted_word": self.last_accepted_word,
            "accepted_emitted": self.accepted_emitted,
            "in_pause": self.segmenter.consecutive_idle_frames >= self.segmenter.pause_threshold_frames
        }
