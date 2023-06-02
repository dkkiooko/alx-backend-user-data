#!/usr/bin/env python3
"""session authentication mechanism
"""
from api.v1.auth.auth import Auth
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
