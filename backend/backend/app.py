from flask import Flask, request, jsonify
import os
from flask_cors import CORS

from crypto.pqc import PQC
from blockchain.chain import Blockchain
from storage.db import init_db, add_user, get_user

app = Flask(__name__)
CORS(app)

# Initialize components
blockchain = Blockchain()
challenges = {}

# Store secret_key temporarily in memory for verification
# Key: username, Value: secret_key
users_secret = {}

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

    # Generate keypair
    public_key, secret_key = PQC.generate_keys()

    # Store secret_key temporarily in memory for verification
    users_secret[username] = secret_key

    # Add public key to blockchain
    blockchain.add_block({
        "username": username,
        "public_key": public_key
    })

    # Add user to database
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

    # Generate a random challenge
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

    # Check if challenge exists (prevents replay attack)
    if username not in challenges:
        return jsonify({"error": "Challenge expired or not found"}), 400

    challenge = challenges[username]

    # Check if message was tampered (must match challenge exactly)
    if message != challenge:
        return jsonify({"error": "Tampered message"}), 400

    # Get stored secret_key for this user
    if username not in users_secret:
        return jsonify({"error": "Secret key not found. Please register again."}), 400

    stored_secret_key = users_secret[username]

    # Get public_key from blockchain
    public_key = None
    for block in blockchain.chain:
        if isinstance(block.data, dict):
            if block.data.get("username") == username:
                public_key = block.data.get("public_key")

    if not public_key:
        return jsonify({"error": "Public key not found"}), 404

    # Compute expected signature: SHA256(message + secret_key)
    expected_signature = PQC.sign(message, stored_secret_key)

    # Verify: compare signatures
    is_valid = (signature == expected_signature)

    # Delete challenge after verification to prevent replay attacks
    del challenges[username]

    if is_valid:
        return jsonify({
            "message": "✅ Authentication successful",
            "debug": {
                "challenge": message,
                "signature": signature,
                "public_key": public_key,
                "expected_signature": expected_signature,
                "result": "VALID"
            }
        })
    else:
        return jsonify({
            "error": "❌ Authentication failed",
            "debug": {
                "challenge": message,
                "signature": signature,
                "public_key": public_key,
                "expected_signature": expected_signature,
                "result": "INVALID"
            }
        }), 401


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