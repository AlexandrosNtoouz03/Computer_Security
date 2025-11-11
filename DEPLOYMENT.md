# 🚀 Deployment Guide

## 📋 **Prerequisites**

### **System Requirements**
- **Python**: 3.8+ (tested with 3.13)
- **Operating System**: Windows/macOS/Linux
- **Network**: Port 2222 available for SFTP server
- **Memory**: 100MB+ available RAM

### **Dependencies**
```bash
pip install asyncssh pytest
```

## 🔧 **Initial Setup**

### **1. Clone/Extract Project**
```bash
# Extract to desired location
cd /path/to/Computer_Security
```

### **2. Install Dependencies** 
```bash
pip install -r requirements.txt
```

### **3. Generate SSH Host Key**
```bash
# Automatic generation (recommended)
python generate_ssh_key.py

# Manual generation (alternative)
ssh-keygen -t ed25519 -f ssh_host_ed25519_key -N ""
```

**Expected output:**
```
✅ Generated SSH host key pair:
  - ssh_host_ed25519_key (private key)
  - ssh_host_ed25519_key.pub (public key)
✅ Set secure permissions on private key
```

### **4. Verify Configuration Files**

Ensure these data files exist and are populated:
- `data/users.json` - User credentials
- `data/user_roles.json` - Role assignments  
- `data/role_perms.csv` - Role permissions
- `data/dac_owners.csv` - File ownership
- `data/mac_labels.json` - Security labels

## ▶️ **Starting the Server**

### **Production Start**
```bash
python main.py
```

**Expected output:**
```
Jail root: /path/to/Computer_Security/sftp_root
2024-11-11 10:54:00,700 INFO asyncssh: Creating SSH listener on port 2222
SFTP listening on 0.0.0.0:2222 (subsystem 'sftp')
```

### **Background Service (Linux/macOS)**
```bash
# Using nohup
nohup python main.py > server.log 2>&1 &

# Using systemd (create service file)
sudo systemctl start sftp-secure.service
```

### **Windows Service**
```powershell
# Run in background
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

## 🔌 **Client Connection**

### **Interactive Client**
```bash
python client/client.py
```

### **Custom Connection**
```bash
python client/client.py host port username password
# Example:
python client/client.py 192.168.1.100 2222 admin admin
```

### **Standard SFTP Clients**
```bash
# OpenSSH SFTP client
sftp -P 2222 test@localhost

# FileZilla, WinSCP, etc.
# Host: localhost, Port: 2222, Protocol: SFTP
```

## 🔧 **Configuration**

### **Server Settings**
Edit `main.py` to modify:
```python
HOST_KEY_PATH = './ssh_host_ed25519_key'  # SSH key location
LISTEN_HOST = ''                          # Bind address ('' = all interfaces)
LISTEN_PORT = 2222                        # Server port  
JAIL_ROOT = './sftp_root'                 # File root directory
```

### **User Management**

#### **Add New User**
1. **Generate password hash:**
```bash
python generate_passwords.py
# Edit the script to add your new user
```

2. **Add to users.json:**
```json
{
  "username": "newuser",
  "salt": "base64-encoded-salt",
  "password_hash": "base64-encoded-hash", 
  "clearance": "confidential"
}
```

3. **Assign roles in user_roles.json:**
```json
{
  "newuser": ["editor"]
}
```

#### **Modify Permissions**
Edit `data/role_perms.csv`:
```csv
role,operation,allowed
editor,read,1
editor,write,1
editor,delete,0
```

### **Security Labels**
Edit `data/mac_labels.json`:
```json
{
  "paths": {
    "/": "unclassified",
    "/confidential": "confidential",
    "/secret": "secret"
  },
  "clearance_hierarchy": {
    "unclassified": 0,
    "internal": 1, 
    "confidential": 2,
    "secret": 3,
    "top_secret": 4
  }
}
```

### **File Ownership**
Edit `data/dac_owners.csv`:
```csv
path,owner,permissions
/,admin,rwx
/public,guest,r--
/private,admin,rwx
```

## 🛡️ **Security Hardening**

### **SSH Key Security**
```bash
# Set restrictive permissions on private key
chmod 600 ssh_host_ed25519_key
chmod 644 ssh_host_ed25519_key.pub
```

### **Network Security**
```bash
# Firewall rules (Linux)
sudo ufw allow 2222/tcp

# Windows Firewall
netsh advfirewall firewall add rule name="SFTP Server" dir=in action=allow protocol=TCP localport=2222
```

### **File System Security**
```bash
# Restrict jail root access
chmod 755 sftp_root/
chown sftp-server:sftp-server sftp_root/
```

### **Audit Log Security**
```bash
# Protect audit log from tampering
chmod 644 audit.jsonl
# Consider log rotation for production
```

## 🧪 **Validation**

### **1. Run Tests**
```bash
pytest tests/ -v
```
**Expected: 12/12 tests passing**

### **2. Connection Test**
```bash
python test_integration.py
```

### **3. Authorization Test**
```bash
python test_authorization.py
```

### **4. Client Test**
```bash
python client/client.py
# Try commands: pwd, ls, mkdir test_dir
```

## 📊 **Monitoring**

### **Audit Log Analysis**
```bash
# View recent access attempts
tail -f audit.jsonl

# Count failed attempts  
grep '"allowed": false' audit.jsonl | wc -l

# User activity summary
grep '"user": "admin"' audit.jsonl | jq '.op' | sort | uniq -c
```

### **Server Health**
```bash
# Check if server is running
netstat -an | grep :2222

# Monitor resource usage
ps aux | grep python
```

### **Log Rotation (Production)**
```bash
# Linux logrotate configuration
/var/log/sftp-server/audit.jsonl {
    weekly
    rotate 52
    compress  
    notifempty
    create 644 sftp-server sftp-server
}
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"Port already in use"**
```bash
# Find process using port
netstat -tulpn | grep :2222
# Kill process
kill -9 <PID>
```

#### **"SSH host key not found"** 
```bash
python generate_ssh_key.py
```

#### **"Permission denied" for all operations**
- Check user exists in `data/users.json`
- Verify password hash is correct
- Check user has roles assigned
- Review `audit.jsonl` for detailed denial reasons

#### **"Authorization denied"**
- Verify user clearance level vs. file security label
- Check role permissions in `data/role_perms.csv`  
- Ensure file ownership in `data/dac_owners.csv`
- Review MAC model rules (no read up, no write down)

#### **Client connection failed**
- Verify server is running: `netstat -an | grep :2222`
- Check firewall rules
- Test with: `telnet localhost 2222`

### **Debug Mode**
Enable detailed logging in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### **Reset to Defaults**
```bash
# Regenerate default users
python generate_passwords.py

# Clear audit log
> audit.jsonl

# Reset file permissions
python test_authorization.py
```

## 🔄 **Updates & Maintenance**

### **Adding Security Models**
1. Extend `server/policy.py`
2. Add new `_check_model()` function
3. Update `authorize()` to include new model
4. Add tests in `tests/test_policy.py`

### **Configuration Changes**
- Clear cache: `policy.clear_cache()`
- Restart server for changes to take effect
- Test changes with: `python test_authorization.py`

### **Data Backup**
```bash
# Backup critical configuration
tar -czf config-backup.tar.gz data/ ssh_host_ed25519_key*
```

---

## 📞 **Support**

For issues or questions:
1. Check `audit.jsonl` for detailed error reasons
2. Run `python test_integration.py` for system validation
3. Review this deployment guide
4. Check project README.md for architecture details

**🎓 Computer Security Group Assignment - Maastricht University**