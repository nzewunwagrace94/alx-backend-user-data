#!/usr/bin/env python3
"""
In this task you will define a _hash_password method that takes in a password
string arguments and returns bytes.

The returned bytes is a salted hash of the input password, hashed with bcrypt.
hashpw.
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ hash password and return the hashed bytes"""
    salt = bcrypt.gensalt()

    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return hashed_pass


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ initialize AUth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        this handle user registration
        """
        user = self._db._session.query(User).filter_by(email=email)
        if user:
            raise ValueError(f"User {email} already exists")

        hashed = _hash_password(password)

        new_user = self._db.add_user(email, str(hashed))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if user is valid """

        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False

        return bcrypt.checkpw(password.encode(), user.hashed_password)


# if __name__ == "__main__":
#     print(_hash_password("Hello Holberton"))
