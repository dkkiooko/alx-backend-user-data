#!/usr/bin/env python3
"""hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes a password

    Args:
        password (str): user password

    Returns:
        bytes: _hashed password_
    """
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt)
