from flask import Flask, request, jsonify, render_template
import json
import os
from crypto_utils import generate_keys, sign_message, verify_signature

app = Flask(__name__)

# 🔥 Store one-time challenges
challenges = {}

# Load users
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    return render_template("index.html")

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Username required"}), 400

    users = load_users()

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    public_key, secret_key = generate_keys()

    users[username] = {
        "public_key": public_key,
        "secret_key": secret_key
    }

    save_users(users)

    return jsonify({
        "status": "success",
        "message": "✅ User Registered",
        "public_key": public_key
    })

# LOGIN → Generate challenge
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')

    users = load_users()

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    challenge = os.urandom(16).hex()

    # 🔥 Save challenge for replay protection
    challenges[username] = challenge

    return jsonify({
        "status": "challenge",
        "challenge": challenge
    })

# VERIFY → Check signature + replay attack
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    username = data.get('username')
    message = data.get('message')

    users = load_users()

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    # 🔥 Replay attack protection
    if challenges.get(username) != message:
        return jsonify({"error": "⚠️ Replay attack detected"}), 400

    public_key = users[username]['public_key']
    secret_key = users[username]['secret_key']

    signature = sign_message(message, secret_key)
    valid = verify_signature(message, signature, public_key)

    if valid:
        # 🔥 Remove challenge after use
        challenges.pop(username, None)

        return jsonify({
            "status": "success",
            "message": "✅ Login Successful"
        })
    else:
        return jsonify({"error": "❌ Verification Failed"}), 401


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)