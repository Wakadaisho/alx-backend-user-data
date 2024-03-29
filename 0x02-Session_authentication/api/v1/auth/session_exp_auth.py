#!/usr/bin/env python3
"""
SessionExp Authentication module
dependant on SessionAuth module
"""

from .session_auth import SessionAuth
from datetime import datetime
import os


class SessionExpAuth(SessionAuth):
    """Session Expiry Authentication class
    """
    def __init__(self) -> None:
        """Initialization of timed session"""
        super().__init__()
        try:
            duration = os.getenv("SESSION_DURATION", 0)
            duration = int(duration)
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id: str = None) -> str:
        """Create a timed session id for a user
        """
        id = super().create_session(user_id)
        if id is None:
            return None
        self.user_id_by_session_id.update({id: {'user_id': user_id,
                                                'created_at': datetime.utcnow()
                                                }})
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if not isinstance(session_id, str):
            return None
        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None
        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if 'created_at' not in session_dict:
            return None

        session_duration = (datetime.utcnow() - created_at).total_seconds()
        if session_duration > self.session_duration:
            return None

        return user_id
