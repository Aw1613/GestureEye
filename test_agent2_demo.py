import sys
import os
import numpy as np
import time

# Ensure Python can find the 'app' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.recognition.inference import ModelInference

def run_mock_demo():
    print("=========================================")
    print("   SIGN-BRIDGE: AGENT 2 MOCK DEMO        ")
    print("=========================================\n")
    
    print("[System] Loading LSTM Model and Vocabulary...")
    try:
        recognizer = ModelInference(
            model_path="models/sign_model.pth", 
            labels_path="models/labels.json"
        )
        print("[System] Model loaded successfully!\n")
    except Exception as e:
        print(f"[Error] Failed to load model: {e}")
        return

    print("[Agent 1] (Mock) Capturing 30 frames from webcam...")
    time.sleep(1)
    
    # Create a fake tensor of shape (30, 126) matching Contract B
    mock_sequence = np.random.rand(30, 126).astype(np.float32)
    print(f"[Agent 1] Sequence captured! Shape: {mock_sequence.shape}\n")
    
    print("[Agent 2] Passing sequence to LSTM model for inference...")
    time.sleep(1)
    
    # Run the model
    prediction = recognizer.predict(mock_sequence)
    
    print("\n=========================================")
    print("   MODEL PREDICTION OUTPUT (CONTRACT C)  ")
    print("=========================================")
    import json
    print(json.dumps(prediction, indent=4))
    print("=========================================\n")
    print("Next step: Pass this JSON to Agent 3 to build a sentence!")

if __name__ == "__main__":
    run_mock_demo()
