"""
Unit tests for DAC, MAC, and RBAC authorization logic.
"""
import pytest
import tempfile
import os
from server import policy

@pytest.fixture
def temp_audit_log(tmp_path, monkeypatch):
    """Create a temporary audit log for testing"""
    test_file = tmp_path / "audit.jsonl"
    monkeypatch.setattr(policy, "AUDIT_LOG", str(test_file))
    return test_file

def test_audit_log_created(temp_audit_log):
    """Test that audit logs are properly created"""
    policy._audit("alice", "read", "/demo.txt", True, "test ok")
    text = temp_audit_log.read_text()
    assert "alice" in text
    assert "read" in text
    assert "demo.txt" in text
    assert "test ok" in text

def test_dac_owner_access():
    """Test DAC allows owners full access"""
    policy.clear_cache()  # Ensure fresh data
    allowed, reason = policy._check_dac("test", "read", "/")
    assert allowed == True
    assert "owner access" in reason

def test_dac_non_owner_permissions():
    """Test DAC permissions for non-owners"""
    policy.clear_cache()
    # Test read permission for non-owner (assuming 'admin' is not owner of '/')
    allowed, reason = policy._check_dac("admin", "read", "/")
    assert allowed == True  # Should have read permission
    assert "read permission granted" in reason

def test_mac_clearance_levels():
    """Test MAC Bell-LaPadula model"""
    policy.clear_cache()
    
    # Test read up prevention: internal user cannot read confidential
    allowed, reason = policy._check_mac("test", "read", "/confidential")
    assert allowed == False
    assert "MAC read denied" in reason
    
    # Test write down prevention: secret user cannot write to unclassified
    allowed, reason = policy._check_mac("admin", "write", "/")
    assert allowed == False
    assert "MAC write denied" in reason

def test_rbac_role_permissions():
    """Test RBAC role-based permissions"""
    policy.clear_cache()
    
    # Test reader can read
    allowed, reason = policy._check_rbac("test", "read", "/")
    assert allowed == True
    assert "RBAC allowed by roles" in reason
    
    # Test reader cannot write
    allowed, reason = policy._check_rbac("test", "write", "/")
    assert allowed == False
    assert "RBAC denied" in reason

def test_combined_authorization():
    """Test complete authorization requiring all three models"""
    policy.clear_cache()
    
    # Case where all models should allow
    result = policy.authorize("test", "read", "/")
    assert result == True
    
    # Case where RBAC should deny (reader cannot write)
    result = policy.authorize("test", "write", "/")
    assert result == False
    
    # Case where MAC should deny (insufficient clearance)
    result = policy.authorize("test", "read", "/confidential")
    assert result == False

def test_user_info_retrieval():
    """Test user information retrieval"""
    policy.clear_cache()
    
    # Test existing user
    info = policy.get_user_info("test")
    assert info is not None
    assert info["username"] == "test"
    assert info["clearance"] == "internal"
    assert "reader" in info["roles"]
    
    # Test non-existent user
    info = policy.get_user_info("nonexistent")
    assert info is None

def test_path_matching():
    """Test path matching logic"""
    policy.clear_cache()
    
    # Test exact path match
    owners = {"/test": ("owner", "rwx")}
    match = policy._find_best_matching_path("/test", owners)
    assert match == "/test"
    
    # Test parent path matching
    owners = {"/": ("owner", "rwx"), "/documents": ("owner", "rwx")}
    match = policy._find_best_matching_path("/documents/file.txt", owners)
    assert match == "/documents"
    
    # Test root fallback
    owners = {"/": ("owner", "rwx")}
    match = policy._find_best_matching_path("/nonexistent/path", owners)
    assert match == "/"

def test_cache_clearing():
    """Test cache clearing functionality"""
    # Load some data first
    policy._load_users()
    assert len(policy._data_cache) > 0
    
    # Clear cache
    policy.clear_cache()
    assert len(policy._data_cache) == 0

def test_individual_model_checks():
    """Test individual model check function"""
    policy.clear_cache()
    
    results = policy.check_individual_models("test", "read", "/")
    assert "DAC" in results
    assert "MAC" in results  
    assert "RBAC" in results
    
    for model, (allowed, reason) in results.items():
        assert isinstance(allowed, bool)
        assert isinstance(reason, str)
        assert len(reason) > 0
