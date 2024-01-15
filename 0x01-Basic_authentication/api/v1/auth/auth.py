#!/usr/bin/env python3
"""
Authentication module for the API
"""

from flask import request
from typing import List, TypeVar


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
        return path not in excluded_paths
        # excluded_paths = [path[:-1]+".+"
        #                   if path.endswith('*') else path
        #                   for path in excluded_paths]
        # print("excluded")/
        # return path not in excluded_paths
        # return not all([match(i, path) for i in excluded_paths])

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
