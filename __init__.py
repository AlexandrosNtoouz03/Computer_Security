"""
Computer Security Group Assignment - Secure SFTP Server

A comprehensive implementation of a secure SFTP server with multi-model
authorization system demonstrating advanced security principles.

Main Components:
    - SFTP Server with SSH authentication
    - Multi-model authorization (DAC + MAC + RBAC)
    - Interactive client with full command support
    - Comprehensive test suite
    - Interactive launchers and utilities

Security Models:
    DAC (Discretionary Access Control):
        - File ownership-based permissions
        - Permission bits (read, write, execute)
        
    MAC (Mandatory Access Control):
        - Bell-LaPadula security model
        - Security clearance levels (unclassified → secret)
        - No read up, no write down enforcement
        
    RBAC (Role-Based Access Control):
        - Role-based operation permissions
        - User-role assignments
        - Granular permission control

Features:
    - Triple authorization (all models must approve)
    - Secure password storage with scrypt hashing
    - Comprehensive audit logging
    - Real-time authorization feedback
    - Interactive configuration utilities
    - Production-ready deployment

Usage:
    # Interactive launcher (recommended)
    python launcher.py
    
    # Direct server start
    python main.py
    
    # Interactive client
    python client/client.py
    
    # Run tests
    python -m pytest tests/ -v

Architecture:
    client/     - SFTP client implementation
    server/     - Server components and authorization
    data/       - Configuration files and user data
    tests/      - Comprehensive test suite
    
Educational Objectives:
    - Multi-layered access control implementation
    - Secure network protocol usage
    - System security architecture
    - Comprehensive testing methodologies
    - Security audit and compliance
"""

from server import authenticate, authorize
from client import main as client_main

__version__ = "1.0.0"
__author__ = "Computer Security Group Assignment - Maastricht University"
__license__ = "Educational Use"
__description__ = "Secure SFTP Server with Multi-Model Authorization"

# Package metadata
__all__ = [
    'authenticate',
    'authorize', 
    'client_main'
]

# Project information
PROJECT_INFO = {
    'name': 'Computer Security SFTP Server',
    'version': __version__,
    'author': __author__,
    'description': __description__,
    'security_models': ['DAC', 'MAC', 'RBAC'],
    'features': [
        'Multi-model authorization',
        'Secure SFTP protocol',
        'Interactive client/server',
        'Comprehensive audit logging',
        'Bell-LaPadula MAC model',
        'Role-based permissions',
        'Scrypt password hashing'
    ],
    'components': {
        'server': 'SFTP server with authorization',
        'client': 'Interactive SFTP client', 
        'auth': 'Authentication system',
        'policy': 'Authorization engine',
        'tests': 'Comprehensive test suite'
    }
}

def get_project_info():
    """Return project information dictionary"""
    return PROJECT_INFO.copy()

def print_project_info():
    """Print formatted project information"""
    info = PROJECT_INFO
    print("=" * 60)
    print(f"🔐 {info['name']}")
    print("=" * 60)
    print(f"Version: {info['version']}")
    print(f"Author: {info['author']}")
    print(f"Description: {info['description']}")
    print(f"\nSecurity Models: {', '.join(info['security_models'])}")
    print(f"\nKey Features:")
    for feature in info['features']:
        print(f"  • {feature}")
    print("\nComponents:")
    for comp, desc in info['components'].items():
        print(f"  • {comp}: {desc}")
    print("=" * 60)