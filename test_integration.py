#!/usr/bin/env python3
"""
Manual integration test for SFTP server with authorization.
This test manually starts the server and tests basic operations.
"""
import sys
import os
import time
import subprocess
import tempfile
import shutil
import asyncio
import signal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from server.policy import clear_cache, authorize

def test_authorization_integration():
    """Test that authorization works correctly in isolation"""
    print("Testing authorization system integration...")
    clear_cache()
    
    # Test various scenarios
    test_cases = [
        ("test", "read", "/", True, "User 'test' should be able to read root"),
        ("test", "write", "/", False, "User 'test' (reader) should NOT be able to write"),
        ("test", "read", "/confidential", False, "User 'test' (internal clearance) should NOT read confidential"),
        ("admin", "read", "/confidential", True, "Admin should be able to read confidential"),
        ("admin", "write", "/confidential", False, "Admin (secret clearance) should NOT write to confidential (write-down prevention)"),
        ("guest", "read", "/", True, "Guest should be able to read root"),
        ("guest", "write", "/", False, "Guest should NOT be able to write"),
    ]
    
    all_passed = True
    for user, op, path, expected, description in test_cases:
        result = authorize(user, op, path)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  {status}: {description}")
        if result != expected:
            print(f"    Expected: {expected}, Got: {result}")
            all_passed = False
    
    return all_passed

def test_sftp_server_integration():
    """Test that the SFTP server starts and can handle basic authorization"""
    print("\nTesting SFTP server integration...")
    
    # Import here to avoid circular imports
    try:
        from main import validate_user_password, Server
        print("✓ Successfully imported SFTP server components")
    except ImportError as e:
        print(f"✗ Failed to import SFTP components: {e}")
        return False
    
    # Test password validation
    if validate_user_password("test", "test"):
        print("✓ Password validation works")
    else:
        print("✗ Password validation failed")
        return False
    
    # Test server creation
    try:
        server = Server()
        print("✓ Server instance created successfully")
    except Exception as e:
        print(f"✗ Failed to create server: {e}")
        return False
    
    # Test authentication flow
    if server.password_auth_supported():
        print("✓ Password authentication supported")
    else:
        print("✗ Password authentication not supported")
        return False
    
    # Test user validation
    if server.validate_password("test", "test"):
        print("✓ User validation through server works")
        print(f"✓ Authenticated user: {server._authenticated_username}")
    else:
        print("✗ User validation through server failed")
        return False
    
    return True

def test_sftp_session_authorization():
    """Test that SFTP session properly integrates with authorization"""
    print("\nTesting SFTP session authorization integration...")
    
    try:
        from main import SFTPSession
        
        # Create a mock SFTP session
        session = SFTPSession()
        session._username = "test"  # Simulate authenticated user
        
        # Test authorization method
        if hasattr(session, '_check_authorization'):
            print("✓ SFTP session has authorization method")
            
            # Test allowed operation
            if session._check_authorization("read", "/"):
                print("✓ Read authorization works for allowed operation")
            else:
                print("✗ Read authorization failed for allowed operation")
                return False
            
            # Test denied operation
            if not session._check_authorization("write", "/"):
                print("✓ Write authorization correctly denies unauthorized operation")
            else:
                print("✗ Write authorization incorrectly allowed unauthorized operation")
                return False
                
        else:
            print("✗ SFTP session missing authorization method")
            return False
            
    except Exception as e:
        print(f"✗ Error testing SFTP session: {e}")
        return False
    
    return True

def main():
    print("SFTP SERVER INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Basic authorization system
    auth_test = test_authorization_integration()
    
    # Test 2: SFTP server components
    server_test = test_sftp_server_integration()
    
    # Test 3: SFTP session authorization
    session_test = test_sftp_session_authorization()
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"  Authorization System: {'✓ PASS' if auth_test else '✗ FAIL'}")
    print(f"  SFTP Server Components: {'✓ PASS' if server_test else '✗ FAIL'}")
    print(f"  SFTP Session Integration: {'✓ PASS' if session_test else '✗ FAIL'}")
    
    all_passed = auth_test and server_test and session_test
    print(f"\nOVERALL RESULT: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 SFTP server authorization integration is working correctly!")
        print("   The server is ready for end-to-end testing.")
    else:
        print("\n⚠️  Some integration issues detected. Review the failures above.")
    
    # Show audit log sample
    audit_file = "audit.jsonl"
    if os.path.exists(audit_file):
        print(f"\n📋 Latest audit log entries:")
        try:
            with open(audit_file, "r") as f:
                lines = f.readlines()
                for line in lines[-3:]:  # Show last 3 entries
                    print(f"   {line.strip()}")
        except Exception:
            pass
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())