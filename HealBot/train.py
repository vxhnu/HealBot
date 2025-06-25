import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet

# Hyperparameters
hidden_size = 16
batch_size = 8
learning_rate = 0.001
num_epochs = 1000

# Load intents
with open("intents.json", "r") as f:
    intents = json.load(f)

all_words, tags, xy = [], [], []
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore = ["?", "!", ".", ","]
all_words = sorted(set(stem(w) for w in all_words if w not in ignore))
tags = sorted(set(tags))

X_train, y_train = [], []
for (pattern_sentence, tag) in xy:
    X_train.append(bag_of_words(pattern_sentence, all_words))
    y_train.append(tags.index(tag))

X_train = np.array(X_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.int64)

class ChatDataset(Dataset):
    def __init__(self):
        self.x_data = torch.from_numpy(X_train)
        self.y_data = torch.from_numpy(y_train)
    def __getitem__(self, idx):
        return self.x_data[idx], self.y_data[idx]
    def __len__(self):
        return len(self.x_data)

dataset = ChatDataset()
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNet(len(all_words), hidden_size, len(tags)).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for words, labels in loader:
        words, labels = words.to(device), labels.to(device)
        outputs = model(words)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if (epoch+1) % 100 == 0:
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")

data_to_save = {
    "input_size": len(all_words),
    "hidden_size": hidden_size,
    "output_size": len(tags),
    "all_words": all_words,
    "tags": tags,
    "model_state": model.state_dict()
}
torch.save(data_to_save, "data_rnn.pth")
print("Training complete. Model saved as data_rnn.pth")
