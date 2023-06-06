#!/usr/bin/env python3
"""hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


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


def _generate_uuid() -> str:
    """ creates a string representation of uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register new user if user already exists raise an error
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        pwd = _hash_password(password=password)
        user = self._db.add_user(email=email, hashed_password=pwd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ method to validate user credentials """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                # use bcrypt
                pwd_bytes = password.encode('utf-8')
                hashed = user.hashed_password
                if bcrypt.checkpw(pwd_bytes, hashed):
                    return True
        except NoResultFound:
            return False
        return False
