import nmap
import asyncio
import ipaddress
import json


async def scanner():
    results = {}
    nm = nmap.PortScanner()
    for ip in ipaddress.IPv4Network("192.168.1.0/24"):
        ip = str(ip)
        nm.scan(hosts=ip, arguments="-A -script=banner ")
        print(f"scanning host: {ip}")
        for host in nm.all_hosts():
            if "tcp" in nm[ip].keys():
                results[ip] = nm[ip]["tcp"]
            elif "udp" in nm[ip].keys():
                results[ip] = nm[ip]["udp"]

        with open("results.json", "w") as outfile:
            json.dump(results, outfile, indent=4)


async def check_vulnerable_services():
    servicelist = []
    port = 0
    count = 0
    with open("results.json", "r") as outfile:
        data = json.load(outfile)

    for ip in ipaddress.IPv4Network("192.168.1.0/24"):
        ip = str(ip)
        for port in range(65535):
            try:
                if data[ip][str(port)]["version"]:
                    banner_and_port_combination = (
                        data[ip][str(port)]["script"]["banner"] + ";" + str(port)
                    )
                    servicelist.append(banner_and_port_combination)
            except KeyError:
                pass

    with open("vulfile.txt", "r") as file:
        data = file.read()

        for i in range(len(servicelist)):
            servicelist[i].split(";")
            servicelist[i].split(",")[:-1]
            parsed_service = ",".join(servicelist[i].split(",")[:-1])
            if parsed_service in data:
                count += 1
                service = servicelist[i].split(";")
                print(f"[!]Vulneribility found: {service[i]} at port {service[i+1]}")
            if count == 0:
                print("No vulnerabilities found.")


async def main():
    await asyncio.gather(scanner(), check_vulnerable_services())


if __name__ == "__main__":
    asyncio.run(main())
