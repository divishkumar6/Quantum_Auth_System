from flask import Flask, request, jsonify
from nacl.signing import SigningKey, VerifyKey
import nacl.encoding
import os

app = Flask(__name__)

users = {}
challenges = {}

# -----------------------------
# REGISTER
# -----------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    # Generate keypair
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    users[username] = {
        "signing_key": signing_key,
        "verify_key": verify_key
    }

    return jsonify({
        "message": "User registered successfully"
    })


# -----------------------------
# LOGIN
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    challenge = os.urandom(32)
    challenges[username] = challenge

    return jsonify({
        "challenge": challenge.hex()
    })


# -----------------------------
# VERIFY
# -----------------------------
@app.route('/verify', methods=['POST'])
def verify_user():
    data = request.get_json()
    username = data.get("username")

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    if username not in challenges:
        return jsonify({"error": "No challenge found"}), 400

    challenge = challenges[username]

    signing_key = users[username]["signing_key"]
    verify_key = users[username]["verify_key"]

    try:
        # Sign
        signed = signing_key.sign(challenge)

        # Verify
        verify_key.verify(signed)

        return jsonify({
            "message": "✅ Authentication successful"
        })

    except Exception as e:
        return jsonify({
            "error": "❌ Authentication failed",
            "details": str(e)
        }), 500


# -----------------------------
# RUN
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)