# 🤝 SignBridge — Team Collaboration & Agent Workflow Rules

> **Project:** SignBridge (Real-Time Sign Language Translator)  
> **Repository:** [ujjwal-mahajan/Sign-Bridge](https://github.com/ujjwal-mahajan/Sign-Bridge)  
> **Purpose:** Guidelines for team communication, git protocol, agent ownership, and project standards.

---

## 1. 💬 Communication Style & Guidelines

To make collaboration smooth and beginner-friendly, all contributors and AI agents must follow these communication standards:

1. **Simple, Plain English:**
   - Explain all concepts and changes in easy-to-understand, beginner-friendly language.
   - Avoid unnecessary technical jargon. When a technical term is required, explain it briefly.

2. **Pre-Action Previews:**
   - Before executing terminal commands or modifying files, provide a 1–2 sentence preview:  
     *"Here is what I am about to do and why."*

3. **Post-Task Summaries:**
   - After completing each task, provide a concise summary covering:
     - **What was changed or created**: The files and features touched.
     - **How it behaves**: What this means for the application.
     - **How to verify/test**: Step-by-step instructions on what to check or test.

4. **Transparent Problem Reporting:**
   - If an error occurs or a task gets blocked, explain the root cause and what specific information or action is needed to resolve it. Never hide failures.

---

## 2. 👥 Agent Roles & Ownership Matrix

Each agent owns a distinct portion of the system. Responsibilities are strictly partitioned to prevent overlapping work and merge conflicts:

| Agent | Role Title | Ownership Scope | Must NOT Own |
|---|---|---|---|
| **Agent 1** | **Input / Keypoint Agent** | Camera capture (`app/capture/`), MediaPipe hand keypoints (`app/keypoints/extractor.py`), coordinate normalization (`app/keypoints/preprocessing.py`), rolling sequence buffer, dataset capture script (`scripts/collect_data.py`), CV tests. | Model architecture, grammar/sentence logic, TTS, final UI layout. |
| **Agent 2** | **Dataset / Model Agent** | Dataset inspection & loading (`training/dataset.py`), vocabulary & label mapping (`app/recognition/labels.py`), temporal model (LSTM/GRU in `app/recognition/model.py`), training pipeline (`training/train.py`), model evaluation & export, inference wrapper (`app/recognition/inference.py`). | Camera capture, sentence builder, TTS, UI layout. |
| **Agent 3** | **Sentence / Speech Agent** | Prediction filtering & confidence thresholding (`app/sentence/filter.py`), temporal stability & duplicate suppression, sign segmentation heuristic (`app/sentence/segmentation.py`), word buffer, basic sentence smoothing (`app/sentence/builder.py`), offline text-to-speech (`app/tts/speech.py`), audio queue. | MediaPipe extraction, model training, main UI layout. |
| **Agent 4** | **UI / Integration Agent** | Live demonstration UI (`app/ui/app.py`), camera feed rendering with landmark overlay, real-time sign & confidence display, recognized word buffer visualization, sentence display, system health status indicators, end-to-end integration testing. | Core model training, raw keypoint math, sentence logic internals. |

---

## 3. 🔄 How the 4 Agents Fit Together

The data moves sequentially through four well-defined handoffs:

```text
[Signing User]
       │
       ▼
 📷 Camera Frame Capture (Agent 1)
       │
       ▼
 🤚 MediaPipe Hand Landmarks & Normalization (Agent 1)
       │
       ▼
 📦 Rolling Sequence Buffer [N frames × D features] (Agent 1 → Agent 2)
       │
       ▼
 🧠 Temporal Model (LSTM/GRU) Inference (Agent 2 → Agent 3)
       │  └─ Returns: {"label": "thank_you", "confidence": 0.91}
       │
       ▼
 🔄 Prediction Filtering & Stability Check (Agent 3)
       │
       ▼
 📝 Word Buffer & Sentence Builder (Agent 3 → Agent 4)
       │  ├─ Sends text & state to UI (Agent 4)
       │  └─ Sends sentence to non-blocking TTS (Agent 3)
       │
       ▼
 🖥️ Live User Interface + 🔊 Spoken Audio Output
```

### Handoff Deliverables

- **Agent 1 → Agent 2:** Exact feature vector shape, normalization rules, and fixed sequence length $N$ documented in `CONTRACTS.md`.
- **Agent 2 → Agent 3:** Exported model file, label map, input requirements, and inference API returning `{"label": str, "confidence": float, "timestamp": float}`.
- **Agent 3 → Agent 4:** Formatted sentence data `{"words": list[str], "text": str}`, status flags, and responsive non-blocking speech.
- **Agent 4 → Users:** Integrated live application with clear visual feedback, camera view, and simple run instructions.

---

## 4. 🌿 Git & Collaboration Protocol

To maintain code safety and avoid accidental loss of work:

1. **Never Force-Push to `main`:**
   - Under no circumstances should `git push --force` or `git push -f` be used on `main`.
2. **Always Pull Before Editing:**
   - Always run `git pull origin main` before starting a new feature or making edits.
3. **Use Dedicated Feature Branches:**
   - Branch naming format: `agent-<number>-<feature>` or `feature/<feature-name>`.
   - Examples: `agent-1-cv`, `agent-2-model`, `feature/collab-rules`.
4. **Test Before Committing:**
   - Ensure the application builds and tests pass cleanly before creating a commit.
5. **Write Clear Commit Messages:**
   - Use clear, descriptive messages (e.g., `feat(keypoints): add wrist-relative normalization`).
6. **Stay Modular:**
   - Do not edit files outside your assigned module without informing the team and documenting interface changes in `CONTRACTS.md`.

---

## 5. 📜 The 20 Team Collaboration Rules

1. **Preview Before Action:** Give a 1–2 sentence plain-English preview before running commands or editing files.
2. **Summarize After Completion:** Provide a simple-English summary after finishing any task.
3. **Pull Before Work:** Always pull the latest `main` branch before starting any new work.
4. **Dedicated Branches:** Always use a dedicated feature or agent branch.
5. **Protect Main:** Never force-push to `main`.
6. **Build & Test First:** Ensure the project builds without errors before pushing commits.
7. **Descriptive Commits:** Write clear, concise, and informative commit messages.
8. **Respect Ownership:** Avoid modifying another agent's assigned codebase area.
9. **Announce Shared Changes:** If a shared file (such as `CONTRACTS.md` or `ARCHITECTURE.md`) must change, notify the team first.
10. **Lock Contracts Early:** Never silently change a data structure, vector dimension, or API contract.
11. **No Duplicate Code:** Never create a second implementation of an existing module or utility.
12. **Update Status Regularly:** Keep `PROJECT_STATUS.md` updated as tasks progress.
13. **Sync Documentation:** Keep `CONTRACTS.md` synchronized whenever a schema or shape changes.
14. **Be Explicit When Blocked:** If blocked, specify exactly what dependency or information is required.
15. **Record Failures Openly:** Document bugs and failed tests openly so they can be resolved systematically.
16. **Use Beginner-Friendly English:** Maintain clear, accessible language in all reports and explanations.
17. **Define Technical Terms:** Briefly explain technical concepts when they are necessary.
18. **Verify Directory Structure:** Check that files and imports remain in their correct directories at every milestone.
19. **Scope Honesty:** Acknowledge MVP limitations; do not claim universal sign translation when the scope covers a controlled 20–30 sign vocabulary.
20. **Working MVP Over Complexity:** Prioritize a reliable, stable, end-to-end working system over unfinished complex features.

---

## 6. 📋 Standard Project Status Handoff Template

When completing a task or handing off to another agent, use this template:

```markdown
### Task Completion Handoff

- **What I changed:**
  <Simple description of the changes>

- **Where:**
  <File paths modified or created>

- **How it works now:**
  <Plain-English explanation of the new behavior>

- **How I tested it:**
  <Command or procedure used to verify the change>

- **What you should check:**
  <Exact steps for the next person or reviewer to see it work>

- **Next dependency:**
  <Which agent or task is needed next>
```
