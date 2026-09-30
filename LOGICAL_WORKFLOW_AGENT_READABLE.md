# Real-Time Sign Language Translator — Logical Workflow

> **Document type:** Authoritative logical workflow for the Real-Time Sign Language Translator MVP.
>
> **AI-agent readability:** This document is intentionally structured so an AI coding agent, including an Antigravity-style agent, can parse the workflow, ownership, inputs, outputs, dependencies, validation rules, and MVP limitations without relying on visual arrows or implicit assumptions.
>
> **Important:** Do not invent missing interfaces or silently change the workflow. When an exact data shape is required, it must be documented in `CONTRACTS.md`.

---

## 1. System Objective

The system accepts a supported sign performed in front of a webcam and processes it through:

```text
USER INPUT
→ CAMERA / FRAME CAPTURE
→ KEYPOINT EXTRACTION
→ PREPROCESSING / NORMALIZATION
→ ROLLING SEQUENCE BUFFER
→ TEMPORAL MODEL
→ TEMPORAL STABILITY / PREDICTION FILTER
→ SIGN SEGMENTATION
→ WORD BUFFER
→ BASIC SENTENCE SMOOTHING
→ TEXT DISPLAY
→ TEXT-TO-SPEECH
→ LIVE UI / DEMO
```

The final MVP result is:

```text
Supported sign/short sequence
→ recognized sign
→ displayed word/sentence
→ spoken output
```

---

# 2. Workflow Contract

## 2.1 Primary Data Flow

```text
Live Video Frames
    ↓
Per-Frame Hand Keypoints
    ↓
Normalized Feature Vectors
    ↓
Temporal Sequence Window
    ↓
Sign Class + Confidence
    ↓
Stable Sign Event
    ↓
Accepted Word/Sign
    ↓
Ordered Word Buffer
    ↓
Smoothed Sentence
    ↓
Text + Speech
```

## 2.2 Ownership Map

| Stage | Owner |
|---|---|
| User Input | System input |
| Camera / Frame Capture | Agent 1 |
| Keypoint Extraction | Agent 1 |
| Preprocessing / Normalization | Agent 1 |
| Rolling Sequence Buffer | Agent 1 + Agent 2 interface |
| Temporal Model | Agent 2 |
| Temporal Stability / Prediction Filter | Agent 3 |
| Sign Segmentation | Agent 3 |
| Word Buffer | Agent 3 |
| Basic Sentence Smoothing | Agent 3 |
| Text Display | Agent 4 |
| Text-to-Speech | Agent 3 |
| Live UI / Demo | Agent 4 |

---

# 3. Stage 1 — User Input

## Owner

System input.

## Input

- Live video frames from the webcam.

## Behavior

A person performs a supported sign in front of the webcam.

## Output

```text
Live video frames
```

---

# 4. Stage 2 — Camera / Frame Capture

## Owner

**Agent 1**

## Purpose

Continuously read frames from the webcam.

## Input

```text
Webcam stream
```

## Processing

The application continuously captures individual frames.

## Output

```text
Individual video frames
```

## Validation Criteria

- [ ] Camera opens.
- [ ] Frames arrive continuously.
- [ ] Frame rate is acceptable.

## Handoff

Frames are passed to **Keypoint Extraction**.

---

# 5. Stage 3 — Keypoint Extraction

## Owner

**Agent 1**

## Purpose

Extract hand landmarks from each video frame.

## Technology

**MediaPipe Hands**

## MVP Requirement

- **21 landmarks per detected hand**
- Face and pose landmarks are optional extensions.
- Face/pose landmarks are **not required for the first MVP**.

## Input

```text
Individual video frame
```

## Processing

MediaPipe extracts landmarks from the detected hand(s).

## Output

For each frame:

```text
Per-frame landmark coordinates
+
Hand-presence information
```

## Temporal Example

```text
Frame 1 → keypoints
Frame 2 → keypoints
Frame 3 → keypoints
...
Frame 30 → keypoints
```

## Handoff

Per-frame keypoints are passed to **Preprocessing / Normalization**.

---

# 6. Stage 4 — Preprocessing / Normalization

## Owner

**Agent 1**

## Purpose

Convert raw landmark coordinates into a consistent numerical representation.

## Input

```text
Raw per-frame landmark coordinates
+
Hand-presence information
```

## Possible Operations

- Normalize relative to a reference point.
- Handle missing hands.
- Standardize dimensions.
- Remove unnecessary noise.

## Output

```text
Consistent numerical feature vector for every frame
```

## Critical Contract Requirement

The exact vector shape and landmark ordering **must be written in `CONTRACTS.md`**.

Do not make downstream agents guess:
- vector dimensions
- landmark ordering
- missing-hand representation
- normalization behavior

## Handoff

Normalized frame-level feature vectors are passed to the **Rolling Sequence Buffer**.

---

# 7. Stage 5 — Rolling Sequence Buffer

## Owner

**Agent 1 + Agent 2 interface**

## Purpose

Maintain the most recent `N` frames as a temporal sequence.

## Input

```text
Normalized numerical feature vectors
```

## Behavior

The buffer continuously maintains recent frames.

Conceptual operation:

```text
REMOVE oldest frame
+
ADD newest frame
```

## Example

```text
30–60 frames → one temporal sequence
```

The exact production window size should be treated as a configurable implementation parameter unless fixed elsewhere in `CONTRACTS.md`.

## Output

```text
Sequence tensor / temporal window
```

## Handoff

The sequence is passed to the **Temporal Model**.

---

# 8. Stage 6 — Temporal Model

## Owner

**Agent 2**

## Purpose

Predict a sign from a temporal sequence rather than from a single static image.

## Input

```text
Temporal sequence of normalized keypoint features
```

## Possible MVP Models

- LSTM
- GRU
- Small Transformer encoder

## Model Behavior

The model learns temporal patterns involving:

- hand shape
- movement
- direction
- timing

## Output

```text
Predicted sign class
+
Confidence
```

## Example

```text
"thank_you" — 0.91
```

## Handoff

The raw prediction is passed to **Temporal Stability / Prediction Filter**.

---

# 9. Stage 7 — Temporal Stability / Prediction Filter

## Owner

**Agent 3**

## Purpose

Convert noisy raw model predictions into stable sign events.

## Problem

Raw predictions may fluctuate.

Example:

```text
hello
hello
hello
hello
water
hello
hello
```

The system must **not** immediately treat every prediction as a new word.

## Input

```text
Predicted sign class
+
Confidence
+
Temporal prediction history
```

## Processing Rules

The filter should:

1. Check confidence.
2. Check stability across several frames.
3. Detect a change in predicted sign.
4. Prevent duplicate word insertion.

## Output

```text
Stable SIGN EVENT
```

## Example Event

```json
{
  "word": "hello",
  "confidence": 0.91,
  "timestamp": "..."
}
```

> The exact event schema should be documented in `CONTRACTS.md` before downstream integration.

## Handoff

Stable sign events are passed to **Sign Segmentation**.

---

# 10. Stage 8 — Sign Segmentation

## Owner

**Agent 3**

## Purpose

Determine when one sign has effectively finished.

## MVP Strategy

Use practical temporal heuristics.

Do **not** claim perfect continuous-sign segmentation for the MVP.

## Possible Signals

- stable prediction
- prediction change
- low-confidence transition
- short movement/hold condition

## Required Documentation

This segmentation strategy must be documented as an **MVP approximation**.

## Output

```text
Accepted word/sign
```

## Handoff

Accepted words/signs are passed to the **Word Buffer**.

---

# 11. Stage 9 — Word Buffer

## Owner

**Agent 3**

## Purpose

Store accepted words in the order they are recognized.

## Input

```text
Accepted words/signs
```

## Example

```text
["hello", "my", "name", "is", "X"]
```

## Required Behavior

The system should avoid duplicate insertion.

## Output

```text
Ordered word sequence
```

## Handoff

The ordered words are passed to **Basic Sentence Smoothing**.

---

# 12. Stage 10 — Basic Sentence Smoothing

## Owner

**Agent 3**

## Purpose

Convert recognized words into a more readable sentence.

## Example

### Raw

```text
"hello my name monil"
```

### Output

```text
"Hello, my name is Monil."
```

## MVP Constraint

**Do not build a huge grammar engine for the MVP.**

Use simple, documented sentence-smoothing rules.

## Output

```text
Readable sentence
```

## Handoff

The sentence is sent to:
- Text Display
- Text-to-Speech

---

# 13. Stage 11 — Text Display

## Owner

**Agent 4**

## Purpose

Display the current recognition state to the user.

## UI Must Show

- current predicted sign
- confidence
- recognized words
- current sentence
- system status

## Example Information

```text
Current Sign:
THANK YOU

Confidence:
91%

Recognized:
hello → thank_you → water

Sentence:
"Hello, thank you for the water."

Status:
● Camera
● Model
● Speech
```

---

# 14. Stage 12 — Text-to-Speech

## Owner

**Agent 3**

## Purpose

Convert the completed/stable sentence into speech.

## Input

```text
Completed/stable sentence
```

## MVP Preference

Use a **local/offline TTS option where practical**, so an internet failure does not break the demonstration.

## Critical Runtime Requirement

TTS must **not freeze the camera/inference loop**.

The speech operation should therefore be handled in a way that keeps live inference responsive.

## Output

```text
Spoken sentence
```

---

# 15. Stage 13 — Live UI / Demo

## Owner

**Agent 4**

## Purpose

Connect the system into a usable real-time demonstration.

## Expected UI Structure

```text
--------------------------------
 REAL-TIME SIGN TRANSLATOR
--------------------------------

 Camera Feed

 Current Sign:
 THANK YOU

 Confidence:
 91%

 Recognized:
 hello → thank_you → water

 Sentence:
 "Hello, thank you for the water."

 Status:
 ● Camera
 ● Model
 ● Speech

--------------------------------
```

## Integration Requirements

The UI should receive outputs from the underlying pipeline without changing subsystem contracts silently.

---

# 16. Stage 14 — End-to-End Result

The complete logical pipeline is:

```text
User signs
    ↓
Camera
    ↓
Keypoints
    ↓
Preprocessing
    ↓
Rolling sequence
    ↓
Temporal model
    ↓
Stable sign event
    ↓
Segmentation
    ↓
Word buffer
    ↓
Sentence smoothing
    ↓
Text
    ↓
Speech
```

---

# 17. System Evolution by Agent

## After Agent 1

The system can:

- see the user through the webcam
- convert video into consistent numerical keypoint sequences

The system **cannot understand signs yet**.

---

## After Agent 2

The system can:

- accept a keypoint sequence
- predict one of the trained signs

It may work offline on recorded/test sequences before real-time integration.

---

## After Agent 3

The system can:

- turn unstable model predictions into usable words
- build a running sentence
- speak the result

---

## After Agent 4

All modules are connected into:

- a usable live demonstration
- visual feedback
- complete end-to-end interaction

---

# 18. Final MVP Definition

The intended MVP is:

```text
A person performs one of the supported signs/short sequences
        ↓
The system recognizes it
        ↓
The system displays the word/sentence
        ↓
The system speaks it
```

---

# 19. Explicit MVP Limitation

A **20–30-word MVP** is a controlled demonstration.

It is **not unrestricted Indian Sign Language or American Sign Language translation**.

The implementation and documentation must not claim broader language coverage than the trained vocabulary and demonstrated capabilities actually support.

---

# 20. AI Agent Implementation Rules

An AI coding agent reading this document must follow these rules.

## Rule 1 — Follow the Pipeline

Do not bypass or silently reorder the documented stages.

Primary order:

```text
Camera
→ Keypoints
→ Preprocessing
→ Sequence
→ Model
→ Prediction Filter
→ Segmentation
→ Word Buffer
→ Sentence
→ Text
→ Speech
```

## Rule 2 — Respect Ownership

Before editing a subsystem, identify its owner.

| Owner | Primary Responsibility |
|---|---|
| Agent 1 | Camera, keypoints, preprocessing, sequence input |
| Agent 2 | Dataset, temporal model, model inference |
| Agent 3 | Prediction filtering, segmentation, words, sentence, TTS |
| Agent 4 | Text display, UI, live integration |

## Rule 3 — Do Not Guess Contracts

If the exact shape, schema, ordering, or representation is unspecified, document it in `CONTRACTS.md` before relying on it.

## Rule 4 — Preserve Existing Interfaces

Do not silently modify another agent's interface.

If an interface must change:
1. document the change
2. update `CONTRACTS.md`
3. update affected consumers
4. run relevant tests

## Rule 5 — Do Not Overbuild the MVP

The source workflow explicitly calls for practical MVP approximations.

Avoid:
- huge grammar engines
- claims of perfect continuous-sign segmentation
- unnecessary face/pose processing in the first MVP
- unrestricted sign-language translation claims

## Rule 6 — Keep Real-Time Behavior Responsive

Camera capture, inference, UI updates, and TTS must work together without the speech subsystem freezing the live inference loop.

## Rule 7 — Validate Every Handoff

At every stage verify:

```text
INPUT
→ PROCESSING
→ OUTPUT
→ CONTRACT
→ VALIDATION
```

## Rule 8 — Prefer Explicit Failure States

When a stage cannot produce valid output, the downstream system should receive a clear state rather than silently assuming valid data.

## Rule 9 — Use Mocked Outputs for Parallel Development

If an upstream module is incomplete, downstream work may use mocked outputs that match the documented contract.

Do not alter upstream implementation merely to unblock UI or downstream development.

## Rule 10 — Keep Documentation Synchronized

When an implementation changes:
- update the relevant contract
- update status documentation
- update tests
- record important limitations

---

# 21. Agent Handoff Matrix

| From | Output | To |
|---|---|---|
| Camera Capture | Video frames | Agent 1 / Keypoint Extraction |
| Keypoint Extraction | Landmark coordinates + hand presence | Preprocessing |
| Preprocessing | Fixed/consistent numerical frame features | Sequence Buffer |
| Sequence Buffer | Temporal sequence/window | Agent 2 |
| Temporal Model | Sign class + confidence | Agent 3 |
| Prediction Filter | Stable sign event | Segmentation |
| Segmentation | Accepted word/sign | Word Buffer |
| Word Buffer | Ordered words | Sentence Smoothing |
| Sentence Smoothing | Readable sentence | Agent 4 + TTS |
| TTS | Spoken sentence | User |
| UI Integration | Live visual feedback | User |

---

# 22. Minimum Validation Checklist

Before considering the complete workflow operational:

- [ ] Camera opens.
- [ ] Frames arrive continuously.
- [ ] Frame rate is acceptable.
- [ ] MediaPipe detects hand landmarks.
- [ ] MVP uses 21 landmarks per detected hand.
- [ ] Missing-hand behavior is defined.
- [ ] Feature normalization is consistent.
- [ ] Exact vector shape is documented in `CONTRACTS.md`.
- [ ] Rolling sequence buffer works.
- [ ] Temporal model accepts the agreed sequence format.
- [ ] Model returns sign class + confidence.
- [ ] Prediction filtering suppresses unstable duplicates.
- [ ] Sign segmentation works as a documented MVP heuristic.
- [ ] Word buffer preserves order.
- [ ] Duplicate words are not unnecessarily inserted.
- [ ] Sentence smoothing produces readable output.
- [ ] Text is displayed.
- [ ] TTS works.
- [ ] TTS does not freeze live inference.
- [ ] UI displays system status.
- [ ] End-to-end pipeline works.
- [ ] MVP limitations are accurately represented.

---

# 23. Source-Fidelity Note

This Markdown specification is a structured conversion of the supplied **REAL-TIME SIGN LANGUAGE TRANSLATOR — LOGICAL WORKFLOW**. The source defines the stages from user input through camera capture, keypoint extraction, preprocessing, sequence buffering, temporal modeling, prediction filtering, segmentation, word buffering, sentence smoothing, text display, TTS, and live UI, as well as the stated MVP limitation. fileciteturn1file0L4-L8
