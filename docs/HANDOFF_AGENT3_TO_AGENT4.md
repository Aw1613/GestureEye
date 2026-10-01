# 🤝 SignBridge — Handoff from Agent 3 (Logic & Speech) to Agent 4 (UI & Integration)

> **Document Type:** Official Handoff Specification  
> **Source Module:** Agent 3 (`app/sentence/`, `app/tts/`)  
> **Target Module:** Agent 4 (`app/ui/app.py`, live integration)  
> **Status:** Milestone M3 COMPLETE $\rightarrow$ Milestone M4 READY  
> **Base Branch:** `main` (latest commit contains all M1, M2, and M3 deliverables)  

---

## 1. Executive Summary

Agent 3 has completed the **Temporal Stability Filtering**, **Word Buffering**, **Heuristic Sentence Smoothing**, and **Asynchronous Non-Blocking Text-to-Speech** modules.

All implementations strictly adhere to `CONTRACTS.md`, backed by 19 passing unit and integration tests.

### What Agent 4 Receives:
1. **Prediction Filter (`app.sentence.PredictionFilter`)**: Converts noisy raw predictions into stable sign events (**Contract D**).
2. **Sentence Builder (`app.sentence.SentenceBuilder`)**: Manages word sequence and produces human-readable smoothed sentences (**Contract E**).
3. **Text-to-Speech Engine (`app.tts.TextToSpeech`)**: Speaks sentences in a background daemon thread in $< 0.001\text{s}$ non-blocking time without freezing camera capture or model inference (**Contract F**).
4. **Sign Segmenter (`app.sentence.SignSegmenter`)**: Tracks sign boundaries, transitions, and pause/rest states.

---

## 2. Python Imports

Agent 4 can import all Agent 3 components cleanly:

```python
# Sentence Logic (Contract D & E)
from app.sentence import PredictionFilter, SentenceBuilder, SignSegmenter

# Text-to-Speech (Contract F)
from app.tts import TextToSpeech
```

---

## 3. Data Contracts Handed Over to Agent 4

```text
 Agent 2                     Agent 3                            Agent 4
┌──────────────┐   Contract C    ┌───────────────────┐  Contract D   ┌───────────────┐
│ Model        │ ──────────────► │ PredictionFilter  │ ────────────► │ Live UI       │
│ Inference    │                 └─────────┬─────────┘               │ Overlay       │
└──────────────┘                           │                         └───────────────┘
                                           ▼
                                 ┌───────────────────┐  Contract E   ┌───────────────┐
                                 │ SentenceBuilder   │ ────────────► │ Sentence View │
                                 └─────────┬─────────┘               └───────────────┘
                                           │
                                           ▼ Contract F
                                 ┌───────────────────┐
                                 │ TextToSpeech      │ ────────────► 🔊 Audio Output
                                 └───────────────────┘
```

### 3.1 Input from Agent 2 — Contract C (Model Prediction)
Passed frame-by-frame from Agent 2 (`ModelInference.predict(sequence)`):
```json
{
  "label": "thank_you",
  "confidence": 0.91,
  "timestamp": 1727634567.123
}
```

### 3.2 Output to Agent 4 — Contract D (Stable Sign Event)
Emitted by `PredictionFilter.process_prediction()` only after **5 consecutive agreeing frames** $\ge 0.60$ confidence:
```json
{
  "word": "thank_you",
  "confidence": 0.91,
  "start_time": 1727634567.0,
  "end_time": 1727634568.5
}
```
*Note: Returns `None` during unstable, low-confidence ($< 0.60$), or duplicate held frames.*

### 3.3 Output to Agent 4 — Contract E (Sentence Object)
Emitted by `SentenceBuilder.add_word(stable_sign)` or `SentenceBuilder.build_sentence()`:
```json
{
  "words": ["hello", "thank_you", "water"],
  "text": "Hello, thank you for the water."
}
```

### 3.4 Target UI Object — Contract G (UI State Object)
Agent 4 combines all subsystem states into this contract for the display:
```json
{
  "current_sign": "thank_you",
  "confidence": 0.91,
  "recognized_words": ["hello", "thank_you", "water"],
  "sentence": "Hello, thank you for the water.",
  "status": {
    "camera": true,
    "model": true,
    "speech": true
  }
}
```

---

## 4. API Reference for Agent 4

### 4.1 `PredictionFilter` (`app/sentence/filter.py`)
```python
filter_engine = PredictionFilter(
    confidence_threshold=0.60,      # minimum confidence per frame (default: 0.60)
    stability_window=5,             # consecutive matching frames required (default: 5)
    pause_threshold_frames=5        # idle frames before resetting duplicate lock (default: 5)
)
```

- **`process_prediction(prediction: dict) -> Optional[dict]`**
  - Accepts Contract C dictionary.
  - Returns Contract D dictionary when a sign stabilizes; returns `None` otherwise.
- **`add_prediction(prediction: dict) -> Optional[dict]`**
  - Alias for `process_prediction()`.
- **`reset()`**
  - Clears candidate stability count and accepted word state.
- **`get_status() -> dict`**
  - Returns diagnostics: `{"current_candidate": str, "consecutive_count": int, "last_accepted_word": str, "in_pause": bool}`.

### 4.2 `SentenceBuilder` (`app/sentence/builder.py`)
```python
builder = SentenceBuilder(suppress_consecutive_duplicates=True)
```

- **`add_word(word_item: Union[str, dict]) -> dict`**
  - Accepts either a label string (e.g. `"water"`) or a Contract D event dict.
  - Returns updated Contract E object: `{"words": [...], "text": "..."}`.
- **`get_words() -> list[str]`**
  - Returns copy of current ordered word list.
- **`get_sentence() -> str`**
  - Returns smoothed sentence string.
- **`build_sentence() -> dict`**
  - Returns current Contract E dictionary without modifying buffer.
- **`remove_last_word() -> Optional[str]`**
  - Backspace feature: deletes the last word from the buffer and recalculates the smoothed sentence.
- **`clear()` / `reset()`**
  - Wipes the word buffer.
- **`finalize_sentence() -> dict`**
  - Returns final Contract E object and clears the buffer for the next utterance.

### 4.3 `TextToSpeech` (`app/tts/speech.py`)
```python
tts = TextToSpeech(rate=160, volume=1.0, enabled=True)
```

- **`speak(text: str) -> bool`**
  - Non-blocking. Queues string to background worker thread. Returns in $< 0.001\text{s}$.
- **`speak_sentence(sentence_data: Union[str, dict]) -> bool`**
  - Non-blocking. Accepts string or Contract E/F dict `{"text": "..."}`.
- **`is_busy() -> bool`**
  - Returns `True` if currently speaking or audio queue is non-empty. Use for UI microphone/speaker animation.
- **`is_available() -> bool`**
  - Returns `True` if pyttsx3 SAPI5 engine is functional.
- **`stop()`**
  - Immediately drains the queue and stops current utterance.
- **`shutdown(timeout=2.0)`**
  - Cleanly shuts down worker thread on application exit.

---

## 5. Ready-to-Use Agent 4 Integration Template

Agent 4 can drop this logic directly into `app/ui/app.py`:

```python
import time
import cv2
import numpy as np

# Agent 1
from app.capture.camera import CameraCapture
from app.keypoints.extractor import HandKeypointExtractor
from app.keypoints.preprocessing import KeypointPreprocessor
from app.keypoints.buffer import SequenceBuffer

# Agent 2
from app.recognition.inference import ModelInference

# Agent 3
from app.sentence import PredictionFilter, SentenceBuilder
from app.tts import TextToSpeech

def run_app():
    # 1. Initialize Pipeline
    camera = CameraCapture(mock=False)      # Set mock=True if no webcam connected
    extractor = HandKeypointExtractor()
    preprocessor = KeypointPreprocessor()
    seq_buffer = SequenceBuffer(sequence_length=30, feature_dim=126)

    model = ModelInference(model_path="models/sign_model.pth", labels_path="models/labels.json")
    pred_filter = PredictionFilter(confidence_threshold=0.60, stability_window=5)
    sentence_builder = SentenceBuilder()
    tts = TextToSpeech(enabled=True)

    camera.start()

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                continue

            # Stage 1: Keypoints (Agent 1)
            raw_keypoints = extractor.extract(frame)
            norm_keypoints = preprocessor.normalize(raw_keypoints)
            seq_buffer.add_frame(norm_keypoints)

            # Stage 2: Inference when buffer full (Agent 2)
            current_sign = None
            confidence = 0.0
            if seq_buffer.is_ready():
                prediction = model.predict(seq_buffer.get_sequence()) # Contract C
                current_sign = prediction["label"]
                confidence = prediction["confidence"]

                # Stage 3: Temporal Stability & Sentence Logic (Agent 3)
                stable_event = pred_filter.process_prediction(prediction) # Contract D
                if stable_event:
                    sentence_builder.add_word(stable_event) # Contract E

            # Contract G UI State Object
            ui_state = {
                "current_sign": current_sign,
                "confidence": confidence,
                "recognized_words": sentence_builder.get_words(),
                "sentence": sentence_builder.get_sentence(),
                "status": {
                    "camera": camera.is_opened(),
                    "model": True,
                    "speech": tts.is_available()
                }
            }

            # Agent 4: Render UI overlay here
            # e.g., draw ui_state on frame and cv2.imshow("SignBridge Live", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):  # 's' to Speak
                tts.speak_sentence(sentence_builder.build_sentence())
            elif key == ord('c'):  # 'c' to Clear
                sentence_builder.clear()
                pred_filter.reset()
            elif key == ord('\b'): # Backspace to delete last word
                sentence_builder.remove_last_word()

    finally:
        camera.release()
        tts.shutdown()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_app()
```

---

## 6. Edge Cases Handled for Agent 4

1. **Camera Won't Freeze on Speech:**
   TTS uses a background queue. `tts.speak_sentence()` returns in $\approx 0.0001\text{s}$.
2. **Resting Hands / Neutral Frame:**
   When hands are lowered, `confidence < 0.60`. The filter pauses and resets the duplicate lock so signing the same sign again is registered correctly.
3. **Holding Signs:**
   If a user holds a sign for 30 consecutive frames, `PredictionFilter` emits the event once at frame 5 and suppresses frames 6–30.
4. **Audio Failures Won't Crash UI:**
   If no audio card or Windows SAPI5 voice is configured, `TextToSpeech` gracefully logs a warning and operates silently without throwing uncaught exceptions.
5. **UI Backspace & Clear Support:**
   `sentence_builder.remove_last_word()` and `sentence_builder.clear()` are thread-safe and immediately update the smoothed text.

---

## 7. Verification Commands for Agent 4

Agent 4 can verify the subsystem before building UI components:

```bash
# Run all 19 Agent 3 unit & integration tests:
python -m pytest tests/test_filter.py tests/test_builder.py tests/test_speech.py tests/test_sentence_speech_integration.py -v

# Run the live terminal & audio demo:
python scripts/demo_agent3.py
```
