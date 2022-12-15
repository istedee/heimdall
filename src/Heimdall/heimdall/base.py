import datetime
import os
import nmap
import json
import pycurl
import asyncio
import functools
from .utils import return_path, ContentCallback, parse_results
from . import configparser
from bs4 import BeautifulSoup
from googlesearch import search
from elasticsearch import Elasticsearch
import warnings
from Heimdall.heimdall.logger_config import Logger


logger = Logger(__name__)


def index(data, address):
    """Index data into elasticsearch"""
    warnings.filterwarnings("ignore", module="elasticsearch")
    client = Elasticsearch(address, max_retries=3)
    for dictionary in data:
        # index the dictionary with Elasticsearch
        client.index(index="heimdall-data-index", doc_type="_doc", body=dictionary)
    logger.info("Indexed %s documents.", len(data))


def get_timestamp() -> str:
    """Returns timestamp for Scanner"""
    return datetime.datetime.utcnow().isoformat(sep="T", timespec="seconds")


async def scanner(config: dict) -> None:
    while True:
        # Check config changes
        if not configparser.ConfigManager().check_configuration(config):
            logger.info("Configuration has changed. Applying the changes.")
            configuration = configparser.ConfigManager()
            configuration.set_config()
            config = configuration.get_config()
            logger.info("Changes made succesfully.")
        """Scanner base logic"""
        if not config["CONFIG"]["port_scan"]:
            logger.info("Portscan not enabled")
            await asyncio.sleep(10)
            return
        sleeptime = config["CONFIG"]["sleeptime"]
        timestamp = get_timestamp()
        logger.info("Starting port scan.")

        loop = asyncio.get_event_loop()
        results = {}
        nm = nmap.PortScanner()
        scanRange = config["CONFIG"]["ip_space"] + "/" + config["CONFIG"]["subnet"]

        start = config["CONFIG"]["ports"]["start"]
        end = config["CONFIG"]["ports"]["end"]

        ports_to_scan = str(start) + "-" + str(end)

        argumentstring = f"-A -script=banner -p {ports_to_scan} --open"

        await loop.run_in_executor(
            None,
            functools.partial(nm.scan, hosts=scanRange, arguments=argumentstring),
        )
        for host in nm.all_hosts():
            if "tcp" in nm[host].keys():
                results[host] = nm[host]["tcp"]
            elif "udp" in nm[host].keys():
                results[host] = nm[host]["udp"]

        results = parse_results(results, timestamp)
        confPath = return_path("../results/results.json")
        changed = False
        # Change comparison does not work at the moment
        # Since there are timestamps, which naturally change
        # During every run. Comparison JSON could be constructed
        # For this purpose to see if the network has changed
        try:
            with open(confPath, "r") as outfile:
                oldres = json.load(outfile)
                if oldres == results:
                    logger.info(
                        "The scan results have not changed. Skipping rest of cycle"
                    )
                else:
                    with open(confPath, "w") as outfile:
                        json.dump(results, outfile, indent=4)
                        changed = True
        except FileNotFoundError:
            logger.info("Results folder not found!")
            logger.info("Creating results directory for storing findings")
            os.mkdir(return_path("../") / "results")
            logger.info("Directory created succesfully!\n")
            logger.info("Storing the findings to the results folder")
            with open(confPath, "w") as outfile:
                json.dump(results, outfile, indent=4)
                changed = True
        if changed:
            logger.info("Port scan done!")

            vulns = await check_vulnerable_services(config, results)

            logger.info("Parsed JSON: %s", json.dumps(vulns))
            index(results, config["CONFIG"]["elastic_address"])
            logger.info("indexing done")

        logger.info(f"Waiting {sleeptime} seconds before next scan.")
        await asyncio.sleep(sleeptime)


async def check_vulnerable_services(config: dict, scanresults: list) -> dict:
    if not config["CONFIG"]["vuln_discovery"]:
        logger.info("Vulnerability discovery is not enabled")
        return scanresults

    logger.info("Starting vulnerability scan")
    checked_banners = {}

    for entry in scanresults:
        try:
            if not entry["banner"]:
                entry["CVE"] = {}
                continue
            if entry["banner"] not in checked_banners:
                vuln = await exploitdb_search(entry["banner"])
                checked_banners[entry["banner"]] = vuln
            else:
                vuln = checked_banners[entry["banner"]]
            entry["CVE"] = vuln or {}
        except KeyError:
            pass
    return scanresults


async def exploitdb_search(name: str) -> dict:
    exploit_dict = {}
    logger.info("Starting ExploitDb lookup...")

    if len(name) != 0:
        try:
            query = str(name) + " " + "site:https://www.exploit-db.com"
            for data in search(query, tld="com", num=20, start=0):
                if "https://www.exploit-db.com/exploits" in data:
                    t = ContentCallback()
                    curlObj = pycurl.Curl()
                    curlObj.setopt(curlObj.URL, "{}".format(data))
                    curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
                    curlObj.setopt(pycurl.TIMEOUT, 10)
                    curlObj.perform()
                    curlObj.close()
                    print(("Url:" + " " + data))
                    soup = BeautifulSoup(t.contents, "lxml")
                    desc = soup.find("meta", property="og:title")
                    keywords = soup.find("meta", attrs={"name": "keywords"})
                    print(keywords["content"])
                    tmp = keywords["content"].split(",")
                    try:
                        cve = tmp[2]
                    except IndexError:
                        cve = None

                    print(
                        (
                            "Title:" + " " + desc["content"]
                            if desc
                            else "Cannot find the description for the exploit"
                        )
                    )
                    print(("CVE:" + " " + cve if cve else "No cve id found"))
                    publish = soup.find("meta", property="article:published_time")
                    print(
                        (
                            "Publish Date:" + " " + publish["content"]
                            if publish
                            else "Cannot find the published date"
                        )
                    )
                    # create dict
                    exploit_dict["service"] = str(name)
                    exploit_dict["cve"] = str(cve)
                    exploit_dict["url"] = str(data)
                    exploit_dict["date"] = str(publish["content"])
                    exploit_dict["desc"] = str(desc["content"])
                    return exploit_dict
        except Exception as e:
            logger.error("Connection Error!")
            logger.error(e)
    return exploit_dict
