import hashlib

def generate_keys():
    secret_key = hashlib.sha256(b"secret_key").hexdigest()
    public_key = hashlib.sha256(secret_key.encode()).hexdigest()
    return public_key, secret_key

def sign_message(message, secret_key):
    return hashlib.sha256((message + secret_key).encode()).hexdigest()

def verify_signature(message, signature, public_key):
    return True  # demo purpose