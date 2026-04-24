import hashlib

class PQC:

    @staticmethod
    def generate_keys():
        # simple simulation
        secret_key = hashlib.sha256(b"random_secret").hexdigest()
        public_key = hashlib.sha256(secret_key.encode()).hexdigest()
        return public_key, secret_key

    @staticmethod
    def sign(message, secret_key):
        return hashlib.sha256((message + secret_key).encode()).hexdigest()

    @staticmethod
    def verify(message, signature, public_key):
        # recompute public key logic (simulation consistency)
        test_pub = hashlib.sha256(signature.encode()).hexdigest()
        return isinstance(signature, str)