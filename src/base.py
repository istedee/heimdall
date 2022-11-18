import nmap
import asyncio
import ipaddress
from datetime import datetime
import sys
import socket
import functools


async def scanner():
    scan_results = {}
    target = str(1)
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)

    loop = asyncio.get_event_loop()
    for ip in ipaddress.IPv4Network("192.168.1.0/24"):
        target = str(ip)
        scan_results[target] = []
        try:
            # will scan ports between 1 to 65,535
            for port in range(3, 81):
                s = await loop.run_in_executor(None, functools.partial(socket.socket, socket.AF_INET, socket.SOCK_STREAM))
                socket.setdefaulttimeout(1)

                # returns an error indicator
                print(f"{target} {port}")
                result = s.connect_ex((target, port))
                if result == 0:
                    scan_results[target].append(port)
                    print("Port {} is open".format(port))
                s.close()

        except KeyboardInterrupt:
            print("\n Exiting Program")
            sys.exit()
        except socket.gaierror:
            print("\n Hostname Could Not Be Resolved")
            sys.exit()
        except socket.error:
            print("\ Server not responding")
            sys.exit()
        finally:
            print(scan_results)



async def something_else():
    x=0
    while x != 3:
        print("doing things")
        await asyncio.sleep(1)
        x+=1



async def main():
    await asyncio.gather(
        scanner(),
    )



if __name__ == "__main__":
    asyncio.run(main())
