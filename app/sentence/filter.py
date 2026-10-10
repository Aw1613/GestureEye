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
        pause_threshold_frames: int = 5,
        timing_gap: float = 0.0
    ):
        """
        Args:
            confidence_threshold: Minimum confidence required per frame (default: 0.60).
            stability_window: Number of consecutive agreeing predictions required (default: 5).
            pause_threshold_frames: Number of idle/low-confidence frames to trigger a pause
                                   and clear the duplicate lock for repeated signs (default: 5).
            timing_gap: Minimum time in seconds between fetching/accepting consecutive signs (default: 0.0).
        """
        self.confidence_threshold = confidence_threshold
        self.stability_window = stability_window
        self.timing_gap = timing_gap
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
        self.last_fetch_time: Optional[float] = None
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
                # Check timing gap between two signs to fetch
                if self.last_fetch_time is not None and self.timing_gap > 0.0:
                    if (timestamp - self.last_fetch_time) < self.timing_gap:
                        # Inside timing gap: do not enter fetch mode
                        return None

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
                self.last_fetch_time = timestamp
                self.accepted_emitted = True
                return event

        return None

    def add_prediction(self, prediction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Alias for process_prediction."""
        return self.process_prediction(prediction)

    def is_in_fetch_mode(self, current_time: Optional[float] = None) -> bool:
        """Check if the timing gap has elapsed since the last fetched sign."""
        if self.last_fetch_time is None or self.timing_gap <= 0.0:
            return True
        now = time.time() if current_time is None else current_time
        return (now - self.last_fetch_time) >= self.timing_gap

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
        self.last_fetch_time = None
        self.segmenter.reset()

    def get_status(self) -> Dict[str, Any]:
        """Return diagnostic status of the filter."""
        in_gap = False
        if self.last_fetch_time is not None and self.timing_gap > 0.0:
            in_gap = (time.time() - self.last_fetch_time) < self.timing_gap

        return {
            "current_candidate": self.current_candidate,
            "consecutive_count": self.consecutive_count,
            "stability_window": self.stability_window,
            "confidence_threshold": self.confidence_threshold,
            "last_accepted_word": self.last_accepted_word,
            "last_fetch_time": self.last_fetch_time,
            "timing_gap": self.timing_gap,
            "in_timing_gap": in_gap,
            "fetch_mode": not in_gap,
            "accepted_emitted": self.accepted_emitted,
            "in_pause": self.segmenter.consecutive_idle_frames >= self.segmenter.pause_threshold_frames
        }
