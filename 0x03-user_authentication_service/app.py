#!/usr/bin/env python3
"""basic Flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """ simple app returns JSON payload """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """ endpoint to register a new user """
    # get email and pwd form data
    email, password = request.form.get("email"), request.form.get("password")
    try:
        # register
        AUTH.register_user(email, password)
        # respond with json
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ request has form data email and password
    creates a new session and stores session ID as a cookie
    and returns a JSON payload of the form """
    email, password = request.form.get("email"), request.form.get("password")
    # find user
    valid = AUTH.valid_login(email=email, password=password)
    if not valid:
        abort(401)
    else:
        session = AUTH.create_session(email=email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session)
        return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
