# 🔐 Secure SFTP Server with Multi-Model Authorization

A comprehensive Computer Security group assignment implementing a secure SFTP server with triple-layer authorization (DAC, MAC, RBAC) and comprehensive audit logging.

## 🎯 **Project Overview**

This project demonstrates advanced security principles through:

- **🔒 Triple Authorization Model**: DAC + MAC + RBAC working together
- **🌐 Secure SFTP Protocol**: Full implementation with SSH authentication  
- **📝 Comprehensive Auditing**: Complete access trail logging
- **🧪 Extensive Testing**: 12/12 tests passing with full coverage
- **🖥️ Interactive Client**: Full-featured SFTP client with authorization enforcement

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    SFTP Client                              │
│  (Interactive commands: ls, get, put, mkdir, stat, etc.)   │
└─────────────────────┬───────────────────────────────────────┘
                      │ SSH/SFTP Protocol (Port 2222)
┌─────────────────────▼───────────────────────────────────────┐
│                 SFTP Server                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            Authorization Engine                     │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐  │    │
│  │  │   DAC   │  │   MAC   │  │        RBAC         │  │    │
│  │  │(Owners) │  │(Labels) │  │(Roles & Perms)      │  │    │
│  │  └─────────┘  └─────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Audit Logger                           │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 🔐 **Security Models**

### **1. DAC (Discretionary Access Control)**
- **Principle**: File ownership and permission bits
- **Data**: `data/dac_owners.csv`
- **Rules**: Owners have full control; others subject to rwx permissions

### **2. MAC (Mandatory Access Control)** 
- **Principle**: Bell-LaPadula security model
- **Data**: `data/mac_labels.json`
- **Clearance Levels**: unclassified(0) → internal(1) → confidential(2) → secret(3) → top_secret(4)
- **Rules**: 
  - **No Read Up**: Cannot read above clearance level
  - **No Write Down**: Cannot write below clearance level

### **3. RBAC (Role-Based Access Control)**
- **Principle**: Role-based operation permissions  
- **Data**: `data/user_roles.json`, `data/role_perms.csv`
- **Roles**: admin, editor, reader, guest
- **Operations**: read, write, create, mkdir, delete

## 👥 **User Accounts**

| User   | Password | Clearance     | Role   | Can Read           | Can Write          |
|--------|----------|---------------|--------|--------------------|-------------------|
| test   | test     | internal      | reader | /, /internal       | None (reader)     |
| admin  | admin    | secret        | admin  | All levels         | All levels        |
| editor | editor   | confidential  | editor | Up to confidential | Up to confidential|
| guest  | guest    | unclassified  | guest  | /public only       | None              |

## 🚀 **Quick Start**

### **Prerequisites**
```bash
# Install dependencies
pip install -r requirements.txt

# Packages needed:
# - asyncssh (SFTP server/client)
# - pytest (testing framework)
```

### **🎯 Main Launcher (Easiest)**

#### **🚀 Comprehensive System Launcher**
```bash
python launcher.py
```
**All-in-one menu with options for:**
- 🚀 Interactive server startup
- 🖥️ Interactive client connection
- 🧪 System testing and validation
- 🔧 Utilities (SSH keys, passwords, audit logs)
- 📚 Documentation viewing

#### **Windows Users:**
```cmd
launch_server.bat    # Start server with dependency checking
launch_client.bat    # Start client with dependency checking
```

### **Option 1: Interactive Setup**

#### **Interactive Server Launcher**
```bash
python start_server.py
```
- Prompts for host, port, SSH key path, jail root directory
- Shows available user accounts
- Generates SSH key if needed
- Confirms settings before starting

#### **Interactive Client Launcher**
```bash
python start_client.py
```
- Prompts for server details and credentials
- Shows available test accounts
- Displays connection summary and available commands

### **Option 2: Direct Launch**

#### **1. Generate SSH Host Key**
```bash
python generate_ssh_key.py
```

#### **2. Start SFTP Server**
```bash
python main.py
```
Server will start on `localhost:2222`

#### **3. Connect with Client**
```bash
python client/client.py
```

Default connection: `test/test` on `127.0.0.1:2222`

## 🖥️ **Client Commands**

Once connected to the SFTP client:

```bash
help                    # Show available commands
pwd                     # Print working directory  
ls [path]              # List directory contents
cd <path>              # Change directory
get <remote> [local]   # Download file from server
put <local> [remote]   # Upload file to server
mkdir <dir>            # Create directory
stat <path>            # Show file/directory statistics
exit                   # Exit client
```

## 🧪 **Testing**

### **Run All Tests**
```bash
pytest tests/ -v
```

Expected output: **12/12 tests passing**

### **Manual Integration Test**
```bash
python test_integration.py
```

### **Authorization Test**
```bash
python test_authorization.py
```

## 📁 **Project Structure**

```
Computer_Security/
├── 📋 README.md                 # This file
├── 🖥️ main.py                   # SFTP server entry point
├── 🔑 ssh_host_ed25519_key      # SSH server private key
├── 📦 requirements.txt          # Python dependencies  
├── client/
│   └── 🖥️ client.py             # Interactive SFTP client
├── server/
│   ├── 🔐 auth.py               # Password authentication
│   ├── 🛡️ policy.py             # Authorization engine (DAC/MAC/RBAC)
│   ├── 🌐 server.py             # SSH server (legacy)
│   └── 📁 sftp.py               # SFTP protocol (legacy)
├── data/
│   ├── 👥 users.json            # User credentials & clearance
│   ├── 🔗 user_roles.json       # User-role mappings
│   ├── 📊 role_perms.csv         # Role permissions
│   ├── 🏠 dac_owners.csv         # File ownership data
│   └── 🏷️ mac_labels.json        # Security labels & hierarchy
├── tests/
│   ├── 🧪 test_policy.py        # Authorization unit tests
│   └── 🔗 test_sftp_basic.py    # Integration tests
└── 📁 sftp_root/                # SFTP jail directory
```

## 🔍 **Security Features**

### **🛡️ Defense in Depth**
- **Triple Authorization**: All three models (DAC, MAC, RBAC) must approve access
- **Fail-Safe Defaults**: Denies access when configuration data missing/invalid
- **Comprehensive Auditing**: Every access attempt logged with detailed reasoning

### **🔒 Authentication**
- **Scrypt Password Hashing**: Secure password storage with salt
- **SSH Key Authentication**: Server identity verification
- **Connection Security**: Full SSH protocol encryption

### **📝 Audit Trail**
All access attempts logged to `audit.jsonl`:
```json
{
  "ts": "2024-11-11T10:30:15Z",
  "user": "test", 
  "op": "read",
  "path": "/confidential",
  "allowed": false,
  "reason": "Authorization DENIED - DAC: ✓ owner access | MAC: ✗ MAC read denied: internal(1) < confidential(2) | RBAC: ✓ RBAC allowed by roles: ['reader']"
}
```

## ⚙️ **Configuration**

### **Adding Users**
1. Edit `data/users.json` - add user with scrypt password hash
2. Edit `data/user_roles.json` - assign roles  
3. Use `generate_passwords.py` to create proper password hashes

### **Setting File Permissions**
Edit `data/dac_owners.csv`:
```csv
path,owner,permissions
/new_directory,username,rwx
```

### **Configuring Security Labels**
Edit `data/mac_labels.json`:
```json
{
  "paths": {
    "/new_path": "confidential"
  }
}
```

### **Managing Role Permissions**
Edit `data/role_perms.csv`:
```csv
role,operation,allowed
new_role,read,1
new_role,write,0
```

## 🐛 **Troubleshooting**

### **"SSH host key not found"**
```bash
python generate_ssh_key.py
```

### **"Port 2222 already in use"**
```bash
# Kill existing server or change port in main.py
netstat -ano | findstr :2222
```

### **"Authorization denied"**
- Check user exists in `data/users.json`
- Verify user has proper clearance level
- Check role permissions in `data/role_perms.csv`
- Review audit log in `audit.jsonl`

### **Authentication Failed**
- Verify username/password combination
- Use `debug_auth.py` to test authentication
- Regenerate password hashes with `generate_passwords.py`

## 📚 **Educational Objectives**

This project demonstrates:

1. **🔐 Access Control Models**: Practical implementation of DAC, MAC, and RBAC
2. **🌐 Network Security**: SSH protocol and secure client-server communication
3. **🏗️ System Design**: Modular architecture with separation of concerns
4. **🧪 Security Testing**: Comprehensive test coverage and validation
5. **📝 Audit Logging**: Security event tracking and analysis
6. **🛡️ Defense in Depth**: Multiple security layers working together

## 📖 **References**

- Bell-LaPadula Model: Classical MAC security model
- SFTP Protocol: SSH File Transfer Protocol (RFC 4251-4254)
- AsyncSSH Library: Python SSH implementation
- Scrypt Algorithm: Secure password hashing

---

## 🎓 **Computer Security Group Assignment**
**Maastricht University**

*Implementing comprehensive authorization models with secure network protocols*
