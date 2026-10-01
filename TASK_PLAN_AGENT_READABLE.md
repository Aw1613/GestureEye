# Real-Time Sign Language Translator — 4-Member Task Plan

> **Purpose:** This document is the authoritative task-plan specification for a four-member real-time sign-language translation project.
>
> **Agent-readability requirement:** An AI coding agent (including an Antigravity-style agent) should be able to read this file without guessing ownership, dependencies, interfaces, milestones, or acceptance criteria.
>
> **Source preservation:** The structure and requirements below are based on the provided task plan. No project requirement has been intentionally removed.

---

## 1. Team Operating Rules

### 1.1 Ownership
- Each member owns **one major subsystem**.
- Each owner is responsible for:
  - implementation
  - tests
  - documentation
  - integration support
  - debugging of their subsystem

### 1.2 Parallel Development Rule
Work may happen in parallel **only after the required interfaces/contracts are documented**.

### 1.3 Change-Control Rules
Agents/members must **NOT**:
1. Change another agent's interface silently.
2. Duplicate another agent's implementation.
3. Edit another agent's core module without coordination.

### 1.4 Shared Responsibilities
All four members participate in:
- architecture review
- final integration
- testing
- demo rehearsal

### 1.5 Contribution Principle
Do **not** measure equal contribution by number of files.

Each member owns one major subsystem plus its implementation, tests, documentation, integration support, and debugging.

---

# 2. System Overview

The project is a **real-time sign language translator**.

The intended high-level pipeline is:

```text
VIDEO
  ↓
NUMERICAL TEMPORAL KEYPOINT SEQUENCES
  ↓
SIGN + CONFIDENCE
  ↓
STABLE WORDS
  ↓
SENTENCE
  ↓
SPEECH
  ↓
COMPLETE LIVE DEMO
```

The four major subsystems are:

1. **Member 1:** Input & Keypoint Pipeline
2. **Member 2:** Dataset & ML Model
3. **Member 3:** Sentence Logic & Speech
4. **Member 4:** UI & Integration

---

# 3. Member 1 — Input & Keypoint Pipeline

## 3.1 Owner
**Member 1**

## 3.2 Main Goal
Convert webcam video into clean, consistent temporal keypoint sequences.

## 3.3 Tasks
1. Inspect camera requirements.
2. Set up webcam capture.
3. Integrate MediaPipe Hands.
4. Define landmark ordering.
5. Handle one-hand and two-hand cases.
6. Define missing-hand representation.
7. Implement preprocessing.
8. Implement coordinate normalization.
9. Build rolling sequence buffer.
10. Build data-capture utility for training samples.
11. Add basic tests.
12. Document the keypoint contract.

## 3.4 Deliverables
- camera module
- keypoint extraction module
- preprocessing module
- sequence buffer
- data collection utility
- tests
- `CONTRACTS.md` contribution

## 3.5 Acceptance Criteria
The subsystem is considered ready when:
- webcam opens reliably
- landmarks are extracted
- missing landmarks are handled
- output has fixed dimensions
- sequence windows can be created
- another agent can consume the output **without guessing its format**

## 3.6 Milestone Output

```text
VIDEO → NUMERICAL TEMPORAL KEYPOINT SEQUENCES
```

## 3.7 Handoff Requirement
Member 1 must document the exact keypoint format before Member 2 depends on it.

The contract must make the following unambiguous:
- landmark ordering
- one-hand/two-hand representation
- missing-hand representation
- preprocessing
- coordinate normalization
- fixed output dimensions
- sequence-window format

---

# 4. Member 2 — Dataset & ML Model

## 4.1 Owner
**Member 2**

## 4.2 Main Goal
Train and validate the temporal sign classifier.

## 4.3 Tasks
1. Inspect candidate dataset structure.
2. Select an initial **20–30 sign vocabulary**.
3. Map dataset labels to project labels.
4. Build preprocessing pipeline compatible with Member 1.
5. Split train/validation/test correctly.
6. Avoid signer leakage where the dataset allows signer-aware splitting.
7. Build baseline LSTM or GRU.
8. Evaluate baseline.
9. Try a small alternative model only if useful.
10. Add keypoint-sequence augmentation.
11. Save model and label mapping.
12. Build inference wrapper.
13. Record metrics and limitations.

## 4.4 Deliverables
- dataset loader
- preprocessing compatibility
- training script
- evaluation script
- trained model
- label map
- inference module
- metrics report

## 4.5 Acceptance Criteria
The subsystem is considered ready when:
- training runs reproducibly
- held-out evaluation works
- model accepts the agreed sequence format
- model returns **class + confidence**
- model can be loaded without retraining

## 4.6 Milestone Output

```text
KEYPOINT SEQUENCE → SIGN + CONFIDENCE
```

## 4.7 Handoff Requirement
Member 2 must document the prediction output format so Member 3 can consume it without guessing.

---

# 5. Member 3 — Sentence Logic & Speech

## 5.1 Owner
**Member 3**

## 5.2 Main Goal
Turn noisy model predictions into stable words and speech.

## 5.3 Tasks
1. [x] Define prediction event format (`CONTRACTS.md` Contract C & D).
2. [x] Implement confidence filtering (`app/sentence/filter.py` with 0.60 threshold).
3. [x] Implement temporal stability check (`app/sentence/filter.py` with 5-frame window).
4. [x] Prevent repeated identical predictions (`app/sentence/filter.py` duplicate suppression).
5. [x] Implement practical sign-boundary/segmentation heuristic (`app/sentence/segmentation.py`).
6. [x] Maintain word buffer (`app/sentence/builder.py`).
7. [x] Implement basic sentence smoothing (`app/sentence/builder.py` Contract E).
8. [x] Implement sentence finalization (`app/sentence/builder.py` finalize_sentence).
9. [x] Integrate TTS (`app/tts/speech.py` pyttsx3 engine Contract F).
10. [x] Ensure TTS does not block live inference (`app/tts/speech.py` worker thread & queue).
11. [x] Add tests for duplicate suppression and sentence building (`tests/test_filter.py`, `tests/test_builder.py`, `tests/test_speech.py`, `tests/test_sentence_speech_integration.py`).

## 5.4 Deliverables
- [x] prediction filter (`app/sentence/filter.py`)
- [x] sign-event generator (`app/sentence/filter.py` Contract D)
- [x] segmentation logic (`app/sentence/segmentation.py`)
- [x] word buffer (`app/sentence/builder.py`)
- [x] sentence builder (`app/sentence/builder.py` Contract E)
- [x] TTS module (`app/tts/speech.py` Contract F)
- [x] tests (19/19 passing)
- [x] demo script (`scripts/demo_agent3.py`)

## 5.5 Acceptance Criteria
The subsystem is considered ready when:
- repeated model predictions do not become repeated words
- low-confidence predictions can be rejected
- words remain in correct order
- sentence can be generated
- TTS can speak it
- TTS does not freeze the main application

## 5.6 Milestone Output

```text
SIGN PREDICTIONS → STABLE WORDS → SENTENCE → SPEECH
```

## 5.7 Handoff Requirement
Member 3 must expose stable outputs that Member 4 can display and integrate.

---

# 6. Member 4 — UI & Integration

## 6.1 Owner
**Member 4**

## 6.2 Main Goal
Connect everything into a simple, judge-friendly live application.

## 6.3 Tasks
1. [x] Inspect outputs from Members 1–3 (`docs/HANDOFF_AGENT3_TO_AGENT4.md`, `CONTRACTS.md`).
2. [x] Build UI shell (`app/ui/overlay.py` 1000x680 composite dark HUD dashboard).
3. [x] Show live camera feed (`app/ui/overlay.py` viewport with hand skeletons and mode tags).
4. [x] Show current sign (`app/ui/overlay.py` high-visibility typography).
5. [x] Show confidence (`app/ui/overlay.py` dynamic color progress bar, threshold tiered).
6. [x] Show recognized words (`app/ui/overlay.py` word chips buffer).
7. [x] Show running sentence (`app/ui/overlay.py` smoothed sentence container box).
8. [x] Show system status (`app/ui/overlay.py` CAM, MODEL, VOICE badges, Contract G).
9. [x] Connect real-time pipeline (`app/ui/app.py` connecting Agent 1 + 2 + 3 + 4).
10. [x] Add error states (fallback for missing camera, missing audio card, and headless environments).
11. [x] Add start/stop/reset controls (`app/ui/app.py` key handlers: 's', 'c', '\b', 'm', 'q', '1'-'5').
12. [x] Run end-to-end tests (`tests/test_end_to_end_mvp.py`, 39/39 passing tests).
13. [x] Improve demo reliability (`scripts/demo_agent4.py` automated tour, headless benchmark mode).
14. [x] Document demo procedure (`docs/DEMO_INSTRUCTIONS.md`, `docs/HANDOFF_AGENT4_INTEGRATION.md`).

## 6.4 Deliverables
- [x] UI (`app/ui/overlay.py`, `app/ui/app.py`, `app/ui/__init__.py`)
- [x] integration layer (`app/ui/app.py` `SignBridgeApp`)
- [x] status/error display (`app/ui/overlay.py` Contract G status badges and toast alerts)
- [x] end-to-end tests (`tests/test_overlay.py`, `tests/test_ui_app.py`, `tests/test_end_to_end_mvp.py`)
- [x] demo instructions (`docs/DEMO_INSTRUCTIONS.md`, `scripts/demo_agent4.py`, `scripts/run_app.py`)

## 6.5 Acceptance Criteria
The subsystem is considered ready when:
- [x] camera appears (live or synthetic mock feed)
- [x] recognition appears (Contract C & D)
- [x] sentence updates (Contract E)
- [x] speech works (async non-blocking TTS Contract F)
- [x] errors are understandable (visual toasts & alerts)
- [x] system remains responsive (30+ FPS, < 0.001s speech invocation)

## 6.6 Milestone Output

```text
COMPLETE LIVE DEMO
```

---

# 7. Dependency Order

The implementation should follow this dependency order.

## Phase 0 — All Members

Complete:
- repository inspection
- architecture
- `CONTRACTS.md`
- `PROJECT_STATUS.md`

## Phase 1 — Member 1

Complete:
- keypoint format

## Phase 2 — Member 2

Complete:
- model can consume Member 1 format
- Member 3 can consume Member 2 prediction format

## Phase 3 — Member 3

Complete:
- stable words
- sentence

## Phase 4 — Member 4

Complete:
- integration

## Phase 5 — All Members

Complete:
- testing
- bug fixing
- demo rehearsal

---

# 8. Safe Parallel Work

The following work can happen simultaneously when the relevant contracts are agreed.

| Member | Safe Parallel Work |
|---|---|
| Member 1 | Webcam and keypoint implementation |
| Member 2 | Dataset inspection and training pipeline using the agreed feature contract |
| Member 3 | Prediction filtering using mocked predictions |
| Member 4 | UI using mocked outputs |

This enables all four members to work simultaneously without requiring unfinished upstream modules.

---

# 9. Milestones

## M0 — Architecture Ready

### Output
- folder structure
- ownership
- contracts
- status tracking

## M1 — Input Ready

### Output
- stable keypoints

## M2 — ML Ready

### Output
- trained classifier

## M3 — Logic + Speech Ready

### Output
- stable sentence + audio

## M4 — UI Ready

### Output
- live interface

## M5 — Integrated MVP

### Output
- complete demonstration

## M6 — Demo Hardening

### Output
- tests
- error handling
- reproducible setup
- demo script

---

# 10. Validation Checklist — Every Milestone

At every milestone, verify all of the following:

- [ ] Correct files exist.
- [ ] Correct owner is editing them.
- [ ] Imports work.
- [ ] Tests pass.
- [ ] Contract is unchanged or versioned.
- [ ] No duplicate implementation exists.
- [ ] `PROJECT_STATUS.md` is updated.
- [ ] Another member can understand the handoff.

---

# 11. Agent Handoff Rules

When an agent finishes work on a subsystem:

1. Verify its acceptance criteria.
2. Run the relevant tests.
3. Confirm the documented interface/contract.
4. Update `PROJECT_STATUS.md`.
5. Document any limitations or known issues.
6. Clearly identify files created or modified.
7. Do not silently change another subsystem's contract.
8. Make the output consumable by the next subsystem without requiring assumptions.

---

# 12. AI Agent Execution Guidance

An AI coding agent reading this file should use the following rules:

## Rule A — Identify Ownership First
Before modifying a file, determine which member/subsystem owns it.

## Rule B — Respect Contracts
Do not infer undocumented data formats when a contract is required. If an interface is missing or ambiguous, document the interface before depending on it.

## Rule C — Avoid Duplicate Implementations
Search the repository before creating a new implementation of an existing subsystem.

## Rule D — Preserve Integration Boundaries
Member 1 → Member 2 → Member 3 → Member 4 is the primary dependency chain.

## Rule E — Use Mocked Interfaces for Parallel Work
If an upstream component is unfinished, use a clearly documented mock rather than changing the upstream implementation.

## Rule F — Validate Before Handoff
A subsystem is not complete merely because its code exists. Its tests, documentation, acceptance criteria, and handoff information must also be complete.

## Rule G — Keep Status Current
Update `PROJECT_STATUS.md` whenever a milestone, interface, implementation state, or important limitation changes.

## Rule H — Do Not Make Silent Cross-Agent Changes
If a change affects another subsystem's contract, coordinate it and version/document the change.

---

# 13. Authoritative Project Flow

The complete intended system is:

```text
[WEBCAM VIDEO]
      |
      v
[MEMBER 1: INPUT & KEYPOINT PIPELINE]
      |
      | fixed-format temporal keypoint sequence
      v
[MEMBER 2: DATASET & ML MODEL]
      |
      | sign class + confidence
      v
[MEMBER 3: SENTENCE LOGIC & SPEECH]
      |
      | stable words + sentence + speech
      v
[MEMBER 4: UI & INTEGRATION]
      |
      v
[COMPLETE LIVE DEMO]
```

---

# 14. Definition of Done

The project reaches the intended MVP when:

- [x] Webcam input works.
- [x] Hand landmarks are extracted.
- [x] Keypoints are normalized into a fixed, documented format.
- [x] Temporal sequences can be created.
- [x] The ML model can consume the agreed sequence format.
- [x] The classifier returns a sign class and confidence.
- [x] Repeated/noisy predictions are filtered.
- [x] Stable words are produced in order.
- [x] A sentence can be generated.
- [x] TTS can speak the sentence without freezing live inference.
- [x] UI displays the live camera, recognition, confidence, words, sentence, and status.
- [x] Errors are understandable.
- [x] End-to-end tests pass.
- [x] Setup is reproducible.
- [x] Demo procedure is documented.
- [x] All milestone/status documentation is current.

---

# 15. Reference to Original Task Plan

This Markdown document is a structured, agent-readable conversion of the supplied **REAL-TIME SIGN LANGUAGE TRANSLATOR — 4-MEMBER TASK PLAN**. The original plan establishes subsystem ownership, tasks, deliverables, acceptance criteria, dependency order, safe parallel work, milestones, validation requirements, and the equal-contribution model. fileciteturn0file0L1-L5
