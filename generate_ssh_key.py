#!/usr/bin/env python3
"""
Generate SSH host key for the SFTP server using asyncssh
"""
import asyncssh
import os

# Generate Ed25519 private/public key pair
private_key = asyncssh.generate_private_key('ssh-ed25519')
public_key = private_key.export_public_key()

# Write private key
with open('ssh_host_ed25519_key', 'wb') as f:
    f.write(private_key.export_private_key())

# Write public key (public_key is already bytes)
with open('ssh_host_ed25519_key.pub', 'wb') as f:
    f.write(public_key)

print("✅ Generated SSH host key pair:")
print("  - ssh_host_ed25519_key (private key)")
print("  - ssh_host_ed25519_key.pub (public key)")

# Set appropriate permissions (read-only for owner on private key)
try:
    os.chmod('ssh_host_ed25519_key', 0o600)
    print("✅ Set secure permissions on private key")
except:
    print("⚠️  Could not set permissions (Windows limitation)")