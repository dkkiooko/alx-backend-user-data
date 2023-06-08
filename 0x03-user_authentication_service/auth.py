#!/usr/bin/env python3
"""hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
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

    def create_session(self, email: str) -> str:
        """take email and return a session ID

        Args:
            email (str): _email of the user_

        Returns:
            str: _session ID of user_
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                session_id = _generate_uuid()
                user.session_id = session_id
                return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """takes session id and returns a user or None if no user found """
        if session_id is None:
            return None
        try:
            session_id = self._db.find_user_by(session_id=session_id)
            return session_id
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ gets user and destroys current session by deleting session ID"""
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ generates reset password token """
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        reset_token = _generate_uuid()
        user.reset_token = reset_token
        return reset_token
