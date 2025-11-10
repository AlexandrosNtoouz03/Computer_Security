
"""
Main entry point for the SFTP server. Starts AsyncSSH, loads host key,
and registers the SFTP subsystem implemented in sftp.py.
"""
import asyncio, asyncssh, logging, os
from server.sftp import SFTPSession
from server.auth import authenticate

HOST_KEY = os.path.join(os.path.dirname(__file__), "ssh_host_ed25519_key")
PORT = 2222

class SFTPServer(asyncssh.SSHServer):
    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        return authenticate(username, password)

    def session_requested(self):
        return SFTPSession()

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    await asyncssh.listen("", PORT, server_host_keys=[HOST_KEY], server_factory=SFTPServer)
    print(f"SFTP server listening on port {PORT}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
