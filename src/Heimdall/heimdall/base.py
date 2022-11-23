import nmap
import ipaddress
import json
from .utils import return_path


async def scanner(config: dict) -> None:
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
    with open(confPath, "w") as outfile:
        json.dump(results, outfile, indent=4)


async def check_vulnerable_services(config: dict) -> None:
    servicelist = []
    port = 0
    count = 0
    confPath = return_path("../results/results.json")
    try:
        with open(confPath, "r") as outfile:
            data = json.load(outfile)

        for ip in ipaddress.IPv4Network(config["ip_space"] + "/" + config["subnet"]):
            ip = str(ip)
            for port in range(config["ports"]["start"], config["ports"]["end"]):
                try:
                    if data[ip][str(port)]["version"]:
                        banner_and_port_combination = (
                            data[ip][str(port)]["script"]["banner"] + ";" + str(port)
                        )
                        servicelist.append(banner_and_port_combination)
                except KeyError:
                    pass
    except FileNotFoundError as e:
        print("Results file not found!")
        print(e)

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
            #                print(f"[!]Vulnerability found: {service[0]} at port {service[1]}")
            if count == 0:
                print("No vulnerabilities found.")
        for key, data in vulns.items():
            print(f"\n[!] Vulnerability found: {key} at port {data}")
