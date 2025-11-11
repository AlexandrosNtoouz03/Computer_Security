#!/usr/bin/env python3
"""
Interactive SFTP Server Startup Script
Prompts for configuration details before starting the server.
"""
import asyncio
import asyncssh
import os
import sys
import getpass
from pathlib import Path

# Import our existing server components
from main import Server, JAIL_ROOT

def print_banner():
    """Display welcome banner"""
    print("=" * 70)
    print("🔐 SECURE SFTP SERVER WITH MULTI-MODEL AUTHORIZATION")
    print("=" * 70)
    print("Computer Security Group Assignment - Maastricht University")
    print("Features: DAC + MAC + RBAC Authorization Models")
    print("=" * 70)

def get_server_config():
    """Interactively collect server configuration"""
    print("\n📋 SERVER CONFIGURATION")
    print("-" * 30)
    
    # Host configuration
    print("\n🌐 Network Configuration:")
    host = input(f"Listen on host (default: 0.0.0.0 - all interfaces): ").strip()
    if not host:
        host = "0.0.0.0"
    
    port_input = input(f"Listen on port (default: 2222): ").strip()
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
    
    # SSH Key configuration
    print("\n🔑 SSH Key Configuration:")
    default_key = "./ssh_host_ed25519_key"
    key_path = input(f"SSH host key path (default: {default_key}): ").strip()
    if not key_path:
        key_path = default_key
    
    # Check if key exists
    if not os.path.exists(key_path):
        print(f"⚠️  SSH host key not found at: {key_path}")
        generate = input("Generate new SSH host key? (y/N): ").strip().lower()
        if generate in ['y', 'yes']:
            generate_ssh_key(key_path)
        else:
            print("❌ Cannot start server without SSH host key.")
            sys.exit(1)
    
    # Jail root configuration
    print("\n📁 File System Configuration:")
    default_jail = os.path.abspath("./sftp_root")
    jail_root = input(f"SFTP jail root directory (default: {default_jail}): ").strip()
    if not jail_root:
        jail_root = default_jail
    
    # Create jail root if it doesn't exist
    os.makedirs(jail_root, exist_ok=True)
    
    # Logging configuration
    print("\n📝 Logging Configuration:")
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    print(f"Available log levels: {', '.join(log_levels)}")
    log_level = input("Log level (default: INFO): ").strip().upper()
    if log_level not in log_levels:
        log_level = "INFO"
    
    return {
        'host': host,
        'port': port,
        'key_path': key_path,
        'jail_root': jail_root,
        'log_level': log_level
    }

def generate_ssh_key(key_path):
    """Generate SSH host key"""
    try:
        print(f"🔧 Generating SSH host key: {key_path}")
        
        # Generate Ed25519 private/public key pair
        private_key = asyncssh.generate_private_key('ssh-ed25519')
        public_key = private_key.export_public_key()
        
        # Write private key
        with open(key_path, 'wb') as f:
            f.write(private_key.export_private_key())
        
        # Write public key
        with open(f"{key_path}.pub", 'wb') as f:
            f.write(public_key)
        
        # Set appropriate permissions
        try:
            os.chmod(key_path, 0o600)
            print(f"✅ Generated SSH host key: {key_path}")
        except:
            print(f"✅ Generated SSH host key: {key_path} (permissions not set - Windows)")
    
    except Exception as e:
        print(f"❌ Failed to generate SSH key: {e}")
        sys.exit(1)

def show_user_accounts():
    """Display available user accounts"""
    print("\n👥 AVAILABLE USER ACCOUNTS")
    print("-" * 40)
    accounts = [
        ("test", "test", "internal", "reader", "Basic read access"),
        ("admin", "admin", "secret", "admin", "Full administrative access"),
        ("editor", "editor", "confidential", "editor", "Read/write up to confidential"),
        ("guest", "guest", "unclassified", "guest", "Limited read-only access")
    ]
    
    print(f"{'Username':<10} {'Password':<10} {'Clearance':<12} {'Role':<8} {'Description'}")
    print("-" * 70)
    for username, password, clearance, role, desc in accounts:
        print(f"{username:<10} {password:<10} {clearance:<12} {role:<8} {desc}")

def confirm_startup(config):
    """Show configuration summary and confirm startup"""
    print("\n📋 CONFIGURATION SUMMARY")
    print("-" * 40)
    print(f"🌐 Server Address: {config['host']}:{config['port']}")
    print(f"🔑 SSH Host Key: {config['key_path']}")
    print(f"📁 Jail Root: {config['jail_root']}")
    print(f"📝 Log Level: {config['log_level']}")
    
    show_user_accounts()
    
    print("\n" + "=" * 70)
    confirm = input("🚀 Start SFTP server with these settings? (Y/n): ").strip().lower()
    return confirm in ['', 'y', 'yes']

def setup_logging(log_level):
    """Configure logging"""
    import logging
    
    # Map string levels to logging constants
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO, 
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }
    
    logging.basicConfig(
        level=level_map.get(log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    
    # Set AsyncSSH logging level
    if log_level == 'DEBUG':
        logging.getLogger("asyncssh").setLevel(logging.DEBUG)
    else:
        logging.getLogger("asyncssh").setLevel(logging.INFO)

async def start_server(config):
    """Start the SFTP server with given configuration"""
    try:
        print(f"\n🚀 Starting SFTP server...")
        print(f"📁 Jail root: {config['jail_root']}")
        
        # Start the server
        await asyncssh.listen(
            config['host'], 
            config['port'],
            server_host_keys=[config['key_path']],
            server_factory=Server
        )
        
        print(f"✅ SFTP server listening on {config['host']}:{config['port']}")
        print(f"🔐 Authorization models active: DAC + MAC + RBAC")
        print(f"📝 Audit logging enabled")
        print("\n" + "=" * 70)
        print("Server is ready! Use Ctrl+C to stop.")
        print("=" * 70)
        
        # Keep server running
        await asyncio.Event().wait()
        
    except OSError as e:
        if "already in use" in str(e) or "10048" in str(e):
            print(f"❌ Port {config['port']} is already in use!")
            print("   Either stop the existing server or choose a different port.")
        else:
            print(f"❌ Failed to start server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

def main():
    """Main interactive server startup"""
    try:
        print_banner()
        
        # Get configuration interactively
        config = get_server_config()
        
        # Setup logging
        setup_logging(config['log_level'])
        
        # Confirm and start
        if confirm_startup(config):
            print("\n🔧 Initializing server components...")
            
            # Update global jail root for our server
            global JAIL_ROOT
            JAIL_ROOT = config['jail_root']
            
            # Start the server
            asyncio.run(start_server(config))
        else:
            print("❌ Server startup cancelled.")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n👋 Server shutdown requested.")
        print("Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()