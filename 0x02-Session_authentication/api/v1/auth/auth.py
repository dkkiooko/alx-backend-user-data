#!/usr/bin/env python3
""" manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ class manages API authentication """
    def __init__(self):
        """ initialize Auth """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ find whether path is authorized """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ find header based on Flask request object """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ find the current user """
        if request:
            return request
        return None
