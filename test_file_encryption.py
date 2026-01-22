# file_encryptor.py - STUDENT TO COMPLETE
import os
import hashlib
from base64 import b64encode, b64decode


class FileEncryptor:
    def __init__(self, key):
        """
        Initialize with encryption key
        key: String password (will be hashed to 32 bytes)
        """
        # Convert key string to 32-byte key using SHA-256
        self.key = hashlib.sha256(key.encode("utf-8")).digest()

    def _xor_encrypt(self, data, key):
        """Simple XOR encryption (for learning purposes)"""
        # For each byte in data, XOR with key byte (cycle through key)
        encrypted = bytearray()
        key_len = len(key)
        for i, b in enumerate(data):
            encrypted.append(b ^ key[i % key_len])
        return bytes(encrypted)

    def _pad_data(self, data, block_size=16):
        """Add PKCS7 padding"""
        padding_length = block_size - (len(data) % block_size)
        if padding_length == 0:
            padding_length = block_size
        padding = bytes([padding_length]) * padding_length
        return data + padding

    def _unpad_data(self, data):
        """Remove PKCS7 padding"""
        if not data:
            raise ValueError("No data to unpad")
        padding_length = data[-1]
        if padding_length <= 0 or padding_length > len(data):
            raise ValueError("Invalid padding length")
        if data[-padding_length:] != bytes([padding_length]) * padding_length:
            raise ValueError("Invalid PKCS7 padding")
        return data[:-padding_length]

    def encrypt_file(self, input_path, output_path):
        """Encrypt a file"""
        try:
            # 1. Read input file
            with open(input_path, "rb") as f:
                plaintext = f.read()

            # 2. Pad data to multiple of block size
            padded = self._pad_data(plaintext, block_size=16)

            # 3. Encrypt using _xor_encrypt
            encrypted = self._xor_encrypt(padded, self.key)

            # 4. Write to output file
            with open(output_path, "wb") as f:
                f.write(encrypted)

            # 5. Return success status
            return True
        except Exception as e:
            print(f"Encryption error: {e}")
            return False

    def decrypt_file(self, input_path, output_path):
        """Decrypt a file"""
        try:
            # 1. Read encrypted file
            with open(input_path, "rb") as f:
                encrypted = f.read()

            # 2. Decrypt using _xor_encrypt (XOR is symmetric)
            padded = self._xor_encrypt(encrypted, self.key)

            # 3. Remove padding using _unpad_data
            plaintext = self._unpad_data(padded)

            # 4. Write to output file
            with open(output_path, "wb") as f:
                f.write(plaintext)

            # 5. Return success status
            return True
        except Exception as e:
            print(f"Decryption error: {e}")
            return False

    def create_test_file(self, content, filename):
        """Create a test file with given content"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    