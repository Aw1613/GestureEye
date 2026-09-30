# SignBridge — Data Contracts

> **Purpose:** This file is the single source of truth for all data shapes,
> schemas, and interface formats shared between agents.
>
> **Rule:** No agent may silently change a contract defined here.
> If a contract must change, update this file first, notify the team,
> and update all affected consumers.

---

## 1. Configuration Constants

These values are used across multiple agents. They must remain consistent
between training and inference.

```
SEQUENCE_LENGTH       = 30       # number of frames per temporal window
LANDMARKS_PER_HAND    = 21       # MediaPipe Hands outputs 21 landmarks
COORDS_PER_LANDMARK   = 3        # x, y, z per landmark
NUM_HANDS             = 2        # left + right
FEATURE_DIM           = 126      # 2 hands * 21 landmarks * 3 coords
NUM_CLASSES           = 20-30    # exact count set after vocabulary selection
CONFIDENCE_THRESHOLD  = 0.60     # minimum confidence to accept a prediction
STABILITY_WINDOW      = 5        # consecutive agreeing predictions before accept
```

---

## 2. Contract A — Per-Frame Feature Vector

Owner: Agent 1 (Keypoint Extraction + Preprocessing)
Consumer: Agent 1 (Sequence Buffer), Agent 2 (Model)

### Landmark Ordering

Each hand produces 21 landmarks in MediaPipe Hands order (WRIST, THUMB_CMC,
THUMB_MCP, THUMB_IP, THUMB_TIP, INDEX_FINGER_MCP, ... , PINKY_TIP).

Full frame vector layout:

```
[ left_hand_landmark_0_x,
  left_hand_landmark_0_y,
  left_hand_landmark_0_z,
  left_hand_landmark_1_x,
  ...
  left_hand_landmark_20_z,
  right_hand_landmark_0_x,
  ...
  right_hand_landmark_20_z ]
```

Total length: 126 floats per frame.

### Missing-Hand Representation

If only one hand is detected, the missing hand's 63 values are filled with 0.0.
If no hands are detected, the entire 126-value vector is filled with 0.0.

### Normalization

Coordinates are normalized relative to the wrist landmark of each hand:
- Subtract the wrist (x, y, z) from all landmarks of that hand.
- Scale so the maximum absolute coordinate value across the hand equals 1.0.
- This makes the features translation-invariant and scale-invariant.

### Output Type

```
numpy array, dtype float32, shape (126,)
```

---

## 3. Contract B — Temporal Sequence Window

Owner: Agent 1 (Sequence Buffer)
Consumer: Agent 2 (Model Inference)

### Shape

```
numpy array, dtype float32, shape (SEQUENCE_LENGTH, FEATURE_DIM)
                                   (30, 126)
```

### Behavior

The buffer is a sliding window of the most recent SEQUENCE_LENGTH frames.
When a new frame arrives, the oldest frame is removed and the new frame is
appended.

### Readiness Rule

The sequence is only passed to the model when the buffer contains exactly
SEQUENCE_LENGTH frames. Until then, no prediction is made.

---

## 4. Contract C — Model Prediction Output

Owner: Agent 2 (Model / Inference Wrapper)
Consumer: Agent 3 (Prediction Filter)

### Schema

```json
{
  "label": "thank_you",
  "confidence": 0.91,
  "timestamp": 1727634567.123
}
```

### Field Definitions

- label (string): The predicted sign class from the vocabulary.
- confidence (float): Model confidence in range [0.0, 1.0].
- timestamp (float): Unix timestamp of the prediction.

### Output Type

Python dictionary with the above keys.

---

## 5. Contract D — Stable Sign Event

Owner: Agent 3 (Prediction Filter + Segmentation)
Consumer: Agent 3 (Word Buffer), Agent 4 (UI)

### Schema

```json
{
  "word": "hello",
  "confidence": 0.88,
  "start_time": 1727634567.0,
  "end_time": 1727634568.5
}
```

### Field Definitions

- word (string): The accepted sign label after stability filtering.
- confidence (float): Average confidence over the stability window.
- start_time (float): Unix timestamp when the stable prediction began.
- end_time (float): Unix timestamp when the sign was finalized.

### Stability Rule

A prediction becomes a stable sign event only after STABILITY_WINDOW
consecutive predictions agree on the same label, each with confidence
above CONFIDENCE_THRESHOLD.

---

## 6. Contract E — Sentence Object

Owner: Agent 3 (Sentence Builder)
Consumer: Agent 4 (UI), Agent 3 (TTS)

### Schema

```json
{
  "words": ["hello", "thank_you", "water"],
  "text": "Hello, thank you for the water."
}
```

### Field Definitions

- words (list of strings): Ordered list of accepted sign labels.
- text (string): Human-readable smoothed sentence.

---

## 7. Contract F — TTS Input

Owner: Agent 3 (TTS)
Consumer: Internal to Agent 3

### Schema

```json
{
  "text": "Hello, thank you for the water."
}
```

### Runtime Rule

TTS must run in a non-blocking manner (separate thread or queue) so that
it does not freeze the camera capture or model inference loop.

---

## 8. Contract G — UI State Object

Owner: Agent 4 (UI)
Consumer: Internal to Agent 4

### Schema

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

### Field Definitions

- current_sign (string or null): Latest predicted sign label.
- confidence (float): Confidence of the current prediction.
- recognized_words (list of strings): All accepted words so far.
- sentence (string): Current smoothed sentence.
- status (object): Health status of each subsystem (true = operational).

---

## 9. Vocabulary

The exact vocabulary will be selected by Agent 2 (Member 2) during
dataset inspection. Once selected, the label list must be recorded here.

### Format

```
VOCABULARY = [
    "hello",
    "thank_you",
    "please",
    "water",
    "help",
    ...
]
```

Status: NOT YET SELECTED — to be filled by Agent 2 after dataset inspection.

---

## 10. Model File Format

Owner: Agent 2
Consumer: Agent 2 (Inference Wrapper)

### Saved Artifacts

- Model weights file: models/sign_model.pth (PyTorch) or models/sign_model.h5 (Keras)
- Label mapping file: models/labels.json

### labels.json Format

```json
{
  "0": "hello",
  "1": "thank_you",
  "2": "please",
  ...
}
```

---

## 11. Contract Change Log

| Date | Contract | Change | Changed By |
|------|----------|--------|------------|
| 2026-09-30 | All | Initial contract definitions | Phase 0 setup |
