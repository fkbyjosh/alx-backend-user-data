#!/usr/bin/env python3
"""
Module for password encryption using bcrypt
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a salt using bcrypt
    
    Args:
        password (str): The password string to hash
    
    Returns:
        bytes: The salted, hashed password as a byte string
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that a provided password matches the hashed password
    
    Args:
        hashed_password (bytes): The hashed password to check against
        password (str): The plain text password to validate
    
    Returns:
        bool: True if password matches the hash, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
