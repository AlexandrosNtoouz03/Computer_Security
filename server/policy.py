"""
Implements authorization models (DAC, MAC, RBAC) and auditing.
Combines all three access control models for comprehensive security.
"""
import json, os, time, csv
from typing import Dict, List, Optional, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
AUDIT_LOG = os.path.join(os.path.dirname(__file__), "..", "audit.jsonl")

# Cache for loaded data to avoid repeated file I/O
_data_cache = {}

def _load_users() -> List[Dict]:
    """Load user data including clearance levels"""
    if 'users' not in _data_cache:
        users_file = os.path.join(DATA_DIR, "users.json")
        try:
            with open(users_file, "r", encoding="utf-8") as f:
                _data_cache['users'] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _data_cache['users'] = []
    return _data_cache['users']

def _load_user_roles() -> Dict[str, List[str]]:
    """Load user-role mappings"""
    if 'user_roles' not in _data_cache:
        roles_file = os.path.join(DATA_DIR, "user_roles.json")
        try:
            with open(roles_file, "r", encoding="utf-8") as f:
                _data_cache['user_roles'] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _data_cache['user_roles'] = {}
    return _data_cache['user_roles']

def _load_role_permissions() -> Dict[str, Dict[str, bool]]:
    """Load role-permission mappings"""
    if 'role_perms' not in _data_cache:
        perms_file = os.path.join(DATA_DIR, "role_perms.csv")
        perms = {}
        try:
            with open(perms_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    role = row['role']
                    operation = row['operation']
                    allowed = bool(int(row['allowed']))
                    if role not in perms:
                        perms[role] = {}
                    perms[role][operation] = allowed
        except (FileNotFoundError, csv.Error):
            pass
        _data_cache['role_perms'] = perms
    return _data_cache['role_perms']

def _load_dac_owners() -> Dict[str, Tuple[str, str]]:
    """Load DAC ownership data"""
    if 'dac_owners' not in _data_cache:
        owners_file = os.path.join(DATA_DIR, "dac_owners.csv")
        owners = {}
        try:
            with open(owners_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    owners[row['path']] = (row['owner'], row['permissions'])
        except (FileNotFoundError, csv.Error):
            pass
        _data_cache['dac_owners'] = owners
    return _data_cache['dac_owners']

def _load_mac_labels() -> Dict:
    """Load MAC security labels and hierarchy"""
    if 'mac_labels' not in _data_cache:
        labels_file = os.path.join(DATA_DIR, "mac_labels.json")
        try:
            with open(labels_file, "r", encoding="utf-8") as f:
                _data_cache['mac_labels'] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _data_cache['mac_labels'] = {"paths": {}, "clearance_hierarchy": {}}
    return _data_cache['mac_labels']

def _get_user_clearance(username: str) -> str:
    """Get user's security clearance level"""
    users = _load_users()
    user = next((u for u in users if u.get("username") == username), None)
    return user.get("clearance", "unclassified") if user else "unclassified"

def _find_best_matching_path(target_path: str, available_paths: Dict) -> Optional[str]:
    """Find the most specific matching path for authorization"""
    target_path = target_path.rstrip('/')
    if not target_path:
        target_path = '/'
    
    # Try exact match first
    if target_path in available_paths:
        return target_path
    
    # Find the longest matching parent path
    best_match = None
    best_length = -1
    
    for path in available_paths.keys():
        path_clean = path.rstrip('/')
        if not path_clean:
            path_clean = '/'
            
        # Check if this path is a parent of target_path
        if target_path == path_clean or target_path.startswith(path_clean + '/'):
            if len(path_clean) > best_length:
                best_length = len(path_clean)
                best_match = path
                
    # If no parent found, use root if available
    if best_match is None and '/' in available_paths:
        best_match = '/'
        
    return best_match

def _check_dac(user: str, op: str, path: str) -> Tuple[bool, str]:
    """Discretionary Access Control - check file ownership and permissions"""
    owners = _load_dac_owners()
    
    matching_path = _find_best_matching_path(path, owners)
    if not matching_path:
        return False, "no DAC entry found"
    
    owner, perms = owners[matching_path]
    
    # Owner has full control
    if user == owner:
        return True, "owner access"
    
    # Check permissions for non-owners (simplified - treating as "other" permissions)
    if op in ['read', 'stat', 'realpath', 'opendir', 'readdir'] and 'r' in perms:
        return True, "read permission granted"
    elif op in ['write', 'create', 'mkdir'] and 'w' in perms:
        return True, "write permission granted"
    elif op == 'delete' and 'x' in perms:  # Using execute bit for delete
        return True, "delete permission granted"
    
    return False, f"insufficient DAC permissions ({perms}) for operation {op}"

def _check_mac(user: str, op: str, path: str) -> Tuple[bool, str]:
    """Mandatory Access Control - check security labels and clearance"""
    mac_data = _load_mac_labels()
    user_clearance = _get_user_clearance(user)
    
    # Find the security label for this path
    matching_path = _find_best_matching_path(path, mac_data["paths"])
    if not matching_path:
        # Default to unclassified if no label found
        file_label = "unclassified"
    else:
        file_label = mac_data["paths"][matching_path]
    
    hierarchy = mac_data["clearance_hierarchy"]
    user_level = hierarchy.get(user_clearance, 0)
    file_level = hierarchy.get(file_label, 0)
    
    # Bell-LaPadula model: no read up, no write down
    if op in ['read', 'stat', 'realpath', 'opendir', 'readdir']:
        # Can read if clearance >= file label (no read up)
        if user_level >= file_level:
            return True, f"MAC read allowed: {user_clearance}({user_level}) >= {file_label}({file_level})"
        else:
            return False, f"MAC read denied: {user_clearance}({user_level}) < {file_label}({file_level})"
    
    elif op in ['write', 'create', 'mkdir', 'delete']:
        # Can write if clearance <= file label (no write down)
        if user_level <= file_level:
            return True, f"MAC write allowed: {user_clearance}({user_level}) <= {file_label}({file_level})"
        else:
            return False, f"MAC write denied: {user_clearance}({user_level}) > {file_label}({file_level})"
    
    return False, f"unknown MAC operation: {op}"

def _check_rbac(user: str, op: str, path: str) -> Tuple[bool, str]:
    """Role-Based Access Control - check user roles and permissions"""
    user_roles = _load_user_roles()
    role_perms = _load_role_permissions()
    
    if user not in user_roles:
        return False, "user has no assigned roles"
    
    user_role_list = user_roles[user]
    if not user_role_list:
        return False, "user has empty role list"
    
    # Check if any of the user's roles allow this operation
    allowed_roles = []
    denied_roles = []
    
    for role in user_role_list:
        if role in role_perms and op in role_perms[role]:
            if role_perms[role][op]:
                allowed_roles.append(role)
            else:
                denied_roles.append(role)
        else:
            denied_roles.append(f"{role}(no-perm)")
    
    if allowed_roles:
        return True, f"RBAC allowed by roles: {allowed_roles}"
    else:
        return False, f"RBAC denied - checked roles: {denied_roles}"

def authorize(user: str, op: str, path: str) -> bool:
    """
    Perform comprehensive authorization using DAC, MAC, and RBAC.
    All three models must allow access for the operation to be authorized.
    """
    # Normalize path
    path = path.strip()
    if not path or path == '.':
        path = '/'
    
    # Check all three access control models
    dac_allowed, dac_reason = _check_dac(user, op, path)
    mac_allowed, mac_reason = _check_mac(user, op, path)
    rbac_allowed, rbac_reason = _check_rbac(user, op, path)
    
    # All models must allow access
    allowed = dac_allowed and mac_allowed and rbac_allowed
    
    # Construct detailed reason
    reasons = [
        f"DAC: {'✓' if dac_allowed else '✗'} {dac_reason}",
        f"MAC: {'✓' if mac_allowed else '✗'} {mac_reason}",
        f"RBAC: {'✓' if rbac_allowed else '✗'} {rbac_reason}"
    ]
    
    final_reason = f"Authorization {'GRANTED' if allowed else 'DENIED'} - " + " | ".join(reasons)
    
    _audit(user, op, path, allowed, final_reason)
    return allowed

def _audit(user, op, path, allowed, reason):
    """Log access attempts for security auditing"""
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "user": user, "op": op, "path": path,
        "allowed": allowed, "reason": reason
    }
    try:
        os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print(f"Failed to write audit log: {e}")

def clear_cache():
    """Clear the data cache - useful for testing or reloading config"""
    global _data_cache
    _data_cache.clear()

def get_user_info(username: str) -> Optional[Dict]:
    """Get comprehensive user information for debugging"""
    users = _load_users()
    user_roles = _load_user_roles()
    
    user_data = next((u for u in users if u.get("username") == username), None)
    if not user_data:
        return None
    
    return {
        "username": username,
        "clearance": user_data.get("clearance", "unclassified"),
        "roles": user_roles.get(username, []),
        "exists": True
    }

def check_individual_models(user: str, op: str, path: str) -> Dict[str, Tuple[bool, str]]:
    """Check each access control model individually - useful for debugging"""
    return {
        "DAC": _check_dac(user, op, path),
        "MAC": _check_mac(user, op, path),
        "RBAC": _check_rbac(user, op, path)
    }
