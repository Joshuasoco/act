# 🎓 PROFESSOR DEMO SCRIPT
## Complete walkthrough for presenting your security project

---

## 📋 DEMO CHECKLIST (Print this!)

### Before Demo:
- [ ] Open VS Code in `c:\dev\activities` folder
- [ ] Have PowerShell terminal ready
- [ ] Have file_encryptor.py, password_manager.py, rbac_system.py visible
- [ ] Know where each key function is (lines noted below)

---

## 🎬 DEMO FLOW (5-10 minutes)

### **INTRODUCTION (30 seconds)**
**What to say:**
"Hello Professor! Today I'll demonstrate three security concepts: file encryption, password hashing, and role-based access control. I've implemented them in Python and can show you how they work."

---

## 🔐 PART 1: PASSWORD MANAGER (2-3 minutes)

### **Step 1: Show the Code**
Open `password_manager.py`

**Point to these sections:**
```
Line 35: Salt generation using secrets.token_hex
Line 38: SHA-256 hashing with salt
Line 42: Password verification by comparing hashes
Line 47: add_user method that stores hashed passwords
Line 64: authenticate method for login
```

**What to say:**z
"This password manager never stores plaintext passwords. When a user registers, we generate a random salt, combine it with their password, and hash it using SHA-256. The hash and salt are stored in a JSON file. During login, we hash the input password with the stored salt and compare hashes."

### **Step 2: Run Live Demo**
```powershell
python test_password_manager.py
```

**Explain the output:**
- "Test 1 shows user registration with hashing"
- "Test 2 demonstrates successful authentication"
- "Test 3 shows failed login with wrong password"
- "Test 4 shows password change functionality"

### **Step 3: Show Stored Data**
```powershell
type test_passwords.json
```

**What to say:**
"Notice the passwords are hashed - even if someone steals this file, they can't get the original passwords. Each user has a unique salt, so even identical passwords have different hashes."

### **If Professor Asks: "Why use salt?"**
**Answer:** "Salt prevents rainbow table attacks. Without salt, attackers could pre-compute hashes for common passwords. With unique salts, they'd need to compute hashes for each user individually, making attacks impractical."

---

## 🔒 PART 2: FILE ENCRYPTION (2-3 minutes)

### **Step 1: Show the Code**
Open `file_encryptor.py`

**Point to these sections:**
```
Line 13: Key derivation using SHA-256
Line 16-22: XOR encryption algorithm
Line 24-30: PKCS7 padding
Line 44-62: encrypt_file method
Line 64-82: decrypt_file method
```

**What to say:**
"This file encryptor uses XOR cipher for encryption. First, we derive a 32-byte key from the password using SHA-256. Then we pad the data to a multiple of 16 bytes using PKCS7. Finally, we XOR each byte with the key."

### **Step 2: Demonstrate Encryption**
```powershell
# Create test file
python -c "from file_encryptor import FileEncryptor; fe = FileEncryptor('mypassword123'); fe.create_test_file('This is confidential data!', 'demo.txt')"

# Show original
type demo.txt

# Encrypt it
python -c "from file_encryptor import FileEncryptor; fe = FileEncryptor('mypassword123'); fe.encrypt_file('demo.txt', 'demo_encrypted.bin'); print('Encrypted!')"

# Show it's encrypted (binary)
powershell -Command "Get-Content demo_encrypted.bin -Encoding Byte -TotalCount 50"

# Decrypt it
python -c "from file_encryptor import FileEncryptor; fe = FileEncryptor('mypassword123'); fe.decrypt_file('demo_encrypted.bin', 'demo_decrypted.txt'); print('Decrypted!')"

# Show decrypted matches original
type demo_decrypted.txt
```

**What to say during demo:**
1. "Here's the original file - readable text"
2. "After encryption, it's binary data - unreadable without the key"
3. "With the correct password, we can decrypt and recover the original"

### **Step 3: Run Full Test**
```powershell
python test_file_encryption.py
```

**Explain:**
"This test shows encryption and decryption working correctly. Notice Test 4 - wrong password causes decryption to fail because the padding becomes invalid."

### **If Professor Asks: "How does XOR work?"**
**Answer:** "XOR is a bitwise operation. If A XOR B = C, then C XOR B = A. This means encryption and decryption use the same operation. For example, 5 XOR 3 = 6, and 6 XOR 3 = 5."

### **If Professor Asks: "Why pad data?"**
**Answer:** "PKCS7 padding ensures data is a multiple of the block size. The padding value indicates how many bytes were added. For example, if we need 3 more bytes, we add [3, 3, 3]. This helps us remove padding correctly after decryption."

---

## 👥 PART 3: RBAC SYSTEM (2-3 minutes)

### **Step 1: Show the Code**
Open `rbac_system.py`

**Point to these sections:**
```
Line 14-22: Role definitions with permissions
Line 42-44: add_user assigns roles
Line 46-53: check_permission verifies access
Line 55-71: can_access_file for file-specific checks
```

**What to say:**
"This is a Role-Based Access Control system. Users are assigned roles like guest, user, editor, or admin. Each role has specific permissions. Before allowing any action, we check if the user's role includes the required permission."

### **Step 2: Run Demo**
```powershell
python test_rbac.py
```

**Explain the output:**
- "Test 1: Guests can only read public files"
- "Test 2: Users can read and write their own files"
- "Test 3: Admins have full access including admin logs"
- "Test 4: Permission escalation is prevented - guests can't access admin logs"

### **Step 3: Show Interactive Example**
```powershell
python
```

Then type:
```python
from rbac_system import RBACSystem
rbac = RBACSystem()

# Add users
rbac.add_user('guest1', 'guest')
rbac.add_user('user1', 'user')
rbac.add_user('admin1', 'admin')

# Check permissions
print("Guest can read public:", rbac.check_permission('guest1', 'read_public'))
print("Guest can delete:", rbac.check_permission('guest1', 'delete_any'))
print("Admin can delete:", rbac.check_permission('admin1', 'delete_any'))

# List all users
print("\nAll users:")
print(rbac.list_users())

exit()
```

**What to say:**
"RBAC follows the principle of least privilege - users only get permissions they need. This prevents unauthorized access and reduces security risks."

### **If Professor Asks: "What's the benefit of RBAC?"**
**Answer:** "RBAC simplifies permission management. Instead of setting permissions per user, we set them per role. If we need to change permissions, we just modify the role definition, not every user. It's also easier to audit - we can see what each role can do."

---

## 🛡️ PART 4: SECURITY TESTS (1 minute)

### **Run Security Tests**
```powershell
python security_test.py
```

**What to say:**
"This validates our implementation - checking for plaintext passwords, verifying encryption works, and ensuring files are properly secured."

---

## 💡 BONUS: CODE MODIFICATION DEMO

### **If Professor Asks: "Can you modify the code?"**

**Example 1: Add password length validation**
```powershell
python
```

```python
from password_manager import PasswordManager

# Original - accepts any password
pm = PasswordManager('demo.json')
pm.add_user('test', 'short')  # Would accept

# Show how to add validation
class SecurePasswordManager(PasswordManager):
    def add_user(self, username, password, role='user'):
        if len(password) < 8:
            print("Error: Password too short!")
            return False
        return super().add_user(username, password, role)

# Now it validates
spm = SecurePasswordManager('demo2.json')
print(spm.add_user('test', 'short'))  # False
print(spm.add_user('test', 'longpassword'))  # True

exit()
```

**Example 2: Show encryption key derivation**
```powershell
python
```

```python
import hashlib

# Show how password becomes key
password = "mypassword123"
key = hashlib.sha256(password.encode('utf-8')).digest()

print(f"Password: {password}")
print(f"Key length: {len(key)} bytes")
print(f"Key (hex): {key.hex()[:40]}...")

exit()
```

---

## 🎯 COMMON PROFESSOR QUESTIONS

### Q: "What's the difference between hashing and encryption?"
**A:** "Hashing is one-way - you can't reverse it. We use it for passwords. Encryption is two-way - you can decrypt with the key. We use it for protecting data that needs to be read later."

### Q: "Why is XOR considered weak?"
**A:** "XOR alone is weak because if an attacker knows part of the plaintext, they can derive the key. We use it here for educational purposes. In production, we'd use AES or ChaCha20."

### Q: "How does PKCS7 padding work?"
**A:** "If data needs N bytes to reach block size, we add N bytes each with value N. For example, need 5 bytes? Add [5,5,5,5,5]. This lets us know how many bytes to remove during decryption."

### Q: "Why store salt with the hash?"
**A:** "We need the same salt to verify passwords later. Since it's random per user, we must store it. Salt doesn't need to be secret - its job is uniqueness, not secrecy."

### Q: "Can you add a new role to RBAC?"
**A:** "Yes! I'd add it to the roles dictionary with its permissions list. For example, 'moderator': ['read_public', 'edit_public', 'moderate_content']. Then users can be assigned that role."

### Q: "What happens if wrong password is used for decryption?"
**A:** "The XOR produces garbage data. When we try to unpad, the padding bytes are invalid, so _unpad_data raises 'Invalid padding length' error."

---

## 🚀 QUICK REFERENCE COMMANDS

```powershell
# Test everything at once
python test_password_manager.py
python test_file_encryption.py  
python test_rbac.py
python security_test.py

# Show specific file
type password_manager.py
type file_encryptor.py
type rbac_system.py

# Interactive Python mode
python
# Then import and demonstrate functions

# Check Python version
python --version

# List all files
dir *.py
```

---

## ✅ FINAL TIPS

1. **Speak confidently** - You built this!
2. **Point to code while explaining** - Show line numbers
3. **Run tests successfully** - Practice beforehand
4. **Explain WHY, not just WHAT** - Security reasoning matters
5. **If stuck, say:** "Let me show you in the code" and navigate to the relevant function

**Most Important:** Know these 3 line numbers by heart:
- `password_manager.py` Line 38: Hashing happens here
- `file_encryptor.py` Line 21: Encryption happens here  
- `rbac_system.py` Line 51: Permission check happens here

---

## 🎓 GOOD LUCK!
You've got this! The code works, you understand it, now just show it confidently.
