#!/usr/bin/env python3
"""
Basic Authentication module
dependant on Auth module
"""

from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Return Base64 part of the Authorization
        header for Basic Authentication
        """
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.replace('Basic ', '')

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """Decode Base64
        """
        if base64_authorization_header is None:
            return None

        try:
            dec_string = base64.b64decode(base64_authorization_header)
            return dec_string.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials from decoded Basic Auth header
        """
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return User object if valid email and password are passed
        """
        if not (isinstance(user_email, str) and isinstance(user_pwd, str)):
            return None
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        authHeader = self.authorization_header(request)
        enc_string = self.extract_base64_authorization_header(authHeader)
        dec_string = self.decode_base64_authorization_header(enc_string)
        email, password = self.extract_user_credentials(dec_string)
        user = self.user_object_from_credentials(email, password)
        return user
