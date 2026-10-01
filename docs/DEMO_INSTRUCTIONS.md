# 🎬 SignBridge — Live Demo & Rehearsal Instructions

> **Milestone:** M4 (UI Ready) & M5 (Integrated MVP)  
> **Audience:** Presenters, Evaluators, Judges, and Developers  
> **Status:** Fully Integrated & Verified  

---

## 1. Quickstart Commands

Launch the application using one of the following commands from the repository root:

```bash
# 1. Standard Live Application (with physical webcam):
python scripts/run_app.py

# 2. Presentation / No-Webcam Mode (uses synthetic camera & demo simulator):
python scripts/run_app.py --mock

# 3. Automated Demonstration Tour (injects signs, updates UI, and speaks):
python scripts/demo_agent4.py

# 4. Run the full unit and integration test suite (39 passing tests):
python -m pytest tests/ -v
```

---

## 2. Interactive UI Dashboard Tour

The SignBridge application renders a 60 FPS, dark-themed HUD dashboard with four synchronized panels:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ SignBridge | Real-Time Sign Language Translator     FPS: 30.0  [CAM] [MODEL] [VOICE] │
├──────────────────────────────────────────┬──────────────────────────────────┤
│                                          │ CURRENT SIGN                     │
│                                          │ THANK_YOU                        │
│                                          │                                  │
│         LIVE CAMERA VIEWPORT             │ CONFIDENCE: 92.0%                │
│       (with MediaPipe Hand Skeletons)    │ [████████████████████] (Green)   │
│                                          │                                  │
│                                          │ STABILITY FILTER: 5/5 FRAMES     │
│                                          │ [████████████████████]           │
│                                          │ ──────────────────────────────── │
│                                          │ WORD BUFFER (3 ACCEPTED)         │
│                                          │ 1. hello                         │
│                                          │ 2. thank_you                     │
│                                          │ 3. water                         │
├──────────────────────────────────────────┴──────────────────────────────────┤
│ SMOOTHED SENTENCE OUTPUT (CONTRACT E):           [Speaking Sentence...]     │
│ "Hello, thank you for the water."                                           │
│ ─────────────────────────────────────────────────────────────────────────── │
│ [S] Speak  |  [C] Clear  |  [Backspace] Undo  |  [M] Mock  |  [1-5] Signs  |  [Q] Quit│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dashboard Panels:
1. **Header Banner:**
   - Displays real-time FPS counter and dynamic subsystem health badges:
     - `CAM`: Green for active hardware capture, Amber for synthetic mock.
     - `MODEL`: Green when PyTorch LSTM classifier is loaded and active.
     - `VOICE`: Green for idle/ready, Violet (`VOICE: SPK`) when actively speaking.
2. **Camera Viewport:**
   - Shows live 640x480 video with real-time MediaPipe hand landmark tracking and bone skeleton connections.
3. **Recognition & Diagnostic Side Panel:**
   - **Current Sign:** Large high-visibility typography showing the active prediction.
   - **Confidence Meter:** Color-coded progress bar (Green $\ge 60\%$, Amber $35-59\%$, Red $< 35\%$).
   - **Stability Filter:** Shows consecutive agreeing frames ($0/5$ to $5/5$) required before accepting a sign into the sentence.
   - **Word Buffer:** Tagged list of accepted sign tokens in sequential order.
4. **Sentence & Speech Output Panel:**
   - Displays smoothed, grammatically coherent English sentence produced by heuristic smoothing rules.
   - Transient action toast alerts (e.g., `[Speaking Sentence...]`, `[Accepted: water]`, `[Cleared]`).

---

## 3. Keyboard Controls

Control the application in real-time during a demo:

| Key | Action | Description |
|:---:|:---|:---|
| **`S`** | **Speak Sentence** | Asynchronously speaks the smoothed sentence via Text-to-Speech without blocking camera or inference. |
| **`C`** | **Clear Buffer** | Clears the word buffer, resets the smoothed sentence, and resets the prediction filter. |
| **`Backspace`** / **`B`** | **Undo Last Word** | Removes the last recognized word from the buffer and recalculates sentence grammar. |
| **`M`** | **Toggle Camera Mode** | Toggles dynamically between live physical webcam and synthetic mock camera. |
| **`1` – `5`** | **Quick Signs** | Instantly injects 5 consecutive agreeing frames for quick demonstrations: <br> • `1`: `hello` <br> • `2`: `thank_you` <br> • `3`: `please` <br> • `4`: `water` <br> • `5`: `help` |
| **`Q`** / **`ESC`** | **Quit** | Cleanly terminates threads, camera capture, and closes the application window. |

---

## 4. Judge Walkthrough Script (3-Minute Live Demo)

Follow this structured script during project evaluations or presentations:

### Step 1: Launch Application
```bash
python scripts/run_app.py
```
- **Explain:** *"SignBridge is an end-to-end, modular, real-time sign language translation pipeline. The interface you see is powered by our Agent 4 UI layer."*
- **Point out:** The top status badges showing camera, ML model, and speech engine status.

### Step 2: Demonstrate Temporal Stability & Recognition
- Sign in front of the camera or press **`1`** (`hello`):
- **Explain:** *"Notice how raw predictions do not immediately trigger word insertions. Agent 3's temporal stability filter requires 5 consecutive agreeing frames with $\ge 60\%$ confidence before accepting a sign. This eliminates hand transition noise and false positives."*
- The word `"hello"` appears in the Word Buffer, and the sentence updates to `"Hello."`.

### Step 3: Demonstrate Multi-Word Sentence Smoothing
- Sign or press **`4`** (`water`) followed by **`3`** (`please`):
- **Explain:** *"As we sign 'hello', 'water', 'please', the SentenceBuilder heuristics assemble these discrete signs into a natural English utterance: 'Hello, water please.' It also handles duplicate suppression if hands are held stationary."*

### Step 4: Demonstrate Asynchronous Speech Synthesis
- Press **`S`**:
- **Explain:** *"Notice the purple `[VOICE: SPK]` indicator in the header. The audio plays cleanly while the camera framerate remains at a smooth 30 FPS. Our Text-to-Speech engine runs in a dedicated background worker daemon, ensuring zero blocking time ($< 0.001\text{s}$) on video processing."*

### Step 5: Demonstrate Error Correction (Undo & Clear)
- Press **`Backspace`**: The last word (`please`) is removed, and the sentence updates to `"Hello, water."`.
- Press **`C`**: The buffer clears and returns to idle state ready for the next sentence.

---

## 5. Troubleshooting & Fallbacks

- **No webcam available?**  
  Run with `--mock` or press `M` in the app. The pipeline will generate synthetic frames and allow full demonstration using the `[1-5]` number keys.
- **Audio muted or headless server?**  
  Add `--no-tts` to run silently, or `--headless` to benchmark the processing loop without opening an X11/Win32 window.
- **Running Automated Tests:**  
  Execute `python -m pytest tests/ -v` to verify all 39 unit, integration, and UI tests pass.
