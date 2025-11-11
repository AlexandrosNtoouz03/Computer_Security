#!/usr/bin/env python3
"""
Debug password validation
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from server.auth import authenticate

# Test the actual authentication function
users_to_test = ["test", "admin", "editor", "guest"]
password = "test"

print("Testing password authentication...")
for user in users_to_test:
    result = authenticate(user, password)
    print(f"  {user} + '{password}': {'✓ SUCCESS' if result else '✗ FAILED'}")

# Also check what's in the users file
from server.policy import _load_users

print("\nLoaded users:")
users = _load_users()
for user in users:
    print(f"  Username: {user.get('username')}")
    print(f"  Clearance: {user.get('clearance')}")
    print(f"  Has password hash: {'Yes' if user.get('password_hash') else 'No'}")
    print(f"  Has salt: {'Yes' if user.get('salt') else 'No'}")
    print("  ---")