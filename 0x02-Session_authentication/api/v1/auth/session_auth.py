#!/usr/bin/env python3
"""
Session Authentication module
dependant on Auth module
"""

from .auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for a user
        """
        if not isinstance(user_id, str):
            return None
        id = str(uuid.uuid4())
        self.user_id_by_session_id.update({id: user_id})
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns User instance based on cookie value
        """
        session = self.session_cookie(request)
        userId = self.user_id_by_session_id.get(session)
        user = User.get(userId)
        return user

    def destroy_session(self, request=None) -> bool:
        """Logs out user / deletes user session
        """
        session_cookie = self.session_cookie(request)
        userId = self.user_id_by_session_id.get(session_cookie)
        if userId is None:
            return False
        del self.user_id_by_session_id[session_cookie]

        return True
