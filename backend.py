# backend.py

from flask import Flask, request, jsonify
import hashlib
import time
import openai
import os

app = Flask(__name__)

# API Keys & Configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ECHO_KEY = os.getenv("GITHUB_ECHO_KEY")

# Function to generate a unique flow script identifier
def generate_flow_id(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()[:16]

# Endpoint for metadata analysis & flow scripting
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    prompt = data.get("prompt", "").lower()

    # Generate a unique ID for the flow script
    flow_id = generate_flow_id(prompt)

    # Basic metadata analysis and categorization
    metadata = {
        "flow_id": flow_id,
        "word_count": len(prompt.split()),
        "sentiment": "positive" if "love" in prompt else "neutral",
        "thought_depth": "deep" if len(prompt.split()) > 10 else "shallow",
        "category": "music" if "beat" in prompt or "song" in prompt else "general",
        "timestamp": int(time.time()),
    }

    return jsonify({"metadata": metadata})

# Endpoint to generate lyrics based on flow scripting
@app.route("/generate_with_flow", methods=["POST"])
def generate_with_flow():
    data = request.json
    flow_name = data.get("flow_name", "")
    lyrics = data.get("lyrics", "")

    if not flow_name or not lyrics:
        return jsonify({"error": "Flow name and lyrics are required"}), 400

    flow_script = get_flow_script(flow_name)
    if not flow_script:
        return jsonify({"error": "Flow script not found"}), 404

    blended_lyrics = blend_lyrics(flow_script, lyrics)

    return jsonify({"blended_lyrics": blended_lyrics})

# Helper function to retrieve the flow script
def get_flow_script(flow_name):
    # In a real system, this would fetch from a database or file.
    # For now, we'll use a simple dictionary to simulate it.
    flow_scripts = {
        "love_flow": "love love love deep deep beat",
        "hiphop_flow": "drop beat flow pop pop drop",
    }
    return flow_scripts.get(flow_name)

# Function to blend lyrics with flow script
def blend_lyrics(flow_script, lyrics):
    flow_words = flow_script.split()
    lyric_words = lyrics.split()

    # Make sure lengths match
    if len(flow_words) != len(lyric_words):
        return "Error: Flow and lyrics lengths do not match!"

    return " ".join(f"({flow}) {word}" for flow, word in zip(flow_words, lyric_words))

# Reset system endpoint
@app.route("/reset")
def reset():
    return jsonify({"status": "Reset command received", "message": "System is active."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)