import random
import json
import torch
from nltk_utils import tokenize, bag_of_words
from model import NeuralNet

# Load intents
with open("intents.json", "r") as f:
    intents = json.load(f)

# Load trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
data = torch.load("data_rnn.pth", map_location=device)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def get_response(user_msg):
    tokens = tokenize(user_msg)
    bow = bag_of_words(tokens, all_words)
    bow = bow.reshape(1, bow.shape[0])
    bow_tensor = torch.from_numpy(bow).float().to(device)

    output = model(bow_tensor)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.5:
        if tag == "medical_centers":
            return "Sure—let me find hospitals near you! Click the button below."
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
    return "I'm sorry, I didn't understand. Could you rephrase?"
