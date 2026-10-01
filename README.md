# SignBridge 🌉

![SignBridge Header](https://img.shields.io/badge/Status-Development-yellow.svg)
![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**SignBridge** is a real-time, AI-powered Indian Sign Language (ISL) communication assistant designed to bridge the gap between sign language and spoken communication. 

By leveraging computer vision and machine learning, SignBridge translates a defined vocabulary of Indian Sign Language into text and spoken sentences in real-time directly through your webcam.

---

## 🎯 Project Goal
The core goal of this project is to create an accessible Minimum Viable Product (MVP) that translates a **defined vocabulary** of signs into continuous words and sentences without heavy latency. 

*Note: The MVP does not claim universal sign-language translation, but rather serves as a foundational step toward accessible real-time ISL interpretation.*

## ⚙️ Architecture & Tech Stack

SignBridge is built with modularity and real-time performance in mind. The system follows a strict, asynchronous data pipeline:

1. **Webcam Capture:** High-performance, unblocked frame capture.
2. **MediaPipe Keypoint Extraction:** Fast, CPU-friendly body/hand landmark detection.
3. **Rolling Sequence Window:** Normalizing and packaging temporal frames.
4. **Temporal ML Model (LSTM/GRU):** Recognizing signs from sequential motion data.
5. **Temporal Filtering & Sentence Building:** Smoothing model confidence and constructing coherent phrases.
6. **Text & Text-to-Speech (TTS) UI:** Providing instant auditory and visual feedback.

> 📖 *For a deep dive into the engineering specifications, data contracts, and module ownership, please read the [ARCHITECTURE.md](./ARCHITECTURE.md).*

## 📂 Repository Structure

The project code is organized into modular domains:

```text
SignBridge/
├── app/
│   ├── capture/        # Webcam interface
│   ├── keypoints/      # MediaPipe extraction & preprocessing
│   ├── recognition/    # Inference & model loading
│   ├── sentence/       # Temporal filtering & word buffering
│   ├── tts/            # Text-to-Speech engine
│   └── ui/             # Real-time user interface
├── data/               # Raw and processed training datasets
├── models/             # Saved PyTorch/TF models
├── training/           # Scripts for dataset building and model training
└── tests/              # Unit and integration tests
```

## 🤝 Collaboration & Contribution
This repository is being actively developed by a team of 4 collaborators (including AI agents). We follow strict module ownership rules to prevent merge conflicts and ensure code quality.

Please read the [COLLABORATION_RULES.md](./COLLABORATION_RULES.md) before pushing to the `main` branch. 

### Quick Rules:
- **Do not** block the webcam capture thread with TTS or UI operations.
- **Do not** silently change shared data contracts (e.g., Sequence shape).
- Always ensure the real-time inference loop stays lightweight.

## 🚀 Getting Started
 
### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install pytest pyttsx3
```

### 2. Launch the Live Application (Agent 4 UI & Integration)
```bash
# Live webcam mode with OpenCV real-time HUD dashboard:
python scripts/run_app.py

# Presentation / screen-share mode without physical webcam:
python scripts/run_app.py --mock

# Automated live demo tour with simulation and speech playback:
python scripts/demo_agent4.py
```

### 3. Keyboard Controls During Live Execution

| Key | Action | Description |
|:---:|:---|:---|
| **`S`** | **Speak Sentence** | Asynchronously speaks smoothed sentence via TTS in $< 0.001\text{s}$ (non-blocking). |
| **`C`** | **Clear Buffer** | Wipes the word buffer and resets the smoothed sentence and stability filter. |
| **`Backspace`** / **`B`** | **Undo Last Word** | Deletes the last accepted word and recalculates sentence grammar. |
| **`M`** | **Toggle Camera Mode** | Switches dynamically between physical webcam and synthetic mock camera. |
| **`1` – `5`** | **Quick Signs** | Injects 5 consecutive agreeing frames: `1: hello`, `2: thank_you`, `3: please`, `4: water`, `5: help`. |
| **`Q`** / **`ESC`** | **Quit** | Cleanly terminates threads, camera capture, and closes the application window. |

### 4. Run the Full Test Suite (39 Tests Across All Agents)
```bash
python -m pytest tests/ -v
```

> 📖 *For a complete judge presentation guide, rehearsal script, and panel breakdowns, read [docs/DEMO_INSTRUCTIONS.md](./docs/DEMO_INSTRUCTIONS.md).*
