"""Utility methods for Heimdall"""

from pathlib import Path
import csv

from Heimdall.heimdall.logger_config import Logger


logger = Logger(__name__)


def return_path(relpath: str) -> str:
    """Path helper, to give full path.
    Helps to call the function or package
    from anywhere."""
    return Path(__file__).parent / relpath


def parse_results(results: dict, timestamp) -> list:
    """Returns parsed dictionary for ELK handle"""
    elkList = []
    for host, ports in results.items():
        for port, data in ports.items():
            elkJson = {}
            elkJson["timestamp"] = timestamp
            elkJson["ip"] = host
            elkJson["port"] = port
            elkJson["name"] = data["name"]
            elkJson["product"] = data["product"]
            elkJson["version"] = data["version"]
            elkJson["extrainfo"] = data["extrainfo"]
            elkJson["banner"] = data.get("script", {}).get("banner", "")
            elkList.append(elkJson)
    return elkList


def save_metadata(results: dict, config: dict, timestamp: str) -> None:
    """Saves metadata to a file for diplaying in frontend"""
    resultspath = return_path("../results/results_meta.txt")
    data = {}
    vulns = []
    devices = []
    ports = []
    start = str(config["ports"]["start"])
    end = str(config["ports"]["end"])
    range = f"{start} - {end}"
    for entry in results:
        devices.append(entry["ip"])
        if entry["CVE"]:
            vulns.append(entry["CVE"])
        ports.append(entry["port"])
    devices_uniq = len(set(devices))
    vulns_uniq = len(set(vulns))
    devices_uniq = len(set(devices))
    devices_uniq = len(set(devices))
    try:
        with open(resultspath, "r") as resultfile:
            # Check if file exists
            pass
        with open(resultspath, "a") as resultfile:
            fields = ["devices", "portsopen", "vulnamount", "timestamp", "rangeports"]
            writer = csv.DictWriter(resultfile, fieldnames=fields)
            writer.writerow(
                {
                    "devices": devices_uniq,
                    "portsopen": len(ports),
                    "vulnamount": vulns_uniq,
                    "timestamp": timestamp,
                    "rangeports": range,
                }
            )
    except FileNotFoundError:

        logger.info("Created new meta file for results")

        with open(resultspath, "w") as result:
            fields = ["devices", "portsopen", "vulnamount", "timestamp", "rangeports"]
            writer = csv.DictWriter(result, fieldnames=fields)
            writer.writeheader()
            writer.writerow(
                {
                    "devices": devices_uniq,
                    "portsopen": len(ports),
                    "vulnamount": vulns_uniq,
                    "timestamp": timestamp,
                    "rangeports": range,
                }
            )


class ContentCallback:
    def __init__(self):
        self.contents = ""

    def content_callback(self, buf):
        self.contents = self.contents + str(buf)
