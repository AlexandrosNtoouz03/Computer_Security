#!/usr/bin/env python3
"""
SFTP System Main Launcher
Provides a menu to launch server, client, or run tests.
"""
import os
import sys
import subprocess
import asyncio

def print_main_menu():
    """Display the main menu"""
    print("=" * 80)
    print("🔐 SECURE SFTP SYSTEM - COMPUTER SECURITY PROJECT")
    print("=" * 80)
    print("Maastricht University - Multi-Model Authorization System")
    print("Features: DAC + MAC + RBAC + Comprehensive Audit Logging")
    print("=" * 80)
    print()
    print("📋 MAIN MENU")
    print("-" * 20)
    print("1. 🚀 Start SFTP Server (Interactive)")
    print("2. 🖥️  Start SFTP Client (Interactive)")
    print("3. 🧪 Run System Tests")
    print("4. 🔧 System Utilities")
    print("5. 📚 View Documentation")
    print("6. ❌ Exit")
    print()

def print_utilities_menu():
    """Display utilities submenu"""
    print("\n🔧 SYSTEM UTILITIES")
    print("-" * 30)
    print("1. Generate SSH Host Key")
    print("2. Reset User Passwords")
    print("3. Test Authorization System")
    print("4. View Audit Log")
    print("5. Clear Audit Log")
    print("6. 🔙 Back to Main Menu")
    print()

def print_documentation_menu():
    """Display documentation menu"""
    print("\n📚 DOCUMENTATION")
    print("-" * 25)
    print("1. View README.md")
    print("2. View Deployment Guide")
    print("3. View Completion Summary")
    print("4. Show User Accounts")
    print("5. Show Security Models")
    print("6. 🔙 Back to Main Menu")
    print()

def run_command(cmd, description):
    """Run a command and handle errors"""
    try:
        print(f"\n🔧 {description}...")
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("\n🧪 RUNNING SYSTEM TESTS")
    print("=" * 40)
    
    tests = [
        ("python -m pytest tests/ -v", "Unit Tests (Authorization Models)"),
        ("python test_integration.py", "Integration Test (Server Components)"),
        ("python test_authorization.py", "Authorization Test (Policy Validation)")
    ]
    
    all_passed = True
    for cmd, desc in tests:
        print(f"\n📋 {desc}")
        print("-" * len(desc))
        if not run_command(cmd, f"Running {desc}"):
            all_passed = False
        print()
    
    if all_passed:
        print("✅ ALL TESTS PASSED! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    input("\nPress Enter to continue...")

def handle_utilities():
    """Handle utilities submenu"""
    while True:
        print_utilities_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            run_command("python generate_ssh_key.py", "Generating SSH Host Key")
        elif choice == '2':
            run_command("python generate_passwords.py", "Resetting User Passwords")
        elif choice == '3':
            run_command("python test_authorization.py", "Testing Authorization System")
        elif choice == '4':
            if os.path.exists("audit.jsonl"):
                print("\n📋 RECENT AUDIT LOG ENTRIES")
                print("-" * 40)
                run_command("tail -10 audit.jsonl", "Showing last 10 audit entries")
            else:
                print("\n📋 No audit log found. Start the server to generate audit entries.")
        elif choice == '5':
            if os.path.exists("audit.jsonl"):
                confirm = input("⚠️  Clear audit log? This cannot be undone (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    with open("audit.jsonl", "w") as f:
                        pass
                    print("✅ Audit log cleared.")
                else:
                    print("❌ Operation cancelled.")
            else:
                print("📋 No audit log to clear.")
        elif choice == '6':
            break
        else:
            print("❌ Invalid option. Please select 1-6.")
        
        if choice != '6':
            input("\nPress Enter to continue...")

def show_user_accounts():
    """Display user account information"""
    print("\n👥 USER ACCOUNTS")
    print("-" * 50)
    accounts = [
        ("test", "test", "internal", "reader", "Basic read access"),
        ("admin", "admin", "secret", "admin", "Full administrative access"),
        ("editor", "editor", "confidential", "editor", "Read/write up to confidential"),
        ("guest", "guest", "unclassified", "guest", "Limited read-only access")
    ]
    
    print(f"{'Username':<10} {'Password':<10} {'Clearance':<12} {'Role':<8} {'Description'}")
    print("-" * 80)
    for username, password, clearance, role, desc in accounts:
        print(f"{username:<10} {password:<10} {clearance:<12} {role:<8} {desc}")

def show_security_models():
    """Display security model information"""
    print("\n🔐 SECURITY MODELS")
    print("-" * 30)
    print("1. DAC (Discretionary Access Control)")
    print("   - File ownership and permission bits")
    print("   - Data: data/dac_owners.csv")
    print("   - Rule: Owners have full control")
    print()
    print("2. MAC (Mandatory Access Control)")
    print("   - Bell-LaPadula security model")
    print("   - Data: data/mac_labels.json")
    print("   - Rules: No read up, no write down")
    print("   - Levels: unclassified → internal → confidential → secret → top_secret")
    print()
    print("3. RBAC (Role-Based Access Control)")
    print("   - Role-based operation permissions")
    print("   - Data: data/user_roles.json, data/role_perms.csv")
    print("   - Roles: admin, editor, reader, guest")
    print()
    print("🛡️  All three models must approve access for operations to succeed.")

def handle_documentation():
    """Handle documentation submenu"""
    while True:
        print_documentation_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            if os.path.exists("README.md"):
                if sys.platform.startswith('win'):
                    os.system("type README.md")
                else:
                    os.system("cat README.md")
            else:
                print("❌ README.md not found.")
        elif choice == '2':
            if os.path.exists("DEPLOYMENT.md"):
                if sys.platform.startswith('win'):
                    os.system("type DEPLOYMENT.md")
                else:
                    os.system("cat DEPLOYMENT.md")
            else:
                print("❌ DEPLOYMENT.md not found.")
        elif choice == '3':
            if os.path.exists("COMPLETION_SUMMARY.md"):
                if sys.platform.startswith('win'):
                    os.system("type COMPLETION_SUMMARY.md")
                else:
                    os.system("cat COMPLETION_SUMMARY.md")
            else:
                print("❌ COMPLETION_SUMMARY.md not found.")
        elif choice == '4':
            show_user_accounts()
        elif choice == '5':
            show_security_models()
        elif choice == '6':
            break
        else:
            print("❌ Invalid option. Please select 1-6.")
        
        if choice != '6':
            input("\nPress Enter to continue...")

def main():
    """Main launcher menu"""
    try:
        while True:
            print_main_menu()
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                print("\n🚀 Starting Interactive SFTP Server...")
                try:
                    subprocess.run([sys.executable, "start_server.py"], check=True)
                except KeyboardInterrupt:
                    print("\n👋 Server startup cancelled.")
                except Exception as e:
                    print(f"❌ Error starting server: {e}")
                
            elif choice == '2':
                print("\n🖥️  Starting Interactive SFTP Client...")
                try:
                    subprocess.run([sys.executable, "start_client.py"], check=True)
                except KeyboardInterrupt:
                    print("\n👋 Client startup cancelled.")
                except Exception as e:
                    print(f"❌ Error starting client: {e}")
                
            elif choice == '3':
                run_tests()
                
            elif choice == '4':
                handle_utilities()
                
            elif choice == '5':
                handle_documentation()
                
            elif choice == '6':
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid option. Please select 1-6.")
            
            if choice != '6':
                print("\n" + "=" * 80)
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()