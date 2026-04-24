from datetime import datetime, timezone


socketio = None


def configure_socket_events(socketio_instance):
    global socketio
    socketio = socketio_instance


def _emit(event_name, payload):
    if socketio is not None:
        socketio.emit(event_name, payload)


def _base_payload(username):
    return {
        "username": username,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def emit_key_generated(username, public_key, secret_key):
    payload = _base_payload(username)
    payload.update({"public_key": public_key, "secret_key": secret_key})
    _emit("key_generated", payload)


def emit_challenge(username, challenge):
    payload = _base_payload(username)
    payload.update({"challenge": challenge})
    _emit("challenge_created", payload)


def emit_signature(username, challenge, signature):
    payload = _base_payload(username)
    payload.update({"challenge": challenge, "signature": signature})
    _emit("signature_generated", payload)


def emit_auth_success(username):
    payload = _base_payload(username)
    payload.update({"status": "success"})
    _emit("auth_success", payload)


def emit_auth_failed(username, reason):
    payload = _base_payload(username)
    payload.update({"status": "failed", "reason": reason})
    _emit("auth_failed", payload)
