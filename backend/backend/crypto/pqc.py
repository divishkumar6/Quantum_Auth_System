import hashlib
import hmac
import secrets


class PQC:
    @staticmethod
    def sha256_hex(value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def derive_public_key(secret_key):
        return PQC.sha256_hex(secret_key)

    @staticmethod
    def generate_keys():
        secret_key = secrets.token_hex(32)
        public_key = PQC.derive_public_key(secret_key)
        return public_key, secret_key

    @staticmethod
    def sign(message, secret_key):
        return PQC.sha256_hex(f"{message}{secret_key}")

    @staticmethod
    def verify(message, signature, secret_key=None, public_key=None):
        if not secret_key or not public_key:
            return False

        derived_public_key = PQC.derive_public_key(secret_key)
        if derived_public_key != public_key:
            return False

        expected_signature = PQC.sign(message, secret_key)
        return hmac.compare_digest(signature or "", expected_signature)
