#!/usr/bin/env python3
"""Route module for the API
"""
from flask import Flask, jsonify
from flask_cors import (CORS, cross_origin)
from auth import Auth


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
