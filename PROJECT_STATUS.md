# SignBridge — Project Status

> **Purpose:** Living document that tracks milestone progress, blockers,
> and ownership status. Updated by all agents as work progresses.

---

## Current Phase: Phase 0 — Architecture Ready

---

## Milestone Tracker

| Milestone | Description | Status | Owner |
|-----------|-------------|--------|-------|
| M0 | Architecture Ready | IN PROGRESS | All |
| M1 | Input Ready (stable keypoints) | DONE | Member 1 |
| M2 | ML Ready (trained classifier) | DONE | Member 2 |
| M3 | Logic + Speech Ready (sentence + audio) | DONE | Member 3 |
| M4 | UI Ready (live interface) | DONE | Member 4 |
| M5 | Integrated MVP | DONE | All |
| M6 | Demo Hardening | DONE | All |

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
| Webcam capture module | DONE | app/capture/camera.py |
| MediaPipe Hands integration | DONE | app/keypoints/extractor.py |
| Landmark preprocessing | DONE | app/keypoints/preprocessing.py |
| Rolling sequence buffer | DONE | |
| Data collection utility | DONE | scripts/ |
| Unit tests | DONE | tests/ |
| Contract documentation verified | DONE | CONTRACTS.md Section 2-3 |

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
| Prediction filter | DONE | app/sentence/filter.py |
| Sign segmentation | DONE | app/sentence/segmentation.py |
| Word buffer | DONE | |
| Sentence builder | DONE | app/sentence/builder.py |
| TTS integration | DONE | app/tts/speech.py |
| Non-blocking speech | DONE | |
| Unit tests | DONE | tests/ |

---

## M4 — UI Ready (DONE)

| Task | Status | Notes |
|------|--------|-------|
| UI layout | DONE | app/ui/app.py |
| Camera feed display | DONE | |
| Prediction overlay | DONE | |
| Confidence display | DONE | |
| Word/sentence display | DONE | |
| System status indicators | DONE | |
| Start/stop/reset controls | DONE | |

---

## M5 — Integrated MVP (DONE)

| Task | Status | Notes |
|------|--------|-------|
| End-to-end pipeline connection | DONE | |
| Integration tests | DONE | |
| Performance verification | DONE | |

---

## M6 — Demo Hardening (DONE)

| Task | Status | Notes |
|------|--------|-------|
| Error handling | DONE | |
| Demo rehearsal | DONE | |
| Demo script/instructions | DONE | docs/ |
| Final bug fixes | DONE | |

---

## Blockers

| Blocker | Affects | Status |
|---------|---------|--------|
| Vocabulary not yet selected | M2 (model training) | Waiting for dataset inspection |

---

## Recent Updates

| Date | Update | By |
|------|--------|----|
| 2026-09-30 | Phase 0 setup: created CONTRACTS.md, PROJECT_STATUS.md, requirements.txt, folder structure | Phase 0 |

