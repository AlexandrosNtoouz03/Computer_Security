"""
Handles password verification using secure hashes
Loads static user data from data/users.json.
"""
import base64, hashlib, secrets, json, os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def _scrypt_hash(password: str, salt: bytes, n=2**14, r=8, p=1, dklen=64):
    return hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p, dklen=dklen)

def _verify_password(password, salt_b64, hash_b64, n=2**14, r=8, p=1, dklen=64):
    try:
        salt = base64.b64decode(salt_b64)
        stored = base64.b64decode(hash_b64)
        calc = _scrypt_hash(password, salt, n, r, p, dklen)
        return secrets.compare_digest(calc, stored)
    except Exception:
        return False

def authenticate(username, password):
    if not os.path.isfile(DATA_PATH):
        return False
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        users = json.load(f)
    user = next((u for u in users if u.get("username") == username), None)
    if not user:
        return False
    return _verify_password(password, user["salt"], user["password_hash"],
                            n=user.get("n", 2**14), r=user.get("r", 8),
                            p=user.get("p", 1), dklen=user.get("dklen", 64))
