"""
Unit test template for DAC, MAC, and RBAC logic.
"""
from server import policy

def test_audit_log_created(tmp_path, monkeypatch):
    test_file = tmp_path / "audit.jsonl"
    monkeypatch.setattr(policy, "AUDIT_LOG", str(test_file))
    policy._audit("alice", "read", "/demo.txt", True, "test ok")
    text = test_file.read_text()
    assert "alice" in text
