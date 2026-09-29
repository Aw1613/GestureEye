# 🤟 SignBridge — System Architecture \& Engineering Specification

> \*\*Project:\*\* SignBridge  
> \*\*Purpose:\*\* Real-time sign-language communication assistant  
> \*\*Document type:\*\* Architecture + agent instructions + module contracts  
> \*\*Status:\*\* Initial architecture specification  
> \*\*Audience:\*\* Human developers, Antigravity agents, reviewers, and hackathon judges

\---

## 0\. 🤖 HOW TO USE THIS FILE

This document is the **engineering source of truth** for the SignBridge repository.

### Rules for Antigravity / AI coding agents

1. **Read this file before modifying the architecture.**
2. Inspect the existing repository before creating or moving files.
3. Treat the module ownership and data contracts below as interfaces.
4. Do not silently change a shared contract.
5. Do not create duplicate implementations of an existing module.
6. Do not invent datasets, labels, model metrics, or test results.
7. Keep the MVP small, testable, and real-time.
8. Prefer simple implementations over unnecessary complexity.
9. Every architectural change should identify:

   * what changed,
   * why it changed,
   * which module owns it,
   * which interface is affected,
   * how it is tested.
10. Never put model training inside the real-time UI/inference loop.
11. Never block webcam capture with TTS, training, or heavy UI operations.
12. If an existing repository implementation conflicts with this document, **inspect the code and discuss the conflict before making a destructive change**.

\---

# 1\. 🎯 PROJECT GOAL

SignBridge is a real-time sign-language communication assistant.

The system captures video from a webcam, extracts hand/body information, recognizes a **defined sign vocabulary**, converts recognized signs into words/sentences, and provides text and speech output.

### Core communication flow

```text
SIGNING USER
    │
    ▼
📷 Webcam
    │
    ▼
🎥 Frame Capture
    │
    ▼
🤚 MediaPipe Keypoints
    │
    ▼
🧹 Preprocessing + Normalization
    │
    ▼
📦 Rolling Sequence Window
    │
    ▼
🧠 Temporal ML Model
    │
    ▼
🎯 Sign + Confidence
    │
    ▼
🔄 Temporal Filtering + Segmentation
    │
    ▼
📝 Word Buffer + Sentence Builder
    │
    ├──────────────► 🖥️ Live Text UI
    │
    └──────────────► 🔊 Text-to-Speech
```

### Important scope

The MVP recognizes a **defined vocabulary** of signs.

It must **not** claim universal sign-language translation.

\---

# 2\. 🏗️ HIGH-LEVEL ARCHITECTURE

```text
┌─────────────────────┐
│       WEBCAM        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Frame Capture     │
│      Agent 1        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  MediaPipe          │
│  Keypoint Extraction│
│      Agent 1        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Preprocessing +     │
│ Normalization       │
│      Agent 1        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Rolling Window    │
│      Agent 1        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Temporal ML      │
│    LSTM / GRU       │
│      Agent 2        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Sign + Confidence   │
│      Agent 2        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Temporal Filter +   │
│ Segmentation        │
│      Agent 3        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Word Buffer +       │
│ Sentence Builder    │
│      Agent 3        │
└──────────┬──────────┘
           │
      ┌────┴─────┐
      ▼          ▼
┌──────────┐ ┌──────────┐
│   TEXT   │ │   TTS    │
│ Agent 4  │ │ Agent 3  │
└────┬─────┘ └──────────┘
     │
     ▼
┌─────────────────────┐
│      Live UI        │
│      Agent 4        │
└─────────────────────┘
```

\---

# 3\. 📁 REPOSITORY ARCHITECTURE

Use this structure as the starting point.

```text
SignBridge/
│
├── app/
│   ├── capture/
│   │   └── camera.py
│   │
│   ├── keypoints/
│   │   ├── extractor.py
│   │   └── preprocessing.py
│   │
│   ├── recognition/
│   │   ├── model.py
│   │   ├── inference.py
│   │   └── labels.py
│   │
│   ├── sentence/
│   │   ├── filter.py
│   │   ├── segmentation.py
│   │   └── builder.py
│   │
│   ├── tts/
│   │   └── speech.py
│   │
│   └── ui/
│       └── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── models/
│
├── training/
│   ├── dataset.py
│   ├── train.py
│   └── evaluate.py
│
├── tests/
│
├── scripts/
│
├── configs/
│
├── docs/
│
├── CONTRACTS.md
├── PROJECT\_STATUS.md
├── README.md
└── requirements.txt
```

### Repository rule

This is a **starting architecture, not a blind copy-paste rule**.

Before creating files, Antigravity must inspect the current repository and reuse existing implementations where appropriate.

\---

# 4\. 👥 MODULE OWNERSHIP

|Agent|Primary responsibility|Main modules|
|-|-|-|
|**Agent 1**|Camera + computer vision + preprocessing|`capture/`, `keypoints/`, sequence buffering|
|**Agent 2**|ML training + recognition|`training/`, `recognition/`, `models/`|
|**Agent 3**|Temporal logic + sentence + speech|`sentence/`, `tts/`|
|**Agent 4**|UI + integration|`ui/`, integration layer|

### Shared ownership

All agents may contribute carefully to:

```text
tests/
docs/
CONTRACTS.md
PROJECT\_STATUS.md
```

### Shared-file rule

Do not make unrelated changes to another agent's module.

If a shared contract must change:

```text
1. Identify the breaking change.
2. Update CONTRACTS.md.
3. Update affected modules.
4. Add/update tests.
5. Document the change.
```

\---

# 5\. 🔌 DATA CONTRACTS

The modules communicate through simple, explicit data structures.

## 5.1 Frame Features

```text
Frame
    ↓
fixed-length numeric vector
```

The feature dimension must be defined by the preprocessing implementation and remain consistent between training and inference.

\---

## 5.2 Sequence

```text
N frames × feature\_dimension
```

Example conceptual representation:

```python
sequence.shape == (N, FEATURE\_DIM)
```

The exact values of `N` and `FEATURE\_DIM` must come from the active configuration.

\---

## 5.3 Model Output

The model converts a sequence into class probabilities:

```text
sequence
    ↓
model
    ↓
class probabilities
```

\---

## 5.4 Prediction Event

```json
{
  "label": "...",
  "confidence": 0.0,
  "timestamp": 0.0
}
```

### Contract

* `label`: predicted class/sign label.
* `confidence`: numeric confidence in the range expected by the model wrapper.
* `timestamp`: event timestamp.

The inference layer must return a predictable schema.

\---

## 5.5 Stable Sign Event

After temporal filtering:

```json
{
  "word": "...",
  "confidence": 0.0,
  "start\_time": 0.0,
  "end\_time": 0.0
}
```

This represents a sign that is stable enough to enter the sentence pipeline.

\---

## 5.6 Sentence Object

```json
{
  "words": \["...", "..."],
  "text": "..."
}
```

\---

## 5.7 TTS Input

```json
{
  "text": "..."
}
```

The TTS module must accept finalized text rather than raw model predictions.

\---

# 6\. 🔗 MODULE INTERFACES

## Interface A — Agent 1 → Agent 2

### Input

A fixed-format normalized keypoint sequence.

```text
Agent 1
Camera
  ↓
Keypoints
  ↓
Normalization
  ↓
Sequence
  ↓
Agent 2
```

### Requirement

Agent 2 **must not need to know how the camera works**.

\---

## Interface B — Agent 2 → Agent 3

### Input

```text
predicted label
confidence
timing
```

Conceptually:

```json
{
  "label": "HELP",
  "confidence": 0.94,
  "timestamp": 123.45
}
```

### Requirement

Agent 3 **must not need to know the internals of the ML model**.

\---

## Interface C — Agent 3 → Agent 4

### Input

```text
current sign
confidence
recognized words
sentence
system state
```

### Requirement

Agent 4 **must not implement its own recognition logic**.

\---

# 7\. 🧠 MODEL ARCHITECTURE

## MVP model

```text
Keypoint Sequence
       ↓
   LSTM / GRU
       ↓
   Dense Layer
       ↓
    Softmax
       ↓
   Sign Class
```

### Model-selection rule

The exact architecture must be selected based on:

* dataset size,
* feature dimension,
* sequence length,
* available hardware,
* inference latency,
* validation performance.

Avoid unnecessarily large models.

### Evaluation rule

The model must be evaluated on **held-out data**.

Do not report invented accuracy.

\---

# 8\. 🏋️ TRAINING PIPELINE

```text
Dataset Videos
      ↓
Frame Sampling
      ↓
Keypoint Extraction
      ↓
Normalization
      ↓
Sequence Creation
      ↓
Train / Validation / Test Split
      ↓
Augmentation
      ↓
Model Training
      ↓
Evaluation
      ↓
Save Model
      ↓
Inference Wrapper
```

### Training principle

Training is an **offline process**.

The live application should load an already-trained model.

\---

# 9\. ⚡ REAL-TIME INFERENCE PIPELINE

```text
Camera Frame
      ↓
Keypoints
      ↓
Normalization
      ↓
Append to Rolling Buffer
      ↓
Enough Frames?
   ┌──┴──┐
   NO    YES
   │      │
   │      ▼
   │   Model Inference
   │      ↓
   │   Prediction
   │      ↓
   │   Temporal Filter
   │      ↓
   │   Stable Sign Event
   │      ↓
   │   Sentence Buffer
   │      ↓
   │   Sentence Smoothing
   │      ↓
   └──► UI Update
           ↓
      TTS when finalized
```

### Real-time rule

If the sequence is too short, **wait**.

Do not make random predictions from insufficient data.

\---

# 10\. 🧩 ERROR HANDLING

The application must fail clearly rather than silently.

|Condition|Required behavior|
|-|-|
|Camera unavailable|Show `Camera not available.`|
|No hand detected|Show `No sign detected.`|
|Insufficient sequence|Wait; do not predict|
|Low confidence|Show uncertain state; do not automatically add word|
|Model unavailable|Show clear model error|
|TTS unavailable|Keep text output working; show speech error|
|Dataset/model mismatch|Fail clearly; never silently reshape incompatible data|

\---

# 11\. 🧪 TESTING STRATEGY

## 11.1 Unit Tests

Test:

* keypoint normalization
* missing-hand handling
* sequence buffer
* prediction filtering
* duplicate suppression
* sentence builder

\---

## 11.2 Model Tests

Test:

* model loading
* input shape
* output classes
* inference speed

\---

## 11.3 Integration Tests

Test:

```text
keypoints → model
model → sentence
sentence → TTS
full pipeline
```

\---

## 11.4 Demo Test

Before every important demo:

```text
☐ Webcam works
☐ Keypoints are detected
☐ Sign is recognized
☐ Confidence is displayed
☐ Sentence is generated
☐ Audio works
☐ UI remains responsive
```

\---

# 12\. ⚡ PERFORMANCE REQUIREMENTS

The application should **feel real-time**.

### Never block:

```text
Camera Capture
```

with:

```text
Model Training
TTS
Heavy UI Operations
```

### Design principle

```text
TRAINING
   │
   └── Offline

INFERENCE
   │
   └── Lightweight + real-time

TTS
   │
   └── Queued / non-blocking where practical
```

\---

# 13\. 🔐 SECURITY \& PRIVACY BASELINE

For the local hackathon demo:

* Process webcam data locally where practical.
* Do not upload camera footage unless explicitly required.
* Avoid storing personal video by default.
* Document every external API/service used.
* Keep secrets and API keys outside source code.
* Never commit private credentials to GitHub.

\---

# 14\. 🚀 MVP VS STRETCH GOALS

## MVP — Required

```text
☐ 20–30 signs
☐ Hand keypoints
☐ Temporal model
☐ Stable prediction
☐ Simple sentence construction
☐ Offline/local TTS
☐ Live UI
```

## Stretch Goals — Only after MVP works

```text
☐ Two-hand fusion
☐ Face/pose features
☐ Larger vocabulary
☐ Advanced continuous recognition
☐ Transformer-based model
☐ Multilingual output
☐ Mobile deployment
```

### Priority rule

> \*\*A stable MVP is more important than an unfinished advanced feature.\*\*

\---

# 15\. 📌 ARCHITECTURE VALIDATION CHECKLIST

Before accepting any architecture change, answer every question:

```text
\[ ] Does this duplicate an existing module?
\[ ] Does this break an existing interface?
\[ ] Does this create circular dependencies?
\[ ] Does this make real-time inference slower?
\[ ] Does this increase complexity without helping the MVP?
\[ ] Which agent owns this change?
\[ ] What tests prove that it works?
```

If any answer is unclear, inspect the repository and resolve the ambiguity before implementing.

\---

# 16\. 🗂️ DEVELOPMENT WORKFLOW

Recommended Git workflow:

```text
main
 │
 ├── agent-1-cv
 ├── agent-2-ml
 ├── agent-3-language
 └── agent-4-ui
```

### Workflow

```text
1. Pull latest main
2. Create/update your branch
3. Implement one focused change
4. Run relevant tests
5. Commit with a clear message
6. Push branch
7. Review integration impact
8. Merge only after tests pass
```

### Suggested commit style

```text
feat: add MediaPipe keypoint extractor
feat: add LSTM inference wrapper
feat: add temporal sign filter
feat: add sentence builder
feat: add Streamlit live UI
test: add sequence buffer tests
fix: handle missing hand landmarks
docs: update architecture contract
```

\---

# 17\. 🧭 IMPLEMENTATION ORDER

Build the project in this order.

## Phase 1 — Skeleton

```text
Repository
    ↓
Module structure
    ↓
Contracts
    ↓
Configuration
    ↓
Basic tests
```

## Phase 2 — Vision

```text
Webcam
    ↓
OpenCV
    ↓
MediaPipe
    ↓
Normalized keypoints
```

## Phase 3 — ML

```text
Dataset
    ↓
Sequences
    ↓
Training
    ↓
Evaluation
    ↓
Saved model
    ↓
Inference wrapper
```

## Phase 4 — Real-Time Recognition

```text
Camera
    ↓
Keypoints
    ↓
Rolling buffer
    ↓
Model
    ↓
Prediction
    ↓
Temporal filtering
```

## Phase 5 — Language

```text
Stable signs
    ↓
Word buffer
    ↓
Sentence builder
```

## Phase 6 — Output

```text
Sentence
   ├──► Text UI
   └──► TTS
```

## Phase 7 — Validation

```text
Unit tests
    ↓
Model tests
    ↓
Integration tests
    ↓
Real-world demo tests
```

\---

# 18\. 🧠 ENGINEERING PRINCIPLES

### Principle 1 — Modular

Each component should have one clear responsibility.

### Principle 2 — Testable

Every important transformation should be independently testable.

### Principle 3 — Real-time

Live inference must remain lightweight.

### Principle 4 — Explainable

Team members must understand the code and architecture they submit.

### Principle 5 — Evidence-based

Use actual datasets, actual measurements, and actual test results.

### Principle 6 — Minimal complexity

Do not add technology merely because it is available.

### Principle 7 — Contract-first

Modules communicate through explicit interfaces.

### Principle 8 — MVP-first

Finish the complete basic pipeline before adding stretch features.

\---

# 19\. 🤖 ANTIGRAVITY AGENT HANDOFF TEMPLATE

When assigning a task to Antigravity, use this structure:

```text
TASK:
\[One specific task]

OWNER:
\[Agent/module owner]

CONTEXT:
\[Relevant architecture section]

INPUT:
\[Expected input]

OUTPUT:
\[Expected output]

FILES:
\[Files that may be created/modified]

DO NOT CHANGE:
\[Protected modules/contracts]

ACCEPTANCE CRITERIA:
\[Exact conditions that define completion]

TESTS:
\[Tests that must pass]

DOCUMENTATION:
\[Docs that need updating]
```

### Example

```text
TASK:
Implement the MediaPipe keypoint extractor.

OWNER:
Agent 1

CONTEXT:
Architecture Section 6 — Interface A.

INPUT:
OpenCV video frame.

OUTPUT:
Fixed-format keypoint vector.

FILES:
app/keypoints/extractor.py
tests/test\_keypoints.py

DO NOT CHANGE:
ML model or sentence pipeline.

ACCEPTANCE CRITERIA:
- Handles valid frames.
- Handles missing hands.
- Returns consistent feature dimensions.
- Does not crash on an empty detection.
- Includes unit tests.

TESTS:
pytest tests/test\_keypoints.py
```

\---

# 20\. 📊 PROJECT DEFINITION OF DONE

A feature is **not complete** merely because the code runs once.

A feature is complete when:

```text
\[✓] Implementation exists
\[✓] Interface is respected
\[✓] Error handling exists
\[✓] Relevant tests exist
\[✓] No known regression is introduced
\[✓] Documentation is updated when necessary
\[✓] Another team member can understand how to use it
```

\---

# 21\. 🏁 FINAL SYSTEM

The intended final architecture is:

```text
                    ┌───────────────────┐
                    │      WEBCAM       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  OpenCV Capture   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ MediaPipe         │
                    │ Keypoints         │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Normalize +       │
                    │ Rolling Buffer    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ LSTM / GRU        │
                    │ Recognition       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Confidence +      │
                    │ Temporal Filter   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Word / Sentence   │
                    │ Builder           │
                    └──────┬──────┬─────┘
                           │      │
                    ┌──────▼──┐ ┌─▼────────┐
                    │  TEXT   │ │   TTS    │
                    └──────┬──┘ └────┬─────┘
                           │         │
                           └────┬────┘
                                ▼
                       ┌─────────────────┐
                       │   Streamlit UI  │
                       └─────────────────┘
```

\---

## ✅ FINAL RULE

> \*\*Build the smallest complete system first. Then make it smarter.\*\*

```text
Camera
  → Keypoints
  → Temporal Model
  → Stable Sign
  → Sentence
  → Text / Speech
  → Live UI
```

This pipeline is the backbone of SignBridge. Every future feature should strengthen this pipeline rather than unnecessarily complicate it.

