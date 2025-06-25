import os
import requests
from flask import Flask, render_template, request, jsonify
from chat import get_response
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Chatbot prediction route
@app.route("/predict", methods=["POST"])
def predict():
    user_msg = request.json.get("message", "")
    response = get_response(user_msg)
    return jsonify({"response": response})

# Hospital search using Google Places API
@app.route("/hospitals", methods=["POST"])
def hospitals():
    from urllib.parse import quote

    data = request.json
    lat, lon = data.get("lat"), data.get("lon")
    print("✅ Received coordinates:", data)

    # Construct Google Places API URL
    url = (
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={lat},{lon}"
        "&radius=5000"
        "&type=hospital"
        f"&key={GOOGLE_API_KEY}"
    )
    print("🌐 Request URL:", url)

    # Make request to Google
    res = requests.get(url).json()
    print("📦 Google Response:", res)

    hospitals = []
    for place in res.get("results", [])[:5]:
        name = place.get("name")
        addr = place.get("vicinity")
        full_address = f"{name} {addr}"
        map_link = f"https://www.google.com/maps/search/{quote(full_address)}"
        hospitals.append(f'<a href="{map_link}" target="_blank">{name} — {addr}</a>')

    # Send the hospital list back to JS
    return jsonify({"hospitals": hospitals})

if __name__ == "__main__":
    print("🚀 Using API Key:", GOOGLE_API_KEY)
    app.run(debug=True)














# import os
# import requests
# from flask import Flask, render_template, request, jsonify
# from chat import get_response
# from dotenv import load_dotenv

# # Load the API key from .env
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# # Initialize Flask app
# app = Flask(__name__)

# @app.route("/")
# def home():
#     return render_template("index.html")

# # Chatbot prediction route
# @app.route("/predict", methods=["POST"])
# def predict():
#     user_msg = request.json.get("message", "")
#     response = get_response(user_msg)
#     return jsonify({"response": response})

# # Hospital search using Google Places API
# @app.route("/hospitals", methods=["POST"])
# def hospitals():
#     data = request.json
#     lat, lon = data.get("lat"), data.get("lon")
#     print("✅ Received coordinates:", data)

#     # Construct Google Places API URL
#     url = (
#         "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#         f"?location={lat},{lon}"
#         "&radius=5000"
#         "&type=hospital"
#         f"&key={GOOGLE_API_KEY}"
#     )
#     print("🌐 Request URL:", url)

#     # Make request to Google
#     res = requests.get(url).json()
#     print("📦 Google Response:", res)

#     hospitals = []
#     for place in res.get("results", [])[:5]:
#         name = place.get("name")
#         addr = place.get("vicinity")
#         hospitals.append(f"{name} — {addr}")

#     # Send the hospital list back to JS
#     return jsonify({"hospitals": hospitals})

# if __name__ == "__main__":
#     print("🚀 Using API Key:", GOOGLE_API_KEY)
#     app.run(debug=True)


