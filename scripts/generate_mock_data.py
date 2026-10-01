import os
import numpy as np
from app.recognition.labels import VOCABULARY

data_dir = 'data/processed'

# Generate 5 fake sequences for each class
for label in VOCABULARY:
    label_dir = os.path.join(data_dir, label)
    os.makedirs(label_dir, exist_ok=True)
    
    for i in range(5):
        # Create a (30, 126) sequence
        sequence = np.random.rand(30, 126).astype(np.float32)
        
        # Save it
        file_path = os.path.join(label_dir, f'sample_{i}.npy')
        np.save(file_path, sequence)

print('Generated mock dataset!')
