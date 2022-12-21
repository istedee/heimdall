import json
import csv
from flask import Response
from flask_restful import Resource
from pathlib import Path


class ScannerHistory(Resource):
    """Set scanner config"""

    def return_path(self, relpath: str) -> str:
        """Path helper, to give full path.
        Helps to call the function or package
        from anywhere."""
        return Path(__file__).parent / relpath

    def get(self):
        """Return config for Scanner"""

        self.confPath = self.return_path("../../results/results_meta.txt")
        content = []
        header = ["id"]
        info = {}
        try:
            with open(self.confPath, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for headers in csv_reader:
                    for key in headers:
                        header.append(key)
                    break
                content = csv_file.readlines()[-100:]
                info["headers"] = header
                temp = []
                for entry in content:
                    entry = entry.strip("\n")
                    temp.append(entry)
                i = 0
                csvlist = []
                for data in temp:
                    i = i + 1
                    tempdict = {}
                    x = data.split(",")
                    print(x)
                    tempdict["id"] = str(i)
                    tempdict[header[1]] = x[0]
                    tempdict[header[2]] = x[1]
                    tempdict[header[3]] = x[2]
                    tempdict[header[4]] = x[3]
                    tempdict[header[5]] = x[4]
                    csvlist.append(tempdict)
                info["runs"] = csvlist

            print(info)
            return Response(
                status=200,
                response=json.dumps(info),
            )
        except FileNotFoundError:
            return Response(
                status=200,
                response=json.dumps(info),
            )
