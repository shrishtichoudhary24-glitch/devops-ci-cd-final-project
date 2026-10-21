"""Counter routes."""
from flask import jsonify, abort
from service import app
from service.common import status

COUNTERS = {}


@app.route("/")
def index():
    """Service index"""
    app.logger.info("Request for index")
    return jsonify(name="Counter service", version="1.0"), status.HTTP_200_OK


@app.route("/health")
def health():
    """Health check"""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/counters", methods=["GET"])
def list_counters():
    """List all counters"""
    app.logger.info("Request to list all counters")
    return jsonify(COUNTERS), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Create a counter"""
    app.logger.info("Request to create counter: %s", name)
    if name in COUNTERS:
        abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")
    COUNTERS[name] = 0
    return jsonify(name=name, counter=0), status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Read a counter"""
    app.logger.info("Request to read counter: %s", name)
    if name not in COUNTERS:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    return jsonify(name=name, counter=COUNTERS[name]), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Increment a counter"""
    app.logger.info("Request to increment counter: %s", name)
    if name not in COUNTERS:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    COUNTERS[name] += 1
    return jsonify(name=name, counter=COUNTERS[name]), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Delete a counter"""
    app.logger.info("Request to delete counter: %s", name)
    COUNTERS.pop(name, None)
    return "", status.HTTP_204_NO_CONTENT
