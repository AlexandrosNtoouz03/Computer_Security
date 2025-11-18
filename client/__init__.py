"""
Client Package - SFTP Client Implementation

This package contains the SFTP client implementation with interactive commands
and authorization-aware functionality.

Modules:
    client: Interactive SFTP client with full command support

Features:
    - Interactive command-line interface
    - Real-time authorization feedback
    - Support for all SFTP operations (ls, get, put, mkdir, stat, etc.)
    - Multiple authentication methods
    - Secure connection handling
"""

from .client import main

__version__ = "1.0.0"
__author__ = "Computer Security Group Assignment"
__all__ = ['main']