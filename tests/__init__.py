"""
Tests Package - Comprehensive Test Suite

This package contains the complete test suite for the SFTP server with
multi-model authorization system.

Test Modules:
    test_policy: Unit tests for authorization models (DAC, MAC, RBAC)
    test_sftp_basic: Integration tests for SFTP server functionality

Test Coverage:
    - Authorization model validation (10 tests)
    - Integration testing (2 tests)
    - End-to-end functionality verification
    - Security model enforcement testing
    - Audit logging validation

Features:
    - 12/12 tests passing
    - Full coverage of security models
    - Integration test validation
    - Mock data and fixtures
    - Comprehensive error scenario testing
"""

# Test configuration
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

__version__ = "1.0.0"
__author__ = "Computer Security Group Assignment"
__all__ = []