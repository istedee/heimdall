import datetime
import os
import nmap, json, pycurl, asyncio, functools
from .utils import return_path, ContentCallback, parse_results
from . import configparser
from bs4 import BeautifulSoup
from googlesearch import search


def get_timestamp() -> str:
    """Returns timestamp for Scanner"""
    return datetime.datetime.now().isoformat(sep="T", timespec="seconds")


async def scanner(config: dict) -> None:
    while True:
        # Check config changes
        if configparser.ConfigManager().check_configuration(config) == False:
            print("Configuration has changed.\n")
            print("Applying the changes...")
            configuration = configparser.ConfigManager()
            configuration.set_config()
            config = configuration.get_config()
            print("Changes made succesfully.\n")
        """Scanner base logic"""
        if config["CONFIG"]["port_scan"] == False:
            print("Portscan not enabled")
            await asyncio.sleep(10)
            return
        sleeptime = config["CONFIG"]["sleeptime"]
        timestamp = get_timestamp()
        print("Starting port scan...")

        loop = asyncio.get_event_loop()
        results = {}
        nm = nmap.PortScanner()
        scanRange = config["CONFIG"]["ip_space"] + "/" + config["CONFIG"]["subnet"]

        await loop.run_in_executor(
            None,
            functools.partial(nm.scan, hosts=scanRange, arguments="-A -script=banner "),
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
                    print("The scan results have not changed. Skipping rest of cycle")
                else:
                    with open(confPath, "w") as outfile:
                        json.dump(results, outfile, indent=4)
                        changed = True
        except FileNotFoundError:
            print("Results folder not found!")
            print("Creating results directory for storing findings")
            os.mkdir(return_path("../") / "results")
            print("Directory created succesfully!\n")
            print("Storing the findings to the results folder")
            with open(confPath, "w") as outfile:
                json.dump(results, outfile, indent=4)
                changed = True
        if changed == True:
            print("Port scan done!\n")

            vulns = await check_vulnerable_services(config, results)
            # for entry in vulns:
            #     print(entry)
            print()
            #############################################
            # Here comes the ELK handle for the parsed with
            results_json = json.dumps(results)
            # insert function here
            #############################################

        print(f"Waiting {sleeptime} seconds before next scan...\n")
        await asyncio.sleep(sleeptime)


async def check_vulnerable_services(config: dict, scanresults: list) -> dict:
    if config["CONFIG"]["vuln_discovery"] == False:
        print("Vulnerability discovery is not enabled")
    else:
        print("Starting vulnerability scan\n")
    checked_banners = {}
    if scanresults:  # skip check if results.json is empty
        for entry in scanresults:
            try:
                if config["CONFIG"]["vuln_discovery"] == True:
                    if entry["banner"]:
                        if entry["banner"] not in checked_banners:
                            vuln = await exploitdb_search(entry["banner"])
                            checked_banners[entry["banner"]] = vuln
                        else:
                            vuln = checked_banners[entry["banner"]]
                        if vuln:
                            entry["CVE"] = vuln
                        else:
                            entry["CVE"] = ""
                    else:
                        entry["CVE"] = ""
                else:
                    entry["CVE"] = ""
            except KeyError:
                pass
    return scanresults


async def exploitdb_search(name: str) -> dict:
    exploit_dict = {}
    print("Starting ExploitDb lookup...")

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
                    print()
                    # create dict
                    exploit_dict["service"] = str(name)
                    exploit_dict["cve"] = str(cve)
                    exploit_dict["url"] = str(data)
                    exploit_dict["date"] = str(publish["content"])
                    exploit_dict["desc"] = str(desc["content"])
                    return exploit_dict
        except Exception as e:
            print("Connection Error!")
            print(e)
    return exploit_dict
