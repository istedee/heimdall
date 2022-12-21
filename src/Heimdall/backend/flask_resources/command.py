import json
import subprocess
from flask import Response
from flask_restful import Resource


class GetCommand(Resource):
    """Sanity check for API"""

    def exec_command(self, command):
        """Execute command within the host terminal"""
        return subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE
        ).stdout.readlines()

    def get(self):

        self.exec_command("ps -fA | grep 'python3 -m '")
        self.exec_command("./start_scanner.sh")
        output = self.exec_command("ps -fA | grep 'python3 -m '")
        return Response(
            status=200,
            response=output,
        )
