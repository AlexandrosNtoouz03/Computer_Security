#!/usr/bin/env python3
"""
Test script for the authorization system.
Tests DAC, MAC, and RBAC models individually and combined.
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from server.policy import authorize, check_individual_models, get_user_info, clear_cache

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_user_info():
    print_separator("USER INFORMATION TEST")
    
    users = ["test", "admin", "nonexistent"]
    for user in users:
        info = get_user_info(user)
        print(f"User '{user}': {info}")

def test_individual_models():
    print_separator("INDIVIDUAL MODEL TESTS")
    
    test_cases = [
        ("test", "read", "/"),
        ("test", "read", "/confidential"),
        ("test", "write", "/"),
        ("test", "write", "/confidential"),
        ("admin", "read", "/secret"),
        ("admin", "write", "/secret"),
    ]
    
    for user, op, path in test_cases:
        print(f"\nTesting: {user} wants to {op} {path}")
        results = check_individual_models(user, op, path)
        for model, (allowed, reason) in results.items():
            status = "✓ ALLOW" if allowed else "✗ DENY"
            print(f"  {model}: {status} - {reason}")

def test_combined_authorization():
    print_separator("COMBINED AUTHORIZATION TESTS")
    
    test_cases = [
        # Test case: (user, operation, path, expected_result, description)
        ("test", "read", "/", True, "User 'test' reading root (should work - reader role, internal clearance, owns path)"),
        ("test", "write", "/", False, "User 'test' writing to root (should fail - reader role can't write)"),
        ("test", "read", "/confidential", False, "User 'test' reading confidential (should fail - insufficient clearance)"),
        ("admin", "read", "/confidential", True, "Admin reading confidential (should work - admin role, no MAC constraint specified)"),
        ("admin", "write", "/secret", True, "Admin writing to secret (should work if admin has proper clearance)"),
        ("guest", "read", "/", True, "Guest reading root (should work - guest can read)"),
        ("guest", "write", "/", False, "Guest writing to root (should fail - guest can't write)"),
    ]
    
    for user, op, path, expected, description in test_cases:
        print(f"\nTest: {description}")
        print(f"  Input: user='{user}', op='{op}', path='{path}'")
        
        result = authorize(user, op, path)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"  Result: {result} (expected {expected}) - {status}")
        
        if result != expected:
            # Show detailed breakdown for failures
            details = check_individual_models(user, op, path)
            print("  Detailed breakdown:")
            for model, (allowed, reason) in details.items():
                print(f"    {model}: {'✓' if allowed else '✗'} {reason}")

def test_path_matching():
    print_separator("PATH MATCHING TESTS")
    
    test_cases = [
        ("test", "read", "/"),
        ("test", "read", "/public"),
        ("test", "read", "/public/file.txt"),
        ("test", "read", "/internal/doc.pdf"),
        ("test", "read", "/confidential/secret.txt"),
        ("test", "read", "/nonexistent/path"),
    ]
    
    for user, op, path in test_cases:
        print(f"\nTesting path matching: {path}")
        result = authorize(user, op, path)
        print(f"  Result: {'✓ ALLOWED' if result else '✗ DENIED'}")

def main():
    print("AUTHORIZATION SYSTEM TEST")
    print("=" * 60)
    
    # Clear any cached data to ensure fresh load
    clear_cache()
    
    test_user_info()
    test_individual_models()
    test_combined_authorization()
    test_path_matching()
    
    print_separator("TEST COMPLETE")
    print("Check audit.jsonl for detailed access logs")

if __name__ == "__main__":
    main()