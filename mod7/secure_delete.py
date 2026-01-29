import os
import random
import string
import datetime

def log_action(message):
    """Saves the action to a log file for audit trail."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry) # Print to screen so we see it happening
    with open("deletion_audit.log", "a") as log_file:
        log_file.write(log_entry + "\n")

def secure_delete(filepath, passes=3):
    """
    Overwrites the file with random data multiple times before deleting.
    This prevents recovery tools from reading the original data.
    """
    
    # 1. Check if file exists (Validation)
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    # Get file size to know how much to overwrite
    file_size = os.path.getsize(filepath)
    log_action(f"START: Secure deletion for '{filepath}' ({file_size} bytes)")

    try:
        with open(filepath, "rb+") as f:
            # 2. Overwrite Logic (Security Practice)
            for i in range(passes):
                # Move pointer to the beginning of the file
                f.seek(0)
                
                # Generate random trash data
                random_data = os.urandom(file_size)
                
                # Write the trash data over the file
                f.write(random_data)
                f.flush() # Force write to disk
                
                log_action(f"PASS {i+1}/{passes}: Overwritten with random data.")
                
        # 3. Final Delete (Disposal)
        os.remove(filepath)
        log_action(f"SUCCESS: File '{filepath}' has been permanently deleted.")
        
    except Exception as e:
        log_action(f"FAILURE: Could not delete '{filepath}'. Error: {e}")

# This part runs when you start the script
if __name__ == "__main__":
    # Create a dummy file for testing if it doesn't exist
    target_file = "confidential_data.txt"
    if not os.path.exists(target_file):
        with open(target_file, "w") as f:
            f.write("This is a secret message that needs to be destroyed.")
        print(f"Created dummy file: {target_file}")

    # Ask user for confirmation
    print("-" * 40)
    print(f"Target File: {target_file}")
    print("-" * 40)
    
    confirm = input("Are you sure you want to securely delete this file? (yes/no): ")
    
    if confirm.lower() == "yes":
        secure_delete(target_file)
    else:
        print("Operation cancelled.")
