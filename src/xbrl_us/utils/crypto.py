"""
Simple encryption utilities for XBRL US credentials.
"""
import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Location to store the salt. This doesn't need to be secret but should be consistent.
_salt_path = Path.home() / ".xbrl-us-salt"


def _get_or_create_salt():
    """Get the salt from disk or create a new one if it doesn't exist."""
    if not _salt_path.exists():
        # Generate a new salt if one doesn't exist
        salt = os.urandom(16)
        with _salt_path.open("wb") as f:
            f.write(salt)
        return salt

    # Read the existing salt
    with _salt_path.open("rb") as f:
        return f.read()


def _get_key():
    """Generate a key from machine-specific information for encryption."""
    # Use a consistent salt for this machine
    salt = _get_or_create_salt()

    # Use a combination of machine-specific information as a password
    # This ensures the encryption is tied to this specific machine
    hostname = os.uname().nodename.encode()
    username = os.getlogin().encode()

    # Combine for a machine-specific password
    password = hostname + b"-" + username

    # Derive a key using PBKDF2
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())

    # Generate the key
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_text(text):
    """Encrypt a text string."""
    key = _get_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(text.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode("utf-8")


def decrypt_text(encrypted_text):
    """Decrypt an encrypted text string."""
    key = _get_key()
    f = Fernet(key)
    encrypted_data = base64.urlsafe_b64decode(encrypted_text.encode("utf-8"))
    return f.decrypt(encrypted_data).decode("utf-8")
