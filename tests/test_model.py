import unittest
import numpy as np
import time
from app.recognition.inference import ModelInference

class TestModelInference(unittest.TestCase):
    def setUp(self):
        # We can initialize ModelInference even without a trained .pth file, 
        # it handles missing weights by falling back to untrained weights and printing a warning.
        self.recognizer = ModelInference(
            model_path="models/sign_model.pth", 
            labels_path="models/labels.json"
        )
        
    def test_inference_contract(self):
        """Test that the prediction output perfectly matches Contract C"""
        # Create a mock sequence matching Contract B: (30, 126)
        mock_sequence = np.random.rand(30, 126).astype(np.float32)
        
        # Run prediction
        prediction = self.recognizer.predict(mock_sequence)
        
        # Validate Contract C dictionary keys
        self.assertIn("label", prediction)
        self.assertIn("confidence", prediction)
        self.assertIn("timestamp", prediction)
        
        # Validate data types
        self.assertIsInstance(prediction["label"], str)
        self.assertIsInstance(prediction["confidence"], float)
        self.assertIsInstance(prediction["timestamp"], float)
        
        # Validate ranges
        self.assertTrue(0.0 <= prediction["confidence"] <= 1.0)
        
        # Ensure timestamp is recent
        self.assertTrue(time.time() - prediction["timestamp"] < 5.0)

if __name__ == "__main__":
    unittest.main()
