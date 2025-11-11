#!/usr/bin/env python3
"""
Interactive SFTP Client Launcher
Prompts for connection details before starting the client.
"""
import asyncio
import sys
import getpass
from client.client import main as client_main

def print_banner():
    """Display welcome banner"""
    print("=" * 70)
    print("🖥️  SECURE SFTP CLIENT - AUTHORIZATION AWARE")
    print("=" * 70)
    print("Computer Security Group Assignment - Maastricht University")
    print("Connects to SFTP server with DAC + MAC + RBAC authorization")
    print("=" * 70)

def show_default_accounts():
    """Show available test accounts"""
    print("\n👥 AVAILABLE TEST ACCOUNTS")
    print("-" * 50)
    accounts = [
        ("test", "test", "internal", "reader", "Basic read access to / and /internal"),
        ("admin", "admin", "secret", "admin", "Full access to all directories"),
        ("editor", "editor", "confidential", "editor", "Read/write up to confidential level"),
        ("guest", "guest", "unclassified", "guest", "Read-only access to /public")
    ]
    
    print(f"{'Username':<10} {'Password':<10} {'Clearance':<12} {'Role':<8} {'Access'}")
    print("-" * 70)
    for username, password, clearance, role, access in accounts:
        print(f"{username:<10} {password:<10} {clearance:<12} {role:<8} {access}")

def get_connection_details():
    """Interactively collect connection details"""
    print("\n🔗 CONNECTION CONFIGURATION")
    print("-" * 35)
    
    # Server details
    print("\n🌐 Server Details:")
    host = input("Server host (default: 127.0.0.1): ").strip()
    if not host:
        host = "127.0.0.1"
    
    port_input = input("Server port (default: 2222): ").strip()
    if not port_input:
        port = 2222
    else:
        try:
            port = int(port_input)
            if port < 1 or port > 65535:
                print("⚠️  Invalid port range. Using default 2222.")
                port = 2222
        except ValueError:
            print("⚠️  Invalid port number. Using default 2222.")
            port = 2222
    
    # Authentication details
    print("\n🔐 Authentication:")
    show_default_accounts()
    
    print(f"\nEnter credentials:")
    username = input("Username: ").strip()
    if not username:
        print("❌ Username is required.")
        sys.exit(1)
    
    # Use getpass for password to hide input
    password = getpass.getpass("Password: ")
    if not password:
        print("❌ Password is required.")
        sys.exit(1)
    
    return {
        'host': host,
        'port': port,
        'username': username,
        'password': password
    }

def show_connection_summary(config):
    """Display connection summary"""
    print("\n📋 CONNECTION SUMMARY")
    print("-" * 30)
    print(f"🌐 Server: {config['host']}:{config['port']}")
    print(f"👤 Username: {config['username']}")
    print(f"🔐 Password: {'•' * len(config['password'])}")

def show_client_help():
    """Show available client commands"""
    print("\n💡 AVAILABLE COMMANDS ONCE CONNECTED")
    print("-" * 45)
    commands = [
        ("help", "Show available commands"),
        ("pwd", "Print current working directory"),
        ("ls [path]", "List directory contents"),
        ("cd <path>", "Change directory"),
        ("get <remote> [local]", "Download file from server"),
        ("put <local> [remote]", "Upload file to server"),
        ("mkdir <dir>", "Create directory"),
        ("stat <path>", "Show file/directory statistics"),
        ("exit", "Exit the client")
    ]
    
    for cmd, desc in commands:
        print(f"  {cmd:<20} {desc}")

def confirm_connection(config):
    """Confirm connection details"""
    show_connection_summary(config)
    show_client_help()
    
    print("\n" + "=" * 70)
    confirm = input("🚀 Connect to SFTP server? (Y/n): ").strip().lower()
    return confirm in ['', 'y', 'yes']

async def connect_client(config):
    """Connect to the SFTP server"""
    try:
        print(f"\n🔗 Connecting to {config['host']}:{config['port']}...")
        print(f"👤 Username: {config['username']}")
        
        # Call the existing client main function
        await client_main(
            config['host'], 
            config['port'], 
            config['username'], 
            config['password']
        )
        
    except ConnectionRefusedError:
        print("❌ Connection refused!")
        print("   Make sure the SFTP server is running on the specified host and port.")
        print("   Try: python start_server.py")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("   Check your connection details and try again.")

def main():
    """Main interactive client launcher"""
    try:
        print_banner()
        
        # Get connection details
        config = get_connection_details()
        
        # Confirm and connect
        if confirm_connection(config):
            print("\n🔧 Initializing client connection...")
            asyncio.run(connect_client(config))
        else:
            print("❌ Connection cancelled.")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n👋 Client startup cancelled.")
        print("Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()