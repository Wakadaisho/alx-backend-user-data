#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login_user() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - Log in a user and create a session token
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}, 400)

    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}, 400)

    user = User.search({'email': email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}, 404)

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}, 401)

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)

    resp = jsonify(user[0].to_json())
    resp.set_cookie(os.getenv("SESSION_NAME"), session_id)
    return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def session_logout_user() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - Log out a user and delete a session token
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({})
