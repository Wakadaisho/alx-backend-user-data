#!/usr/bin/env python3
"""
SessionDB Authentication module
dependant on SessionExpAuth module
"""

from .session_exp_auth import SessionExpAuth
from datetime import datetime
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """SessionDB Authentication class
    """
    def create_session(self, user_id: str = None) -> str:
        """Create a timed session id for a user
        """
        id = super().create_session(user_id)
        UserSession(user_id=user_id, session_id=id).save()
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if not isinstance(session_id, str):
            return None
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None or len(user_session) == 0:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        if user_session[0].created_at is None:
            return None
        session_duration = (datetime.utcnow() -
                            user_session[0].created_at).total_seconds()
        if session_duration > self.session_duration:
            return None
        return user_session[0].user_id
    
    def destroy_session(self, request=None) -> bool:
        """Logs out user / deletes user session
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_session = UserSession.search({'session_id': session_cookie})
        if user_session is None or len(user_session) == 0:
            return False
        user_session[0].remove()
        return True
