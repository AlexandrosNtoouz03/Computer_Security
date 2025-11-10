"""
Implements authorization models (DAC, MAC, RBAC) and auditing.
Just basics
"""
import json, os, time

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AUDIT_LOG = os.path.join(os.path.dirname(__file__), "..", "audit.jsonl")

def authorize(user: str, op: str, path: str) -> bool:
    """
    TODO: Perform DAC, MAC, and RBAC checks.
    For now returns False and logs the attempt.
    """
    allowed = False
    reason = "not yet implemented"
    _audit(user, op, path, allowed, reason)
    return allowed

def _audit(user, op, path, allowed, reason):
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": user, "op": op, "path": path,
        "allowed": allowed, "reason": reason
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
