import hashlib
import secrets


def create_ownership_challenge():
    return secrets.token_hex(16)


def generate_ownership_proof(file_id, challenge):
    data = f"{file_id}:{challenge}".encode()
    return hashlib.sha256(data).hexdigest()


def verify_ownership_proof(file_id, challenge, proof):
    expected = generate_ownership_proof(file_id, challenge)
    return secrets.compare_digest(expected, proof)