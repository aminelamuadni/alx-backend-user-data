#!/usr/bin/env python3
"""
A simple Flask application that returns a greeting message in JSON format.
"""
from flask import Flask, jsonify

# Initialize the Flask application
app = Flask(__name__)


# Define a route for the application
@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint which returns a JSON message.
    """
    return jsonify({"message": "Bienvenue"})


# Run the application if this file is executed as the main program
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
