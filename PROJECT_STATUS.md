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
| M1 | Input Ready (stable keypoints) | NOT STARTED | Member 1 |
| M2 | ML Ready (trained classifier) | NOT STARTED | Member 2 |
| M3 | Logic + Speech Ready (sentence + audio) | NOT STARTED | Member 3 |
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
| Vocabulary selected | NOT STARTED | Pending Agent 2 dataset inspection |

---

## M1 — Input Ready (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| Webcam capture module | NOT STARTED | app/capture/camera.py |
| MediaPipe Hands integration | NOT STARTED | app/keypoints/extractor.py |
| Landmark preprocessing | NOT STARTED | app/keypoints/preprocessing.py |
| Rolling sequence buffer | NOT STARTED | |
| Data collection utility | NOT STARTED | scripts/ |
| Unit tests | NOT STARTED | tests/ |
| Contract documentation verified | NOT STARTED | CONTRACTS.md Section 2-3 |

---

## M2 — ML Ready (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| Dataset inspection | NOT STARTED | |
| Vocabulary selection (20-30 signs) | NOT STARTED | |
| Label mapping | NOT STARTED | app/recognition/labels.py |
| Dataset loader | NOT STARTED | training/dataset.py |
| Train/val/test split | NOT STARTED | |
| LSTM/GRU model | NOT STARTED | app/recognition/model.py |
| Training pipeline | NOT STARTED | training/train.py |
| Evaluation | NOT STARTED | training/evaluate.py |
| Model export | NOT STARTED | models/ |
| Inference wrapper | NOT STARTED | app/recognition/inference.py |

---

## M3 — Logic + Speech Ready (NOT STARTED)

| Task | Status | Notes |
|------|--------|-------|
| Prediction filter | NOT STARTED | app/sentence/filter.py |
| Sign segmentation | NOT STARTED | app/sentence/segmentation.py |
| Word buffer | NOT STARTED | |
| Sentence builder | NOT STARTED | app/sentence/builder.py |
| TTS integration | NOT STARTED | app/tts/speech.py |
| Non-blocking speech | NOT STARTED | |
| Unit tests | NOT STARTED | tests/ |

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
| Vocabulary not yet selected | M2 (model training) | Waiting for dataset inspection |

---

## Recent Updates

| Date | Update | By |
|------|--------|----|
| 2026-09-30 | Phase 0 setup: created CONTRACTS.md, PROJECT_STATUS.md, requirements.txt, folder structure | Phase 0 |
