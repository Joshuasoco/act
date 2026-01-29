import os
import time
import unittest
from secure_delete import secure_delete, log_action

class TestSecureDelete(unittest.TestCase):

    def setUp(self):
        """Setup a dummy file before each test."""
        self.test_file = "test_secret.txt"
        self.log_file = "deletion_audit.log"
        
        with open(self.test_file, "w") as f:
            f.write("Super secret data for testing.")
            
    def tearDown(self):
        """Clean up if something failed."""
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except:
                pass

    def test_file_deletion_success(self):
        """Test if the file is actually deleted."""
        self.assertTrue(os.path.exists(self.test_file), "Test file should exist before deletion")
        
        secure_delete(self.test_file, passes=1)
        
        self.assertFalse(os.path.exists(self.test_file), "Test file should be gone after secure_delete")

    def test_audit_log_entry(self):
        """Test if the action is logged."""
        # Clear log or define a marker
        marker = f"TEST_MARKER_{int(time.time())}"
        log_action(marker)
        
        secure_delete(self.test_file, passes=1)
        
        # Read the log file
        with open(self.log_file, "r") as f:
            content = f.read()
            
        self.assertIn("SUCCESS: File 'test_secret.txt' has been permanently deleted.", content)

if __name__ == '__main__':
    unittest.main()
