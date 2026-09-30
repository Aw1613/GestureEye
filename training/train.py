import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from app.recognition.model import SignLanguageLSTM
from app.recognition.labels import VOCABULARY, NUM_CLASSES
from training.dataset import get_dataloader

def train_model(data_dir="data/processed", epochs=50, batch_size=32, lr=0.001, save_dir="models"):
    # Ensure save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Create labels mapping
    labels_dict = {label: idx for idx, label in enumerate(VOCABULARY)}
    
    # Save labels dict to models/labels.json if not exists
    labels_path = os.path.join(save_dir, "labels.json")
    with open(labels_path, "w") as f:
        # Save mapping from ID (string) to label
        id_to_label = {str(idx): label for label, idx in labels_dict.items()}
        json.dump(id_to_label, f, indent=4)
        
    print(f"Loading data from {data_dir}...")
    train_loader = get_dataloader(data_dir, labels_dict, batch_size=batch_size)
    
    if len(train_loader.dataset) == 0:
        print("No training data found. Exiting training loop.")
        return
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = SignLanguageLSTM(num_classes=NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    print(f"Starting training for {epochs} epochs...")
    model.train()
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        correct = 0
        total = 0
        
        for sequences, labels in train_loader:
            sequences, labels = sequences.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(sequences)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        avg_loss = epoch_loss / len(train_loader)
        accuracy = 100 * correct / total
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%")
            
    # Save the trained model
    model_path = os.path.join(save_dir, "sign_model.pth")
    torch.save(model.state_dict(), model_path)
    print(f"Training complete. Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
