#!/usr/bin/env python3
""" basic authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """inherits from auth"""
    def __init__(self):
        """ initialize"""
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ get basic Base64 part of Authorization header """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """returns decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            decoded = decoded64.decode('utf-8')
        except BaseException:
            return None
        return decoded

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """ returns user email and password from Base64 decoded value """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns User instance based on email and pwd """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None
        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overload Auth method current_user """
        authentication_header = self.authorization_header(request)

        if not authentication_header:
            return None

        encoded = self.extract_base64_authorization_header(
            authentication_header)

        if not encoded:
            return None

        decoded = self.decode_base64_authorization_header(encoded)

        if not decoded:
            return None

        email, password = self.extract_user_credentials(decoded)

        if not email or not password:
            return None

        user = self.user_object_from_credentials(email, password)
        return user
