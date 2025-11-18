"""
Server Package - SFTP Server with Multi-Model Authorization

This package contains the core server components with integrated
DAC, MAC, and RBAC authorization models.

Modules:
    auth: Password authentication with scrypt hashing
    policy: Multi-model authorization engine (DAC + MAC + RBAC)

Security Models:
    - DAC: Discretionary Access Control (file ownership)
    - MAC: Mandatory Access Control (Bell-LaPadula model)
    - RBAC: Role-Based Access Control (role permissions)

Features:
    - Triple-layer authorization (all models must approve)
    - Comprehensive audit logging
    - Secure password storage with scrypt
    - Bell-LaPadula security model enforcement
    - Role-based permission management
"""

from .auth import authenticate
from .policy import authorize, get_user_info, clear_cache

__version__ = "1.0.0"
__author__ = "Computer Security Group Assignment"
__all__ = ['authenticate', 'authorize', 'get_user_info', 'clear_cache']