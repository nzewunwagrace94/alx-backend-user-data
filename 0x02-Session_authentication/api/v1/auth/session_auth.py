#!/usr/bin/env python3
"""
Create a class SessionAuth that inherits from Auth. For the moment
this class will be empty. It's the first step for creating a new
 authentication mechanism:

validate if everything inherits correctly without any overloading
validate the “switch” by using environment variables
Update api/v1/app.py for using SessionAuth instance for the variable
 auth depending of the value of the environment variable AUTH_TYPE,
   If AUTH_TYPE is equal to session_auth:

import SessionAuth from api.v1.auth.session_auth
create an instance of SessionAuth and assign it to the variable auth
Otherwise, keep the previous mechanism.
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth that inherits from Auth. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id: """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID: """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            user = User.get(user_id)
            return user
        return None

    def destroy_session(self, request=None):
        """ delete session """
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
