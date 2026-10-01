import os
import torch
import torch.nn as nn
from app.recognition.model import SignLanguageLSTM
from app.recognition.labels import VOCABULARY, NUM_CLASSES
from training.dataset import get_dataloader

def evaluate_model(data_dir="data/processed", model_path="models/sign_model.pth", batch_size=32):
    if not os.path.exists(model_path):
        print(f"Error: Model weights not found at {model_path}. Run training first.")
        return

    labels_dict = {label: idx for idx, label in enumerate(VOCABULARY)}
    
    print(f"Loading data from {data_dir}...")
    test_loader = get_dataloader(data_dir, labels_dict, batch_size=batch_size, shuffle=False)
    
    if len(test_loader.dataset) == 0:
        print("No evaluation data found. Exiting.")
        return
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = SignLanguageLSTM(num_classes=NUM_CLASSES).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    criterion = nn.CrossEntropyLoss()
    
    total_loss = 0.0
    correct = 0
    total = 0
    
    print("Starting evaluation...")
    with torch.no_grad():
        for sequences, labels in test_loader:
            sequences, labels = sequences.to(device), labels.to(device)
            
            outputs = model(sequences)
            loss = criterion(outputs, labels)
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
    avg_loss = total_loss / len(test_loader)
    accuracy = 100 * correct / total
    
    print(f"Evaluation Complete!")
    print(f"Average Loss: {avg_loss:.4f}")
    print(f"Accuracy:     {accuracy:.2f}%")

if __name__ == "__main__":
    evaluate_model()
