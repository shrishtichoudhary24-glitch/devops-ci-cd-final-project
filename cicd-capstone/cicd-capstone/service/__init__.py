"""Counter service package."""
import logging
from flask import Flask

app = Flask(__name__)

# pylint: disable=wrong-import-position
from service import routes  # noqa: E402,F401

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level or logging.INFO)

app.logger.info("Counter service starting")
