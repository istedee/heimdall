"""
Init file for starting the application
"""

import json
import os
from flask import Flask, Response
from flask_cors import CORS


# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy
def create_app(test_config=None):
    """
    Starts the app
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    app.debug = True

    if test_config is None:
        app.config.from_pyfile("./config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app, resources={r"/*": {"origins": "*"}})

    from . import api

    app.register_blueprint(api.API_BP)

    @app.route("/api/")
    def view():
        """Return api entrypoint."""
        return Response(
            status=200,
            response=json.dumps("API is running!"),
        )

    return app
