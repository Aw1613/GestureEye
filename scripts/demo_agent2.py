import sys
import numpy as np
import time
sys.path.append('C:/Users/Ujjwal/Sign-Bridge')

from app.recognition.inference import ModelInference

print('--- INITIALIZING SIGN-BRIDGE (AGENT 2) ---')
recognizer = ModelInference(
    model_path='models/sign_model.pth',
    labels_path='models/labels.json'
)

print('\n[Agent 1] Capturing 30 frames from webcam...')
time.sleep(1.0)
# Mocking a sequence of 30 frames, 126 features each
mock_sequence = np.random.rand(30, 126).astype(np.float32)
print(f'[Agent 1] Sequence captured! Shape: {mock_sequence.shape}')

print('\n[Agent 2] Passing sequence to LSTM model for inference...')
time.sleep(1.0)
prediction = recognizer.predict(mock_sequence)

print('\n--- MODEL PREDICTION (CONTRACT C) ---')
import json
print(json.dumps(prediction, indent=4))
