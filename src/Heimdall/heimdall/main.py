import asyncio

from . import base

from . import configparser

import os


def set_configuration():
    set = configparser.ConfigManager()
    set.set_config()
    config = set.get_config()
    return config

async def check_file_changes():
    #tähän funktioon tsekkailut sille onko file muuttunu
    while True:
        print("checking file changes")
        await asyncio.sleep(20)

async def main():
    config = set_configuration()
    print(config)
    tasks = set()
    task_list = []
    loop = asyncio.get_event_loop()
    file_change_task = asyncio.create_task(check_file_changes())
    if config["CONFIG"]["port_scan"]:
        portscan = asyncio.create_task(base.scanner(config["CONFIG"]))
        if config["CONFIG"]["vuln_discovery"]:
            vulnscan = asyncio.create_task(base.check_vulnerable_services(config["CONFIG"]))
    else:
        print("\nPortScan is disabled, enable scanning to use Heimdall")
        print("This can be done from the config/config.yml file\n")
    await file_change_task
    await vulnscan
    await portscan

if __name__ == "__main__":
    asyncio.run(main())
