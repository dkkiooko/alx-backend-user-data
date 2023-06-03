#!/usr/bin/env python3
""" view for session authentication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """route for /api/v1/auth_session/login
    captures all credentials for session authentication
    """
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    found_users = User.search({"email": email})
    if not found_users or found_users == []:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """route for /api/v1/auth_session/logout
    destroys cookie session and logs out
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if destroyed is False:
        abort(404)
    return jsonify({}), 200
