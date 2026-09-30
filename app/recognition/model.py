import torch
import torch.nn as nn

class SignLanguageLSTM(nn.Module):
    def __init__(self, input_dim=126, hidden_dim=64, num_layers=2, num_classes=20, dropout=0.2):
        super(SignLanguageLSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Temporal feature extraction
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        
        # Classification head
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes)
        )
        
    def forward(self, x):
        # x shape: (batch_size, sequence_length, input_dim) -> (B, 30, 126)
        
        # lstm_out shape: (B, 30, hidden_dim)
        # hidden state shape: (num_layers, B, hidden_dim)
        lstm_out, (h_n, c_n) = self.lstm(x)
        
        # We take the output of the last time step for classification
        last_out = lstm_out[:, -1, :] # Shape: (B, hidden_dim)
        
        # Pass through fully connected layers
        out = self.fc(last_out) # Shape: (B, num_classes)
        
        return out
