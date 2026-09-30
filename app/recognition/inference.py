import os
import json
import time
import torch
import numpy as np
from app.recognition.model import SignLanguageLSTM

class ModelInference:
    def __init__(self, model_path="models/sign_model.pth", labels_path="models/labels.json", confidence_threshold=0.60):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.confidence_threshold = confidence_threshold
        
        # Load labels
        if not os.path.exists(labels_path):
            raise FileNotFoundError(f"Labels file not found at {labels_path}")
            
        with open(labels_path, "r") as f:
            self.id_to_label = json.load(f)
            
        self.num_classes = len(self.id_to_label)
        
        # Initialize and load model
        self.model = SignLanguageLSTM(num_classes=self.num_classes).to(self.device)
        
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
        else:
            print(f"Warning: Model weights not found at {model_path}. Using untrained model.")
            
    def predict(self, sequence):
        """
        Predicts the sign from a sequence of frames.
        
        Args:
            sequence (np.ndarray): Shape (30, 126)
            
        Returns:
            dict: Prediction output following Contract C.
        """
        # Ensure correct shape
        if sequence.shape != (30, 126):
            raise ValueError(f"Expected sequence shape (30, 126), got {sequence.shape}")
            
        # Convert to tensor and add batch dimension: (1, 30, 126)
        sequence_tensor = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(sequence_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]
            
            # Get max probability and corresponding class index
            confidence, predicted_idx = torch.max(probabilities, 0)
            
            confidence = confidence.item()
            predicted_idx = str(predicted_idx.item())
            
            label = self.id_to_label.get(predicted_idx, "unknown")
            
        return {
            "label": label,
            "confidence": confidence,
            "timestamp": time.time()
        }
