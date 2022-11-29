import nmap
import json
from .utils import return_path, ContentCallback, parse_results
import pycurl
from bs4 import BeautifulSoup
from googlesearch import search
import asyncio


async def scanner(config: dict, timestamp: str) -> None:
    """Scanner base logic"""
    if config["port_scan"] == False:
        print("Portscan not enabled")
        await asyncio.sleep(10)
        return
    print("Starting port scan...")
    results = {}
    nm = nmap.PortScanner()
    scanRange = config["ip_space"] + "/" + config["subnet"]

    nm.scan(hosts=scanRange, arguments="-A -script=banner ")
    for host in nm.all_hosts():
        if "tcp" in nm[host].keys():
            results[host] = nm[host]["tcp"]
        elif "udp" in nm[host].keys():
            results[host] = nm[host]["udp"]

    confPath = return_path("../results/results.json")
    try:
        with open(confPath, "w") as outfile:
            json.dump(results, outfile, indent=4)
    except FileNotFoundError:
        print("Results folder not found!")
        print("Cannot save results to a file")
    print("Port scan done!\n")

    #############################################
    # Here comes the ELK handle for the parsed
    parsedELK = parse_results(results, timestamp)
    # insert function here
    #############################################

    check_vulnerable_services(config, results, timestamp)
    await asyncio.sleep(120)


def check_vulnerable_services(config: dict, scanresults: dict, timestamp: str) -> None:
    if config["vuln_discovery"] == False:
        print("Vulnerability discovery is not enabled")
        return
    print("Starting vulnerability scan\n")
    servicelist = []
    port = 0
    count = 0
    data = scanresults

    for host, ports in scanresults.items():
        for port, data in ports.items():
            try:
                if data["version"]:
                    banner_and_port_combination = (
                        data["script"]["banner"] + ";" + str(port)
                    )
                    servicelist.append(banner_and_port_combination)
            except KeyError:
                pass

    vulPath = return_path("../files/vulfile.txt")
    with open(vulPath, "r") as file:
        data = file.read()
        vulns = {}
        for i in range(len(servicelist)):
            servicelist[i].split(";")
            servicelist[i].split(",")[:-1]
            parsed_service = ",".join(servicelist[i].split(",")[:-1])
            if parsed_service in data:
                count += 1
                service = servicelist[i].split(";")
                vulns[service[0]] = service[1]
            if count == 0:
                print("No vulnerabilities found.")
        for key, data in vulns.items():
            print(f"\n[!] Vulnerability found: {key} at port {data}")

    def exploitdb_search(name):

        if len(name) != 0:
            try:
                query = str(name) + " " + "site:https://www.exploit-db.com"
                for data in search(query, tld="com", num=20, start=0, stop=25, pause=2):
                    if "https://www.exploit-db.com/exploits" in data:
                        t = ContentCallback()
                        curlObj = pycurl.Curl()
                        curlObj.setopt(curlObj.URL, "{}".format(data))
                        curlObj.setopt(curlObj.WRITEFUNCTION, t.content_callback)
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
                        author = soup.find("meta", property="article:author")
                        print(("CVE:" + " " + cve if cve else "No cve id found"))
                        print(
                            (
                                "Author:" + " " + author["content"]
                                if author
                                else "No author name found"
                            )
                        )
                        publish = soup.find("meta", property="article:published_time")
                        print(
                            (
                                "Publish Date:" + " " + publish["content"]
                                if publish
                                else "Cannot find the published date"
                            )
                        )
                        print()

            except Exception as e:
                print("Connection Error!")
                print(e)
