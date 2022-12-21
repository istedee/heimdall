import configparser
import json
from flask import Response, request
from flask_restful import Resource
from pathlib import Path


class ScannerConfig(Resource):
    """Set scanner config"""

    def return_path(self, relpath: str) -> str:
        """Path helper, to give full path.
        Helps to call the function or package
        from anywhere."""
        return Path(__file__).parent / relpath

    def get(self):
        """Return config for Scanner"""

        parser = configparser.ConfigParser()
        self.confPath = self.return_path("../../config/config.ini")
        parser.read(self.confPath)
        parser.sections()
        config_keys = {key: value.lower() for key, value in parser["CONFIG"].items()}
        return Response(
            status=200,
            response=json.dumps(config_keys),
        )

    def post(self):
        """Set config for Scanner"""

        parser = configparser.ConfigParser()
        self.confPath = self.return_path("../../config/config.ini")
        parser.read(self.confPath)
        for key, value in request.json.items():
            parser.set("CONFIG", key, str(value))
        with open(self.confPath, "w") as configfile:
            parser.write(configfile)
        return Response(
            status=200,
            response=json.dumps("OK"),
        )
