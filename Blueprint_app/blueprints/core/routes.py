from flask import Blueprint, jsonify

core = Blueprint('core', __name__)

@core.route('/')
def home():
    """
    API Endpoint: GET /
    Description: Health check for the API.
    """
    return jsonify({"message": "Welcome to the mediTrack API! The system is operational."}), 200