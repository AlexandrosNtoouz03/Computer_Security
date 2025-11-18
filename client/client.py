"""
Interactive SFTP client with full command support:
Commands: pwd, ls, get, put, mkdir, stat, exit
"""
import asyncio, asyncssh, sys, os
from pathlib import Path

class SFTPClient:
    def __init__(self, sftp):
        self.sftp = sftp
        self.current_dir = "/"
    
    async def cmd_pwd(self, args):
        """Print working directory"""
        try:
            path = await self.sftp.realpath('.')
            print(f"Current directory: {path}")
            self.current_dir = path
        except Exception as e:
            print(f"pwd failed: {e}")
    
    async def cmd_ls(self, args):
        """List directory contents"""
        path = args[0] if args else "."
        try:
            entries = await self.sftp.listdir(path)
            print(f"Contents of {path}:")
            for entry in entries:
                print(f"  {entry}")
        except Exception as e:
            print(f"ls failed: {e}")
    
    async def cmd_get(self, args):
        """Download file from server"""
        if not args:
            print("Usage: get <remote_file> [local_file]")
            return
        
        remote_file = args[0]
        local_file = args[1] if len(args) > 1 else os.path.basename(remote_file)
        
        try:
            await self.sftp.get(remote_file, local_file)
            print(f"Downloaded: {remote_file} -> {local_file}")
        except Exception as e:
            print(f"get failed: {e}")
    
    async def cmd_put(self, args):
        """Upload file to server"""
        if not args:
            print("Usage: put <local_file> [remote_file]")
            return
        
        local_file = args[0]
        remote_file = args[1] if len(args) > 1 else os.path.basename(local_file)
        
        if not os.path.exists(local_file):
            print(f"Local file not found: {local_file}")
            return
        
        try:
            await self.sftp.put(local_file, remote_file)
            print(f"Uploaded: {local_file} -> {remote_file}")
        except Exception as e:
            print(f"put failed: {e}")
    
    async def cmd_mkdir(self, args):
        """Create directory"""
        if not args:
            print("Usage: mkdir <directory>")
            return
        
        directory = args[0]
        try:
            await self.sftp.mkdir(directory)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"mkdir failed: {e}")
    
    async def cmd_stat(self, args):
        """Get file/directory statistics"""
        if not args:
            print("Usage: stat <file_or_directory>")
            return
        
        path = args[0]
        try:
            attrs = await self.sftp.stat(path)
            print(f"Statistics for {path}:")
            print(f"  Size: {attrs.size} bytes")
            print(f"  Mode: {oct(attrs.permissions) if attrs.permissions else 'N/A'}")
            print(f"  Modified: {attrs.mtime if attrs.mtime else 'N/A'}")
        except Exception as e:
            print(f"stat failed: {e}")
    
    async def cmd_cd(self, args):
        """Change directory"""
        path = args[0] if args else "/"
        try:
            # Verify the directory exists
            await self.sftp.listdir(path)
            self.current_dir = path
            print(f"Changed to directory: {path}")
        except Exception as e:
            print(f"cd failed: {e}")
    
    async def cmd_help(self, args):
        """Show available commands"""
        commands = {
            "pwd": "Print working directory",
            "ls [path]": "List directory contents",
            "cd <path>": "Change directory",
            "get <remote> [local]": "Download file from server",
            "put <local> [remote]": "Upload file to server", 
            "mkdir <dir>": "Create directory",
            "stat <path>": "Show file/directory statistics",
            "help": "Show this help message",
            "exit": "Exit the client"
        }
        
        print("Available commands:")
        for cmd, desc in commands.items():
            print(f"  {cmd:<20} - {desc}")
    
    async def run_interactive(self):
        """Run interactive command loop"""
        print("🔐 Secure SFTP Client - Authorization System Active")
        print("Type 'help' for available commands, 'exit' to quit")
        
        # Show initial directory
        await self.cmd_pwd([])
        
        while True:
            try:
                # Command prompt
                line = input(f"sftp:{self.current_dir}> ").strip()
                if not line:
                    continue
                
                parts = line.split()
                cmd = parts[0].lower()
                args = parts[1:]
                
                if cmd == "exit":
                    print("Goodbye!")
                    break
                elif cmd == "help":
                    await self.cmd_help(args)
                elif cmd == "pwd":
                    await self.cmd_pwd(args)
                elif cmd == "ls":
                    await self.cmd_ls(args)
                elif cmd == "cd":
                    await self.cmd_cd(args)
                elif cmd == "get":
                    await self.cmd_get(args)
                elif cmd == "put":
                    await self.cmd_put(args)
                elif cmd == "mkdir":
                    await self.cmd_mkdir(args)
                elif cmd == "stat":
                    await self.cmd_stat(args)
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit gracefully.")
            except EOFError:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def show_available_accounts():
    """Display available test accounts (passwords not shown for security)"""
    print("\n📋 Available Test Accounts:")
    print("┌─────────────┬──────────────┬───────────────────────┬─────────────────────┐")
    print("│ Username    │ Clearance    │ Role                  │ Notes               │")
    print("├─────────────┼──────────────┼───────────────────────┼─────────────────────┤")
    print("│ test        │ internal     │ reader                │ Standard test user  │")
    print("│ admin       │ secret       │ admin (full access)   │ Administrative user │")
    print("│ alice       │ confidential │ editor                │ Can read/write      │")
    print("│ bob         │ internal     │ reader                │ Read-only access    │")
    print("│ charlie     │ unclassified │ guest                 │ Limited access      │")
    print("│ demo        │ unclassified │ guest                 │ Demo account        │")
    print("└─────────────┴──────────────┴───────────────────────┴─────────────────────┘")
    print("\n🔒 Note: Contact your administrator for account passwords")

def get_connection_details():
    """Prompt user for connection details"""
    print("🔐 Secure SFTP Client - Connection Setup")
    print("=" * 40)
    
    # Show available accounts
    show_available_accounts()
    
    # Get connection details
    print("\n🌐 Enter connection details:")
    host = input("  Server host [127.0.0.1]: ").strip() or "127.0.0.1"
    
    try:
        port_input = input("  Server port [2222]: ").strip()
        port = int(port_input) if port_input else 2222
    except ValueError:
        port = 2222
        print("  ⚠️ Invalid port, using default: 2222")
    
    username = input("  Username: ").strip()
    if not username:
        print("  ❌ Username is required!")
        return None
    
    import getpass
    password = getpass.getpass("  Password: ")
    if not password:
        print("  ❌ Password is required!")
        return None
    
    return host, port, username, password

async def main(host=None, port=None, username=None, password=None):
    # If no parameters provided, prompt for them
    if not all([host, port, username, password]):
        connection_details = get_connection_details()
        if not connection_details:
            print("❌ Invalid connection details. Exiting.")
            return
        host, port, username, password = connection_details
    
    print(f"\n🔗 Connecting to SFTP server at {host}:{port}")
    print(f"👤 Username: {username}")
    
    try:
        async with asyncssh.connect(host, port=port, username=username, password=password, 
                                  known_hosts=None) as conn:
            print("✅ Connected successfully!")
            
            async with conn.start_sftp_client() as sftp:
                print("✅ SFTP subsystem started")
                
                client = SFTPClient(sftp)
                await client.run_interactive()
                
    except asyncssh.DisconnectError as e:
        print(f"❌ Connection failed: {e}")
    except asyncssh.PermissionDenied:
        print("❌ Authentication failed: Invalid username/password")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        # If command line arguments provided, use them
        if len(sys.argv) > 1:
            asyncio.run(main(*sys.argv[1:]))
        else:
            # Otherwise, prompt for connection details
            asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n👋 Goodbye!")
        pass

