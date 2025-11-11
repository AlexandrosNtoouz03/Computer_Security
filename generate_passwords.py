#!/usr/bin/env python3
"""
Generate proper password hashes for all test users
"""
import sys
import os
import base64
import hashlib
import secrets
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def _scrypt_hash(password: str, salt: bytes, n=2**14, r=8, p=1, dklen=64):
    return hashlib.scrypt(password.encode(), salt=salt, n=n, r=r, p=p, dklen=dklen)

def generate_password_entry(username: str, password: str, clearance: str):
    """Generate a complete user entry with proper password hash"""
    salt = secrets.token_bytes(16)
    n, r, p, dklen = 2**14, 8, 1, 64
    password_hash = _scrypt_hash(password, salt, n, r, p, dklen)
    
    return {
        "username": username,
        "salt": base64.b64encode(salt).decode(),
        "password_hash": base64.b64encode(password_hash).decode(),
        "n": n,
        "r": r,
        "p": p,
        "dklen": dklen,
        "clearance": clearance
    }

# Generate proper entries for all users
users = [
    generate_password_entry("test", "test", "internal"),
    generate_password_entry("admin", "admin", "secret"), 
    generate_password_entry("editor", "editor", "confidential"),
    generate_password_entry("guest", "guest", "unclassified")
]

# Save to users.json
users_file = os.path.join("data", "users.json")
with open(users_file, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2)

print("Generated new user passwords:")
for user in users:
    print(f"  {user['username']} -> password: {user['username']} (clearance: {user['clearance']})")

print(f"\nUpdated {users_file}")
print("You can now authenticate with:")
print("  test/test, admin/admin, editor/editor, guest/guest")