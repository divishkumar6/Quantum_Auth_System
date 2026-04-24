import os
import sys
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mail import Mail, Message


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config import Config  # noqa: E402


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
mail = Mail(app)


def validate_payload(data):
    required = ["name", "email", "username", "secret_key"]
    missing = [field for field in required if not (data.get(field) or "").strip()]
    return missing


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "email_service"})


@app.route("/send-secret-key", methods=["POST"])
def send_secret_key():
    data = request.get_json(silent=True) or {}
    missing = validate_payload(data)
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    recipient = data["email"].strip()
    name = data["name"].strip()
    secret_key = data["secret_key"].strip()

    if not app.config.get("MAIL_USERNAME") or not app.config.get("MAIL_PASSWORD"):
        return jsonify({"error": "EMAIL_USER and EMAIL_PASS environment variables are required."}), 500

    body = (
        f"Hello {name},\n\n"
        f"Your Secret Key:\n{secret_key}\n\n"
        "Do NOT share this key."
    )

    try:
        message = Message(
            subject="QuantumPay Secure Key",
            recipients=[recipient],
            body=body,
        )
        mail.send(message)
        return jsonify({"message": "Secret key email sent successfully."}), 200
    except Exception as exc:
        return jsonify({"error": f"Failed to send email: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
