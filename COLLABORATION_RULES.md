Hi Antigravity! I am collaborating with my teammate on a hackathon project. 
He created the repository under GitHub account `ujjwal-mahajan`. 

Here are the guidelines for how we will work together:

1. COMMUNICATION STYLE (VERY IMPORTANT):
   - Explain everything in plain, simple, beginner-friendly English. Avoid unnecessary technical jargon.
   - Before you run commands or modify files, give a 1-2 sentence preview: "Here is what I'm about to do and why."
   - After you finish a task, provide a quick plain-English summary:
     * What was changed or created
     * What it looks like / how it behaves in our app
     * What I should click or check in my browser to test it

2. WORKSPACE SETUP:
   - Check if the repository is already cloned in this workspace. If not, clone it:
     `git clone https://github.com/ujjwal-mahajan/Sign-Bridge.git`
     (or use SSH `git@github.com:ujjwal-mahajan/Sign-Bridge.git` if configured).
   - If already cloned or inside the repo folder, inspect the project.
   - Install dependencies (e.g. `npm install` or Python requirements).
   - If there is a `.env.example`, copy it to `.env` and let me know if any API keys are needed.
   - Run the local development server and confirm it works smoothly.

3. COLLABORATION & GIT PROTOCOL:
   - NEVER force push to `main`.
   - ALWAYS run `git pull origin main` before starting any new feature or edit.
   - Work on dedicated feature branches (e.g., `git checkout -b feature/<feature-name>`).
   - Before pushing, make sure the project builds without errors.
   - Write clear, concise commit messages.
   - Stay modular: avoid touching core files or files my teammate is actively editing.

Please acknowledge these instructions, inspect our setup, and explain what our next step is in simple terms!

---

REAL-TIME SIGN LANGUAGE TRANSLATOR
AGENT RESPONSIBILITIES + SYSTEM INSIGHT

AGENT 1 — INPUT / KEYPOINT AGENT

OWNERSHIP:
Everything from webcam input up to clean temporal keypoint sequences.

WORK:
- webcam capture
- MediaPipe integration
- hand landmark extraction
- optional future Holistic integration
- missing-hand handling
- coordinate normalization
- feature formatting
- rolling sequence buffer
- training-data capture utility
- tests

DO NOT OWN:
- model architecture
- sentence grammar
- TTS
- final UI

HANDOFF TO AGENT 2:
"Here is a sequence with exactly N frames and D features per frame."

WHAT THE SYSTEM CAN DO AFTER AGENT 1:
The computer can watch a person and turn their movements into numerical time-series data.

Example:
Person moves hand
→ camera frame
→ landmarks
→ normalized numbers
→ 30/60-frame sequence

At this point the system does NOT understand what the sign means.


AGENT 2 — DATASET / MODEL AGENT

OWNERSHIP:
Everything related to training and sign classification.

WORK:
- dataset inspection
- vocabulary selection
- label mapping
- dataset loader
- train/validation/test split
- augmentation
- LSTM/GRU baseline
- evaluation
- model saving/loading
- inference wrapper
- metrics

DO NOT OWN:
- webcam implementation
- sentence grammar
- TTS
- UI

HANDOFF TO AGENT 3:
"Given this sequence, the model returns a label and confidence."

WHAT THE SYSTEM CAN DO AFTER AGENT 2:
The system can recognize supported signs from keypoint sequences.

Example:
Keypoint sequence
→ temporal model
→ "thank_you"
→ 0.91 confidence

At this point it can recognize individual supported signs, but continuous sentence handling is not solved yet.


AGENT 3 — SENTENCE / SPEECH AGENT

OWNERSHIP:
Everything after model prediction until speech output.

WORK:
- prediction filtering
- confidence thresholding
- temporal stability
- duplicate suppression
- sign segmentation heuristic
- word buffer
- sentence smoothing
- sentence finalization
- TTS
- audio queue/state
- tests

DO NOT OWN:
- MediaPipe extraction
- model training
- main UI

HANDOFF TO AGENT 4:
"Here is the current sign, recognized words, sentence, confidence and system status."

WHAT THE SYSTEM CAN DO AFTER AGENT 3:
It can convert model predictions into usable language output.

Example:
Repeated noisy predictions
→ filtering
→ "hello"
→ "thank you"
→ "I need water"
→ spoken sentence

This is where the raw ML output becomes something understandable to a user.

Important:
The MVP should use simple sentence smoothing, not pretend to solve full sign-language grammar.


AGENT 4 — UI / INTEGRATION AGENT

OWNERSHIP:
Everything visible to the user and the final connection of all modules.

WORK:
- UI
- webcam display
- prediction overlay
- confidence display
- recognized-word display
- sentence display
- status/error messages
- module integration
- end-to-end testing
- demo mode
- demo instructions
- final reliability fixes

DO NOT OWN:
- core model training
- core keypoint extraction
- sentence logic
- TTS internals

WHAT THE SYSTEM CAN DO AFTER AGENT 4:
The complete MVP can be demonstrated live.

User:
signs

System:
sees sign
→ extracts movement
→ recognizes word
→ builds sentence
→ displays it
→ speaks it


HOW THE FOUR AGENTS FIT TOGETHER

AGENT 1
VIDEO
↓
KEYPOINT SEQUENCE

AGENT 2
KEYPOINT SEQUENCE
↓
SIGN + CONFIDENCE

AGENT 3
SIGN + CONFIDENCE
↓
STABLE WORDS
↓
SENTENCE
↓
SPEECH

AGENT 4
ALL OUTPUTS
↓
LIVE APPLICATION


WHAT EACH AGENT MUST HAND OVER

Agent 1:
- exact feature format
- exact sequence shape
- preprocessing rules
- example input
- tests

Agent 2:
- model file
- label mapping
- inference API
- expected input shape
- output format
- metrics

Agent 3:
- prediction-event contract
- sentence state
- TTS interface
- filtering rules
- tests

Agent 4:
- integrated application
- setup instructions
- demo instructions
- integration tests


WORK IS EQUAL BY RESPONSIBILITY, NOT BY FILE COUNT

Each agent must contribute:
1. implementation
2. tests
3. documentation
4. debugging
5. integration support

No agent should be considered "finished" simply because their main code file exists.


VALIDATION RESPONSIBILITY

Every agent validates:
- their own code
- their inputs
- their outputs
- their interface
- their tests
- their documentation

The lead/coordination process validates:
- cross-agent compatibility
- folder placement
- duplicate code
- broken imports
- end-to-end behavior


SIMPLE PROJECT STATUS FORMAT

At the end of each completed task:

What I changed:
...

Where:
...

How it works now:
...

How I tested it:
...

What you should check:
...

Next dependency:
...


COLLABORATION RULES

1. Before commands or file edits:
Give a 1–2 sentence plain-English preview.

2. After every completed task:
Give a simple-English summary.

3. Before starting new work:
Pull the latest main.

4. Use a dedicated feature branch.

5. Never force-push main.

6. Test/build before pushing.

7. Use clear commit messages.

8. Avoid modifying another agent's ownership area.

9. If a shared file must change:
Tell the team first and document the change.

10. Never silently change a contract.

11. Never create a second implementation of something that already exists.

12. Keep PROJECT_STATUS.md updated.

13. Keep CONTRACTS.md updated.

14. If blocked:
Explain the exact blocker and what information/action is needed.

15. If something fails:
Do not hide it. Record it and fix it before marking the task complete.

16. Use beginner-friendly English.

17. Explain technical words when they are necessary.

18. At every milestone validate that files are in the correct folder and imports/references point to the correct implementation.

19. Do not claim unrestricted sign-language translation if the MVP only supports a limited vocabulary.

20. Prefer a smaller working system over a large unfinished system.
