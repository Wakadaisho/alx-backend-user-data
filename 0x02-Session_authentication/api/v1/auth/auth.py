#!/usr/bin/env python3
"""
Authentication module for the API
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Wrapper that marks a path
        as requiring authentication"""
        from re import match
        if path is None or len(excluded_paths or []) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        checked_paths = []

        for i in excluded_paths:
            if i.endswith('*'):
                checked_paths.append(i[:-1])
            else:
                checked_paths.append(i)

        for i in checked_paths:
            if path.startswith(i):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Extract auth header from request object
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from request object
        """
        return None

    def session_cookie(self, request=None):
        """Get the session cookie
        """
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        cookie = request.cookies.get(cookie_name)
        return cookie
