# 🔐 Secure SFTP Server with Multi-Layer Authorization

A comprehensive SFTP server implementation demonstrating enterprise-grade security controls including DAC, MAC, and RBAC authorization models.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AsyncSSH](https://img.shields.io/badge/AsyncSSH-2.x-green) 
![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-red)
![Tests](https://img.shields.io/badge/Tests-12%2F12%20Passing-brightgreen)

## 🔐 Security Architecture

This project implements a **triple-layer authorization system** that demonstrates advanced cybersecurity concepts:

### 1. **DAC (Discretionary Access Control)**
- File ownership and permission-based access
- Owner-controlled resource sharing
- Traditional Unix-style permissions

### 2. **MAC (Mandatory Access Control)** 
- **Bell-LaPadula Model** implementation
- Information flow control (no read up, no write down)
- Security clearance levels: `unclassified` → `internal` → `confidential` → `secret`

### 3. **RBAC (Role-Based Access Control)**
- Operation-based permissions per role
- Roles: `admin`, `editor`, `reader`, `guest`
- Fine-grained SFTP operation control

## 🚀 Features

- ✅ **Secure Authentication**: scrypt password hashing (16384 iterations)
- ✅ **Comprehensive Authorization**: All three security models enforced simultaneously  
- ✅ **Complete Audit Trail**: All access attempts logged to `audit.jsonl`
- ✅ **Honeypot Detection**: 5 honeypot accounts for intrusion monitoring
- ✅ **Interactive SFTP Client**: Full-featured client with all SFTP operations
- ✅ **Production Ready**: Enterprise-grade security controls

## 📋 Requirements

```
Python 3.8+
asyncssh >= 2.0.0
tabulate >= 0.9.0
pytest >= 7.0.0 (for testing)
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd computer-security-sftp
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Start the SFTP server:**
```bash
python main.py
```

4. **Connect using the interactive client:**
```bash
python client/client.py
```

## 👥 User Accounts

The system includes test accounts with different security clearances and roles:

| Username | Clearance     | Role   | Capabilities              |
|----------|---------------|--------|---------------------------|
| test     | internal      | reader | Read operations only      |
| admin    | secret        | admin  | Full administrative access|
| alice    | confidential  | editor | Read, write, create files |
| bob      | internal      | reader | Read operations only      |
| charlie  | unclassified  | guest  | Limited access           |
| demo     | unclassified  | guest  | Demo/testing account     |

> **Note**: Contact your administrator for account passwords. Passwords are not displayed for security reasons.

## 🧪 Testing

Run the comprehensive test suite to verify all security components:

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/test_policy.py -v      # Authorization tests
python -m pytest tests/test_sftp_basic.py -v  # Integration tests
```

**Expected Result:** 12/12 tests passing ✅

## 📊 Security Controls Matrix

| Control Type | Implementation | Status |
|--------------|---------------|---------|
| Authentication | scrypt hashing + secure passwords | ✅ Active |
| Authorization | DAC + MAC + RBAC (triple layer) | ✅ Active |  
| Audit Logging | Complete operation logging | ✅ Active |
| Intrusion Detection | Honeypot accounts | ✅ Active |
| Data Protection | SSH/SFTP encryption | ✅ Active |
| Access Control | Role-based restrictions | ✅ Active |

## 🔍 Usage Examples

### Basic SFTP Operations
```bash
# Connect to server
python client/client.py

# Inside SFTP client:
sftp:/> pwd              # Show current directory
sftp:/> ls               # List directory contents  
sftp:/> get file.txt     # Download file
sftp:/> put local.txt    # Upload file
sftp:/> mkdir newdir     # Create directory
sftp:/> stat file.txt    # Show file statistics
```

### Authorization Testing
```python
# Test authorization for specific operations
from server.policy import authorize

# Check if user can read a file
authorize("alice", "read", "/confidential/data.txt")  # True (clearance match)
authorize("bob", "read", "/confidential/data.txt")    # False (insufficient clearance)

# Check role permissions  
authorize("admin", "delete", "/any/file.txt")         # True (admin role)
authorize("guest", "delete", "/any/file.txt")         # False (guest role)
```

## 🔧 Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SFTP Client   │────│   SFTP Server   │────│ Authorization   │
│                 │    │    (main.py)    │    │   Engine        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                │                       ▼
                         ┌─────────────────┐    ┌─────────────────┐
                         │ Authentication  │    │   Audit Logger  │
                         │   (auth.py)     │    │                 │
                         └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
├── main.py              # SFTP server with authorization integration
├── client/
│   └── client.py        # Interactive SFTP client
├── server/
│   ├── auth.py          # Authentication & password verification  
│   ├── policy.py        # Authorization engine (DAC/MAC/RBAC)
│   └── sftp.py          # SFTP protocol utilities
├── data/
│   ├── users.json       # User accounts & security clearances
│   ├── user_roles.json  # User-to-role mappings
│   ├── role_perms.csv   # Role permission definitions
│   ├── dac_owners.csv   # File ownership information
│   └── mac_labels.json  # MAC security labels
├── tests/               # Comprehensive test suite
└── sftp_root/          # SFTP server file system root
```

## 🛡️ Security Considerations

- **Production Deployment**: Change all default passwords and regenerate SSH host keys
- **Network Security**: Use firewall rules to restrict SFTP server access
- **Monitoring**: Monitor `audit.jsonl` for suspicious activity
- **Honeypot Alerts**: Set up alerting for honeypot account login attempts
- **Regular Updates**: Keep AsyncSSH and Python dependencies updated

## 📜 License

This project is for educational purposes demonstrating cybersecurity concepts including access control models, secure authentication, and intrusion detection.

## 🤝 Contributing

This is an academic project showcasing security implementations. For educational use and security research.

---

**⚠️ Disclaimer**: This is a demonstration system for educational purposes. Ensure proper security review before any production deployment.