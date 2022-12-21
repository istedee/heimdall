import json
from flask import Response
from flask_restful import Resource
from pathlib import Path

import yaml


class GetConfig(Resource):
    """Return Elastic address from config"""

    def return_path(self, relpath: str) -> str:
        """Path helper, to give full path.
        Helps to call the function or package
        from anywhere."""
        return Path(__file__).parent / relpath

    def get(self):
        """Return address for Elastic"""
        self.confPath = self.return_path("../../config/config.yml")

        with open(self.confPath, "r") as config:
            settings = yaml.safe_load(config)
            ela_address = settings["CONFIG"]["elastic_address"]

        return Response(
            status=200,
            response=json.dumps(ela_address),
        )
