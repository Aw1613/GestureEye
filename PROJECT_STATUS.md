# SignBridge — Project Status

> **Purpose:** Living document that tracks milestone progress, blockers,
> and ownership status. Updated by all agents as work progresses.

---

## Current Phase: Phase 0 — Architecture Ready

---

## Milestone Tracker

| Milestone | Description | Status | Owner |
| M0 | Architecture Ready | DONE | All |
| M1 | Input Ready (stable keypoints) | DONE | Member 1 |
| M2 | ML Ready (classifier code & tests) | DONE (Weights Pending) | Member 2 |
| M3 | Logic + Speech Ready (sentence + audio) | DONE | Member 3 |
| M4 | UI Ready (live interface) | NOT STARTED | Member 4 |
| M5 | Integrated MVP | NOT STARTED | All |
| M6 | Demo Hardening | NOT STARTED | All |

---

## M0 — Architecture Ready (IN PROGRESS)

| Task | Status | Notes |
|------|--------|-------|
| Repository created | DONE | github.com/ujjwal-mahajan/Sign-Bridge |
| ARCHITECTURE.md | DONE | System architecture and module contracts |
| COLLABORATION_RULES.md | DONE | Agent communication and ownership rules |
| LOGICAL_WORKFLOW_AGENT_READABLE.md | DONE | 14-stage pipeline specification |
| TASK_PLAN_AGENT_READABLE.md | DONE | 4-member task plan and milestones |
| CONTRACTS.md | DONE | Data shapes and interface schemas |
| PROJECT_STATUS.md | DONE | This file |
| requirements.txt | DONE | Python dependencies for MVP |
| Folder structure created | DONE | App, training, data, tests, scripts, configs, docs |
| Vocabulary selected | DONE | Pending Agent 2 dataset inspection |

---

## M1 — Input Ready (DONE)

| Task | Status | Notes |
|------|--------|-------|
| Webcam capture module | DONE | app/capture/camera.py with mock & real support |
| MediaPipe Hands integration | DONE | app/keypoints/extractor.py (21 landmarks x 2 hands) |
| Landmark preprocessing | DONE | app/keypoints/preprocessing.py (wrist-relative, scale normalized) |
| Rolling sequence buffer | DONE | app/keypoints/buffer.py ((30, 126) sliding window) |
| Data collection utility | DONE | scripts/collect_data.py |
| Unit tests | DONE | tests/test_camera.py, tests/test_keypoints.py (6/6 passing) |
| Contract documentation verified | DONE | Fully conforms to CONTRACTS.md Contract A & B |

---

## M2 — ML Ready (DONE)

| Task | Status | Notes |
|------|--------|-------|
| Dataset inspection | DONE | |
| Vocabulary selection (20-30 signs) | DONE | |
| Label mapping | DONE | app/recognition/labels.py |
| Dataset loader | DONE | training/dataset.py |
| Train/val/test split | DONE | |
| LSTM/GRU model | DONE | app/recognition/model.py |
| Training pipeline | DONE | training/train.py |
| Evaluation | DONE | training/evaluate.py |
| Model export | DONE | models/ |
| Inference wrapper | DONE | app/recognition/inference.py |

---

## M3 — Logic + Speech Ready (DONE)

| Task | Status | Notes |
|------|--------|-------|
| Prediction filter | DONE | app/sentence/filter.py (stability window 5, conf >= 0.60, Contract D) |
| Sign segmentation | DONE | app/sentence/segmentation.py (heuristic boundary & pause detection) |
| Word buffer | DONE | app/sentence/builder.py (ordered storage, duplicate suppression) |
| Sentence builder | DONE | app/sentence/builder.py (heuristic smoothing, Contract E) |
| TTS integration | DONE | app/tts/speech.py (pyttsx3 engine, Contract F) |
| Non-blocking speech | DONE | app/tts/speech.py (background worker thread & queue) |
| Unit tests | DONE | tests/test_filter.py, test_builder.py, test_speech.py, test_sentence_speech_integration.py (19/19 passing) |

---

## M4 — UI Ready (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| UI layout | NOT STARTED | app/ui/app.py |
| Camera feed display | NOT STARTED | |
| Prediction overlay | NOT STARTED | |
| Confidence display | NOT STARTED | |
| Word/sentence display | NOT STARTED | |
| System status indicators | NOT STARTED | |
| Start/stop/reset controls | NOT STARTED | |

---

## M5 — Integrated MVP (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| End-to-end pipeline connection | NOT STARTED | |
| Integration tests | NOT STARTED | |
| Performance verification | NOT STARTED | |

---

## M6 — Demo Hardening (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| Error handling | NOT STARTED | |
| Demo rehearsal | NOT STARTED | |
| Demo script/instructions | NOT STARTED | docs/ |
| Final bug fixes | NOT STARTED | |

---

## Blockers

| Blocker | Affects | Status |
|---------|---------|--------|
| Real training data collection | Real model accuracy | In progress using scripts/collect_data.py |

---

## Recent Updates

| Date | Update | By |
|------|--------|----|
| 2026-10-01 | Member 3 complete: implemented prediction filter, sign segmentation, sentence builder with smoothing, non-blocking TTS, and 19 unit/integration tests (all passing) | Member 3 |
| 2026-10-01 | Merged Member 1 and Member 2 codebases into main; verified test suites | All / Team |
| 2026-10-01 | Member 2 complete: NUM_CLASSES fix, evaluate.py, test_model.py, mock dataset generator | Member 2 |
| 2026-09-30 | Member 1 complete: camera, keypoints, preprocessing, sequence buffer, dataset script & 6 unit tests | Member 1 |
| 2026-09-30 | Phase 0 setup: created CONTRACTS.md, PROJECT_STATUS.md, requirements.txt, folder structure | Phase 0 |

