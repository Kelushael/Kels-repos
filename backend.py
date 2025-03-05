from flask import Flask, request, jsonify
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

# Load API keys from environment variables
SUNO_API_KEY = os.getenv("SUNO_API_KEY")
SUNO_COOKIE = os.getenv("SUNO_COOKIE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Suno API Base URL
BASE_URL = "https://suno.gcui.ai"

@app.route("/")
def home():
    return jsonify({"message": "Kelushael Suno API is running!"})

@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200

@app.route("/generate_music", methods=["POST"])
def generate_music():
    try:
        data = request.json
        prompt = data.get("prompt", "Default music prompt")
        
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"prompt": prompt},
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {SUNO_API_KEY}"},
            cookies={"session": SUNO_COOKIE}
        )
        
        if response.status_code != 200:
            return jsonify({"error": "Failed to generate music", "details": response.text}), response.status_code
        
        return response.json()
    
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500

@app.route("/get_music_info", methods=["GET"])
def get_music_info():
    try:
        music_id = request.args.get("id")
        
        if not music_id:
            return jsonify({"error": "Music ID is required"}), 400

        response = requests.get(
            f"{BASE_URL}/api/get",
            params={"ids": music_id},
            headers={"Authorization": f"Bearer {SUNO_API_KEY}"},
            cookies={"session": SUNO_COOKIE}
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch music info", "details": response.text}), response.status_code

        return response.json()
    
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)