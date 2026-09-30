import os
import glob
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SignDataset(Dataset):
    def __init__(self, data_dir, labels_dict):
        """
        Args:
            data_dir (str): Directory containing subdirectories for each sign.
            labels_dict (dict): Dictionary mapping string labels to integer IDs.
        """
        self.data_dir = data_dir
        self.labels_dict = labels_dict
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
        sequence = np.load(file_path)
        
        # Convert to torch tensor
        sequence_tensor = torch.tensor(sequence, dtype=torch.float32)
        label_tensor = torch.tensor(label_id, dtype=torch.long)
        
        return sequence_tensor, label_tensor

def get_dataloader(data_dir, labels_dict, batch_size=32, shuffle=True):
    dataset = SignDataset(data_dir, labels_dict)
    if len(dataset) == 0:
        print(f"Warning: No data found in {data_dir}. Ensure data/processed/ has valid .npy files.")
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
