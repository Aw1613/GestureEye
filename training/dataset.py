import os
import glob
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SignDataset(Dataset):
    def __init__(self, data_dir, labels_dict, apply_jitter=False):
        """
        Args:
            data_dir (str): Directory containing subdirectories for each sign.
            labels_dict (dict): Dictionary mapping string labels to integer IDs.
            apply_jitter (bool): Apply random mathematical noise to simulate different body sizes.
        """
        self.data_dir = data_dir
        self.labels_dict = labels_dict
        self.apply_jitter = apply_jitter
        self.samples = []
        
        # Load all .npy files from the data directory
        for label_name, label_id in self.labels_dict.items():
            label_dir = os.path.join(self.data_dir, label_name)
            if os.path.exists(label_dir):
                file_pattern = os.path.join(label_dir, "*.npy")
                for file_path in glob.glob(file_pattern):
                    self.samples.append((file_path, label_id))
                    
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        file_path, label_id = self.samples[idx]
        
        # Load the sequence. Expected shape: (30, 126)
        sequence = np.load(file_path).astype(np.float32)
        
        # --- HACKATHON FEATURE: Data Augmentation ---
        # Adds realistic noise and scaling to simulate different users and camera angles
        if self.apply_jitter:
            noise = np.random.normal(loc=0.0, scale=0.015, size=sequence.shape)
            sequence = sequence + noise
            scale = np.random.uniform(0.9, 1.1)
            sequence = sequence * scale

        # Convert to torch tensor
        sequence_tensor = torch.tensor(sequence, dtype=torch.float32)
        label_tensor = torch.tensor(label_id, dtype=torch.long)
        
        return sequence_tensor, label_tensor

def get_dataloader(data_dir, labels_dict, batch_size=32, shuffle=True, apply_jitter=False):
    dataset = SignDataset(data_dir, labels_dict, apply_jitter=apply_jitter)
    if len(dataset) == 0:
        print(f"Warning: No data found in {data_dir}. Ensure data/raw/ has valid .npy files.")
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
