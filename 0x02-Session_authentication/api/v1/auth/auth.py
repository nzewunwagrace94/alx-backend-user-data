#!/usr/bin/env python3
""" Now you will create a class to manage the API authentication.
Create a folder api/v1/auth
Create an empty file api/v1/auth/__init__.py
Create the class Auth:
in the file api/v1/auth/auth.py
import request from flask
class name Auth
public method def require_auth(self, path: str, excluded_paths: List[str])
 -> bool: that returns False - path and excluded_paths will be used later,
 now, you don't need to take care of them
public method def authorization_header(self, request=None) -> str: that
returns None - request will be the Flask request object
public method def current_user(self, request=None) -> TypeVar('User'):
 that returns None - request will be the Flask request object
This class is the template for all authentication system you will implement.
"""
# from flask import request
from typing import (
    List, TypeVar
)
import os


class Auth:
    """
    This is the Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public require_auth method
            Return bool"""
        if not path:
            return True

        if path[-1] != '/':
            path += '/'

        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == '*':
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return authorization value from request header"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """return user or none"""
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request: """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(session_name)
        return cookie
