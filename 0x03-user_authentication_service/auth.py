#!/usr/bin/env python3
"""Auth module
"""
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
