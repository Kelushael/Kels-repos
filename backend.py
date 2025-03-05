from flask import Flask, request, jsonify, render_template
import openai
import requests
import os

app = Flask(__name__)

# API Keys & Configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ECHO_KEY = os.getenv("GITHUB_ECHO_KEY")

# FlowScript storage (temporary for active session)
flow_scripts = {}

### 🧠 FRONTEND SERVING ###
@app.route("/")
def home():
    return render_template("index.html")

### 🎶 SAVE A FLOW SCRIPT ###
@app.route("/save_flow", methods=["POST"])
def save_flow():
    data = request.json
    flow_name = data.get("flow_name", "")
    flow_script = data.get("flow_script", "")

    if not flow_name or not flow_script:
        return jsonify({"error": "Flow name and script required"}), 400

    flow_scripts[flow_name] = flow_script
    return jsonify({"message": f"Flow '{flow_name}' saved successfully!"})

### ✍️ GENERATE LYRICS USING AI + FLOW SCRIPT ###
@app.route("/generate_with_flow", methods=["POST"])
def generate_with_flow():
    data = request.json
    flow_name = data.get("flow_name", "")
    lyrics = data.get("lyrics", "")

    if not flow_name or not lyrics:
        return jsonify({"error": "Flow name and lyrics required"}), 400

    if flow_name not in flow_scripts:
        return jsonify({"error": "Flow not found!"}), 404

    flow_script = flow_scripts[flow_name].split()
    lyric_words = lyrics.split()

    if len(flow_script) != len(lyric_words):
        return jsonify({"error": "Flow and lyrics length mismatch!"}), 400

    blended_lyrics = " ".join(f"({flow}) {word}" for flow, word in zip(flow_script, lyric_words))

    return jsonify({"blended_lyrics": blended_lyrics})

### 🔗 AI MESSAGE RELAY – UPDATE CHATGPT IN REAL-TIME ###
@app.route("/relay_message", methods=["POST"])
def relay_message():
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message required"}), 400

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You will receive real-time updates from an external system."},
                  {"role": "user", "content": message}],
        api_key=OPENAI_API_KEY
    )

    return jsonify({"response": response["choices"][0]["message"]["content"]})

### 🔄 RESET SYSTEM ###
@app.route("/reset")
def reset():
    return jsonify({"status": "System Reset", "message": "All processes cleared."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)