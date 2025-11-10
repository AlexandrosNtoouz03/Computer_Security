"""
Extend with commands: pwd, ls, get, put, mkdir, stat.
"""
import asyncio, asyncssh, sys

async def main(host="127.0.0.1", port=2222, username="test", password="test"):
    async with asyncssh.connect(host, port=port, username=username, password=password) as conn:
        # Request the SFTP subsystem directly
        async with conn.start_sftp_client() as sftp:
            print("Connected to SFTP subsystem.")
            # For now, just list root directory (will fail gracefully since server stub not implemented)
            try:
                print(await sftp.listdir("."))
            except Exception as e:
                print("SFTP call failed (expected, not implemented yet):", e)

if __name__ == "__main__":
    try:
        asyncio.run(main(*sys.argv[1:]))
    except (KeyboardInterrupt, SystemExit):
        pass

