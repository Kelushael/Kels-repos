from flask import Flask, request, jsonify
import os
import hashlib
import time

app = Flask(__name__)

# Allowed AI & user IP addresses for security
ALLOWED_IPS = {
    "44.226.145.213",
    "54.187.200.255",
    "34.213.214.55",
    "35.164.95.156",
    "44.230.95.183",
    "44.229.200.200"
}

# Store lyrics before they are manually entered (Lattice Buffer)
lattice_buffer = {}

# Generate an Echo Key for access control
def generate_echo_key():
    return hashlib.sha256(f"{time.time()}_{os.urandom(16)}".encode()).hexdigest()[:16]

# Middleware: Only allow requests from whitelisted IPs
@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip not in ALLOWED_IPS:
        return jsonify({"error": "Unauthorized access - IP not allowed"}), 403

# Provide a public link for external AI contributions
@app.route("/generate_lattice_link", methods=["POST"])
def generate_lattice_link():
    key = generate_echo_key()
    public_url = f"https://yourdomain.com/lattice/{key}"
    return jsonify({"public_link": public_url, "echo_key": key})

# Store lyrics in the lattice buffer
@app.route("/submit_lyrics", methods=["POST"])
def submit_lyrics():
    data = request.json
    echo_key = data.get("echo_key")
    lyrics = data.get("lyrics")

    if not echo_key or not lyrics:
        return jsonify({"error": "Echo key and lyrics required"}), 400

    lattice_buffer[echo_key] = lyrics
    return jsonify({"message": "Lyrics stored in lattice buffer.", "stored_lyrics": lyrics})

# Retrieve lyrics for realignment before final input
@app.route("/get_lattice_lyrics/<echo_key>", methods=["GET"])
def get_lattice_lyrics(echo_key):
    if echo_key in lattice_buffer:
        return jsonify({"lattice_lyrics": lattice_buffer[echo_key]})
    else:
        return jsonify({"error": "No lyrics found for this Echo Key."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)