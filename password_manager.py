import hashlib
import os
import json
import secrets


class PasswordManager:
    def __init__(self, storage_file='passwords.json'):
        self.storage_file = storage_file
        self.users = self._load_users()

    def _load_users(self):
        """Load users from storage file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # No file yet -> start with empty dict
            return {}
        except json.JSONDecodeError:
            # Corrupted/empty file -> also start fresh
            return {}

    def _save_users(self):
        """Save users to storage file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password, salt=None):
        """
        Hash a password using SHA-256 with salt
        Returns: (hashed_password, salt_used)
        """
        if salt is None:
            salt = secrets.token_hex(16)  # Generate random salt

        # Combine salt + password, then hash
        combo = (salt + password).encode('utf-8')
        hashed = hashlib.sha256(combo).hexdigest()
        return hashed, salt

    def verify_password(self, password, stored_hash, salt):
        """Verify if password matches stored hash"""
        candidate_hash, _ = self.hash_password(password, salt)
        return candidate_hash == stored_hash

    def add_user(self, username, password, role='user'):
        """Add a new user with hashed password"""
        # 1. Check if username already exists
        if username in self.users:
            return False  # or raise an exception

        # 2. Hash the password with a new salt
        pwd_hash, salt = self.hash_password(password)

        # 3. Store username, hashed password, salt, and role
        self.users[username] = {
            'hash': pwd_hash,
            'salt': salt,
            'role': role
        }

        # 4. Save to file
        self._save_users()
        return True

    def authenticate(self, username, password):
        """Authenticate a user"""
        # 1. Find user by username
        user = self.users.get(username)
        if not user:
            return False, None

        # 2. Verify password
        if self.verify_password(password, user['hash'], user['salt']):
            # 3. Return (success, role)
            return True, user['role']
        else:
            return False, None

    def change_password(self, username, old_password, new_password):
        """Change user password"""
        user = self.users.get(username)
        if not user:
            return False

        # 1. Verify old password
        if not self.verify_password(old_password, user['hash'], user['salt']):
            return False

        # 2. Hash new password with new salt
        new_hash, new_salt = self.hash_password(new_password)

        # 3. Update stored credentials
        user['hash'] = new_hash
        user['salt'] = new_salt
        self._save_users()
        return True
