#!/usr/bin/env python3
""" expiration in authentication sessions
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """inherits from SessionAuth

    Args:
        SessionAuth (_Auth_): _class for session authorization_
    """
    def __init__(self):
        """initialize by overloading
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session id for user id

        Args:
            user_id (_str_, optional): _id_. Defaults to None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """overload previous method

        Args:
            session_id (_str_, optional): _session id_. Defaults to None.
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if self.session_duration <= 0:
            return user_details.get('user_id')
        if 'created_at' not in user_details.keys():
            return None
        created_at = user_details.get('created_at')
        window = created_at + timedelta(seconds=self.session_duration)
        if window < datetime.now():
            return None
        return user_details.get("user_id")
