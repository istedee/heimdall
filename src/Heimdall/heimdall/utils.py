"""Utility methods for Heimdall"""

from pathlib import Path


def return_path(relpath: str) -> str:
    """Path helper, to give full path.
    Helps to call the function or package
    from anywhere."""
    return Path(__file__).parent / relpath


def parse_results(results: dict, timestamp) -> list:
    """Returns parsed dictionary for ELK handle"""
    elkList = []
    for host, ports in results.items():
        print(host)
        for port, data in ports.items():
            print(port)
            elkJson = {}
            elkJson["timestamp"] = timestamp
            elkJson["ip"] = host
            elkJson["port"] = port
            elkJson["name"] = data["name"]
            elkJson["product"] = data["product"]
            elkJson["version"] = data["version"]
            elkList.append(elkJson)
    return elkList


class ContentCallback:
    def __init__(self):
        self.contents = ""

    def content_callback(self, buf):
        self.contents = self.contents + str(buf)
