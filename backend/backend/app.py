from flask import Flask, request, jsonify
import os

from crypto.pqc import PQC
from blockchain.chain import Blockchain
from storage.db import init_db, add_user, get_user

app = Flask(__name__)

# Initialize components
blockchain = Blockchain()
challenges = {}

init_db()

# -----------------------------
# REGISTER
# -----------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username")
    name = data.get("name")
    gender = data.get("gender")
    mobile = data.get("mobile")

    if not username:
        return jsonify({"error": "Username required"}), 400

    if get_user(username):
        return jsonify({"error": "User already exists"}), 400

    public_key, secret_key = PQC.generate_keys()

    blockchain.add_block({
        "username": username,
        "public_key": public_key
    })

    success = add_user(username, name, gender, mobile)

    if not success:
        return jsonify({"error": "Database error"}), 500

    return jsonify({
        "message": "User registered",
        "secret_key": secret_key,
        "public_key": public_key
    })


# -----------------------------
# LOGIN (GET CHALLENGE)
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")

    if not get_user(username):
        return jsonify({"error": "User not found"}), 404

    challenge = os.urandom(8).hex()
    challenges[username] = challenge

    return jsonify({
        "challenge": challenge
    })


# -----------------------------
# VERIFY
# -----------------------------
@app.route('/verify', methods=['POST'])
def verify_user():
    data = request.get_json()

    username = data.get("username")
    message = data.get("message")
    signature = data.get("signature")

    if username not in challenges:
        return jsonify({"error": "Challenge expired"}), 400

    challenge = challenges[username]

    if message != challenge:
        return jsonify({"error": "Tampered message"}), 400

    public_key = None

    for block in blockchain.chain:
        if isinstance(block.data, dict):
            if block.data.get("username") == username:
                public_key = block.data.get("public_key")

    if not public_key:
        return jsonify({"error": "Public key not found"}), 404

    is_valid = PQC.verify(message, signature, public_key)

    del challenges[username]

    if is_valid:
        return jsonify({
            "message": "✅ Authentication successful",
            "debug": {
                "challenge": message,
                "signature": signature,
                "public_key": public_key
            }
        })
    else:
        return jsonify({"error": "❌ Authentication failed"}), 401


# -----------------------------
# BLOCKCHAIN STATUS (FOR DEMO)
# -----------------------------
@app.route('/blockchain', methods=['GET'])
def get_chain():
    chain_data = []

    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "data": block.data,
            "hash": block.hash,
            "prev_hash": block.prev_hash
        })

    return jsonify(chain_data)


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)