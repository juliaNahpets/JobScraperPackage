import hashlib
import base64


def get_encoded_id(url):
    hash_data = hashlib.sha256(url.encode())
    base64_hash = base64.urlsafe_b64encode(hash_data.digest())

    encoded_id = base64_hash.decode("utf-8").rstrip("=")

    return encoded_id
