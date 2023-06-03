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
    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not found_users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 404
    found_user = found_users[0]

    from api.v1.app import auth
    session_id = auth.create_session(found_user.id)
    SESSION_COOKIE = getenv('SESSION_NAME')

    response = jsonify(found_user.to_json())
    response.set_cookie(SESSION_COOKIE, session_id)
    return response