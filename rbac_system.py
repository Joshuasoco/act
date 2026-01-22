# rbac_system.py - STUDENT TO COMPLETE
import json


class RBACSystem:
    def __init__(self, policy_file='rbac_policy.json'):
        self.policy_file = policy_file
        self.roles = self._load_roles()
        self.users = {}

    def _load_roles(self):
        """Load roles and permissions from policy file"""
        # Default roles if file doesn't exist
        default_roles = {
            'guest': ['read_public'],
            'user': ['read_public', 'write_own', 'read_own'],
            'editor': ['read_public', 'write_own', 'read_own', 'edit_public'],
            'admin': [
                'read_public', 'write_own', 'read_own',
                'edit_public', 'delete_any', 'manage_users'
            ]
        }

        # Try to load from file, use defaults if file not found or invalid
        try:
            with open(self.policy_file, 'r') as f:
                data = json.load(f)
                # Expecting a dict like default_roles
                if isinstance(data, dict):
                    return data
                else:
                    return default_roles
        except (FileNotFoundError, json.JSONDecodeError):
            return default_roles

    def add_user(self, user_id, role='user'):
        """Add a user with specified role"""
        # Validate role exists
        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}")

        # Add user to users dictionary
        self.users[user_id] = role

    def check_permission(self, user_id, permission):
        """Check if user has specific permission"""
        # Find user's role
        role = self.users.get(user_id)
        if role is None:
            return False

        # Check if permission exists in role's permissions
        permissions = self.roles.get(role, [])
        return permission in permissions

    def can_access_file(self, user_id, filename, action='read'):
        """Check if user can perform action on file"""
        # Define file types and required permissions
        file_permissions = {
            'public.txt': {'read': 'read_public', 'write': 'edit_public'},
            f'{user_id}_private.txt': {'read': 'read_own', 'write': 'write_own'},
            'admin_logs.txt': {'read': 'delete_any', 'write': 'manage_users'}
        }

        # Determine required permission for this file/action
        perms_for_file = file_permissions.get(filename)
        if not perms_for_file:
            # Unknown file -> deny by default
            return False

        required_perm = perms_for_file.get(action)
        if not required_perm:
            return False

        # Use check_permission to verify
        return self.check_permission(user_id, required_perm)

    def list_users(self):
        """List all users and their roles"""
        # Return formatted list of users
        lines = []
        for user_id, role in self.users.items():
            lines.append(f"{user_id}: {role}")
        return "\n".join(lines)


# Sample data to test with
sample_users = [
    ('guest1', 'guest'),
    ('user1', 'user'),
    ('editor1', 'editor'),
    ('admin1', 'admin')
]
    