# 🤖 HealBot – Your Friendly Symptom Checker Chatbot

HealBot is an AI-powered chatbot that helps users understand their symptoms, provides casual and supportive health advice, and can even suggest nearby hospitals using your location. It's like having a virtual health buddy — not a doctor, but helpful when you need guidance.

---

## 🔧 Features
- 💬 Natural chat interface for symptom checking
- 🧠 AI-trained intent recognition using PyTorch
- 📍 Finds nearby hospitals via Google Maps API
- 📝 Easily customizable via `intents.json`


# ▶️ How to Run the Program

Follow these steps to set up and run **HealBot** on your local machine.

---

## 1. 📦 Clone the Repository

If you haven’t already:

```bash
git clone https://github.com/your-username/healbot.git
cd healbot
```

---

## 2. 🐍 Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate       # On Windows
```

---

## 3. 📥 Install Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

---

## 4. 🔐 Set Up Your Google API Key

1. Get a Google Places API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create a `.env` file in the root folder:

```
GOOGLE_PLACES_API_KEY=your_actual_api_key_here
```

---

## 5. 📚 Download NLTK Data

Run this once to download required tokenizer files:

```python
import nltk
nltk.download('punkt')
```

---

## 6. 🧠 Train the Chatbot Model

This will generate the file `data_rnn.pth`:

```bash
python train.py
```

> ✅ You only need to retrain if you update `intents.json`.

---

## 7. 🚀 Launch the Web App

Run the Flask server:

```bash
python app.py
```

Once running, open your browser and go to:

```
http://localhost:5000
```

---

## 8. 📍 Using the Hospital Locator Feature

- Click the **“Find Hospitals Near Me”** button.
- Allow location access in your browser.
- HealBot will list the top 5 nearby hospitals.
- 🔗 Clickable addresses open directly in **Google Maps**.

---

## 9. ✅ You're All Set!

You can now chat with HealBot, check symptoms, get health tips, and locate nearby hospitals — all from your browser!

---

> 💡 Tip: Customize the chatbot by editing `intents.json`, then re-run `train.py`.
