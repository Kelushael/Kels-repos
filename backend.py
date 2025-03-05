from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

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

    # Metadata filtering logic
    metadata = {
        "flow_id": flow_id,
        "word_count": len(prompt.split()),
        "sentiment": "positive" if "love" in prompt else "neutral",
        "thought_depth": "deep" if len(prompt.split()) > 10 else "shallow",
        "category": "music" if "beat" in prompt or "song" in prompt else "general",
        "timestamp": int(time.time()),
    }

    return jsonify({"metadata": metadata})

# System health check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "Healthy", "message": "Backend is operational."})

# Reset or debug function
@app.route("/reset")
def reset():
    return jsonify({"status": "Reset command received", "message": "System is active."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)