#!/usr/bin/env python3
"""basic Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logout function to respond to DELETE /sessions route
    """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=cookie)
    if user:
        AUTH.destroy_session(user_id=user)
        return redirect('/')
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """finds the user and returns a payload """
    session_cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_cookie)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ generates a reset password token when requested """
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ updates a password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
