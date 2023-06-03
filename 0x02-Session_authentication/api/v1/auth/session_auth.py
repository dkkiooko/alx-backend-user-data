#!/usr/bin/env python3
"""session authentication mechanism
"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from api.v1.views.users import User
from uuid import uuid4


class SessionAuth(Auth):
    """ Session inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates Session ID for user_id

        Args:
            user_id (str, optional): _id_. Defaults to None.

        Returns:
            str: _ uuid Session Id_
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """get user id for session

        Args:
            session_id (str, optional): _current session id_. Defaults to None.

        Returns:
            str: _user id of current session user_
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads from Auth
        Returns: User instance based on cookie value
        """
        session_id = self.session_cookie(request)
        user_id_for_session = self.user_id_for_session_id(session_id)
        return User.get(user_id_for_session)
