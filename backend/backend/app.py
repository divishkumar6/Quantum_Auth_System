from flask import Flask, jsonify, request
from flask_cors import CORS
import os

try:
    from backend.blockchain.chain import Blockchain
    from backend.crypto.pqc import PQC
    from backend.storage.db import add_user, get_user, init_db
except ImportError:
    from blockchain.chain import Blockchain
    from crypto.pqc import PQC
    from storage.db import add_user, get_user, init_db


app = Flask(__name__)
CORS(app)

blockchain = Blockchain()
challenges = {}
users_secret = {}

init_db()


def normalize_username(value):
    return (value or "").strip()


def get_public_key_from_chain(username):
    for block in reversed(blockchain.chain):
        data = block.data if isinstance(block.data, dict) else None
        if data and data.get("username") == username:
            return data.get("public_key")
    return None


def response_payload(
    *,
    result,
    status_code,
    message=None,
    error=None,
    challenge=None,
    signature=None,
    public_key=None,
    username=None,
    extra=None,
):
    payload = {
        "result": result,
        "status_code": status_code,
        "message": message,
        "error": error,
        "username": username,
        "challenge": challenge,
        "signature": signature,
        "public_key": public_key,
    }
    if extra:
        payload.update(extra)
    return payload


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = normalize_username(data.get("username"))
    name = (data.get("name") or "").strip()
    gender = (data.get("gender") or "").strip()
    mobile = (data.get("mobile") or "").strip()

    missing = [
        field
        for field, value in {
            "username": username,
            "name": name,
            "gender": gender,
            "mobile": mobile,
        }.items()
        if not value
    ]
    if missing:
        status_code = 400
        return (
            jsonify(
                response_payload(
                    result="REGISTER_FAILED",
                    status_code=status_code,
                    error=f"Missing required fields: {', '.join(missing)}",
                    username=username or None,
                )
            ),
            status_code,
        )

    if get_user(username):
        public_key = get_public_key_from_chain(username)
        status_code = 409
        return (
            jsonify(
                response_payload(
                    result="USER_EXISTS",
                    status_code=status_code,
                    error="User already exists",
                    username=username,
                    public_key=public_key,
                )
            ),
            status_code,
        )

    public_key, secret_key = PQC.generate_keys()

    if not add_user(username, name, gender, mobile):
        status_code = 500
        return (
            jsonify(
                response_payload(
                    result="REGISTER_FAILED",
                    status_code=status_code,
                    error="Database error while creating the user",
                    username=username,
                    public_key=public_key,
                )
            ),
            status_code,
        )

    blockchain.add_block({"username": username, "public_key": public_key})
    users_secret[username] = secret_key
    challenges.pop(username, None)

    status_code = 201
    return (
        jsonify(
            response_payload(
                result="REGISTERED",
                status_code=status_code,
                message="User registered successfully",
                username=username,
                public_key=public_key,
                extra={"secret_key": secret_key},
            )
        ),
        status_code,
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = normalize_username(data.get("username"))

    if not username:
        status_code = 400
        return (
            jsonify(
                response_payload(
                    result="LOGIN_FAILED",
                    status_code=status_code,
                    error="Username required",
                )
            ),
            status_code,
        )

    if not get_user(username):
        status_code = 404
        return (
            jsonify(
                response_payload(
                    result="USER_NOT_FOUND",
                    status_code=status_code,
                    error="User not found",
                    username=username,
                )
            ),
            status_code,
        )

    public_key = get_public_key_from_chain(username)
    if not public_key:
        status_code = 404
        return (
            jsonify(
                response_payload(
                    result="LOGIN_FAILED",
                    status_code=status_code,
                    error="Public key not found on blockchain",
                    username=username,
                )
            ),
            status_code,
        )

    challenge = os.urandom(16).hex()
    challenges[username] = challenge

    status_code = 200
    return (
        jsonify(
            response_payload(
                result="CHALLENGE_CREATED",
                status_code=status_code,
                message="Challenge generated",
                username=username,
                challenge=challenge,
                public_key=public_key,
            )
        ),
        status_code,
    )


@app.route("/verify", methods=["POST"])
def verify_user():
    data = request.get_json(silent=True) or {}
    username = normalize_username(data.get("username"))
    message = data.get("message") or ""
    signature = data.get("signature") or ""

    if not username:
        status_code = 400
        return (
            jsonify(
                response_payload(
                    result="VERIFY_FAILED",
                    status_code=status_code,
                    error="Username required",
                    signature=signature or None,
                )
            ),
            status_code,
        )

    if not get_user(username):
        status_code = 404
        return (
            jsonify(
                response_payload(
                    result="USER_NOT_FOUND",
                    status_code=status_code,
                    error="User not found",
                    username=username,
                    signature=signature or None,
                )
            ),
            status_code,
        )

    public_key = get_public_key_from_chain(username)
    if not public_key:
        status_code = 404
        return (
            jsonify(
                response_payload(
                    result="VERIFY_FAILED",
                    status_code=status_code,
                    error="Public key not found on blockchain",
                    username=username,
                    signature=signature or None,
                )
            ),
            status_code,
        )

    challenge = challenges.get(username)
    if not challenge:
        status_code = 400
        return (
            jsonify(
                response_payload(
                    result="CHALLENGE_MISSING",
                    status_code=status_code,
                    error="Challenge expired or not found",
                    username=username,
                    signature=signature or None,
                    public_key=public_key,
                )
            ),
            status_code,
        )

    stored_secret_key = users_secret.get(username)
    if not stored_secret_key:
        challenges.pop(username, None)
        status_code = 409
        return (
            jsonify(
                response_payload(
                    result="VERIFY_FAILED",
                    status_code=status_code,
                    error="Secret key not found in memory. Please register again.",
                    username=username,
                    challenge=challenge,
                    signature=signature or None,
                    public_key=public_key,
                )
            ),
            status_code,
        )

    if message != challenge:
        challenges.pop(username, None)
        status_code = 400
        return (
            jsonify(
                response_payload(
                    result="TAMPERED_MESSAGE",
                    status_code=status_code,
                    error="Tampered message detected",
                    username=username,
                    challenge=challenge,
                    signature=signature or None,
                    public_key=public_key,
                )
            ),
            status_code,
        )

    derived_public_key = PQC.derive_public_key(stored_secret_key)
    if derived_public_key != public_key:
        challenges.pop(username, None)
        status_code = 409
        return (
            jsonify(
                response_payload(
                    result="VERIFY_FAILED",
                    status_code=status_code,
                    error="Stored secret key does not match blockchain public key",
                    username=username,
                    challenge=challenge,
                    signature=signature or None,
                    public_key=public_key,
                    extra={"derived_public_key": derived_public_key},
                )
            ),
            status_code,
        )

    expected_signature = PQC.sign(message, stored_secret_key)
    is_valid = PQC.verify(
        message,
        signature,
        secret_key=stored_secret_key,
        public_key=public_key,
    )
    challenges.pop(username, None)

    if is_valid:
        status_code = 200
        return (
            jsonify(
                response_payload(
                    result="VALID",
                    status_code=status_code,
                    message="Authentication successful",
                    username=username,
                    challenge=message,
                    signature=signature,
                    public_key=public_key,
                    extra={"expected_signature": expected_signature},
                )
            ),
            status_code,
        )

    status_code = 401
    return (
        jsonify(
            response_payload(
                result="INVALID",
                status_code=status_code,
                error="Authentication failed",
                username=username,
                challenge=message,
                signature=signature,
                public_key=public_key,
                extra={"expected_signature": expected_signature},
            )
        ),
        status_code,
    )


@app.route("/blockchain", methods=["GET"])
def get_chain():
    chain_data = [
        {
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "prev_hash": block.prev_hash,
        }
        for block in blockchain.chain
    ]
    return jsonify(
        {
            "status_code": 200,
            "result": "BLOCKCHAIN_READY",
            "is_valid": blockchain.is_chain_valid(),
            "length": len(chain_data),
            "chain": chain_data,
        }
    )


@app.route("/status", methods=["GET"])
def system_status():
    return jsonify(
        {
            "status_code": 200,
            "result": "SYSTEM_READY",
            "users_in_memory": sorted(users_secret.keys()),
            "active_challenges": challenges,
            "blockchain_valid": blockchain.is_chain_valid(),
            "blockchain_length": len(blockchain.chain),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
