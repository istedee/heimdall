import json
from flask import Response, jsonify
from flask_restful import Resource


class GetPing(Resource):
    """Sanity check for API"""

    def get(self):

        return Response(
            status=200,
            response=json.dumps("pong"),
        )
