#!/usr/bin/env python3
"""Auth module
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash password method
    """
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generate UUIDs
    """
    import uuid
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialization method
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """Method that registers a user to the database
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Method that checks if the password is valid
        """
        import bcrypt
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
