import nmap
import asyncio
import ipaddress
import json


async def scanner():
    results = {}
    nm = nmap.PortScanner()
    for ip in ipaddress.IPv4Network("192.168.1.0/24"):
        ip = str(ip)
        nm.scan(hosts=ip, arguments="-sS -sC -O -sV")
        print(f"scanning host: {ip}")
        for host in nm.all_hosts():
            if "tcp" in nm[ip].keys():
                results[ip] = nm[ip]["tcp"]
            elif "udp" in nm[ip].keys():
                results[ip] = nm[ip]["udp"]

    with open("results.json", "w") as outfile:
        json.dump(results, outfile, indent=4)


async def main():
    await asyncio.gather(
        scanner(),
    )


if __name__ == "__main__":
    asyncio.run(main())
