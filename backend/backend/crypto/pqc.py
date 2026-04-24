import hashlib
import secrets

class PQC:

    @staticmethod
    def generate_keys():
        # Generate a random secret key
        secret_key = secrets.token_hex(32)
        # Public key is SHA256 of secret key
        public_key = hashlib.sha256(secret_key.encode()).hexdigest()
        return public_key, secret_key

    @staticmethod
    def sign(message, secret_key):
        # Signature is SHA256(message + secret_key)
        return hashlib.sha256((message + secret_key).encode()).hexdigest()

    @staticmethod
    def verify(message, signature, public_key):
        # This method is kept for compatibility but verification
        # should be done using stored secret_key in app.py
        # Return False as we can't verify without secret_key
        return False