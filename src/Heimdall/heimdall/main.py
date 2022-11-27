import asyncio

from . import base

from . import configparser


def set_configuration():
    set = configparser.ConfigManager()
    set.set_config()
    config = set.get_config()
    return config


async def main():
    config = set_configuration()
    print(config)
    tasks = set()
    if config["CONFIG"]["port_scan"]:
        portscan = asyncio.create_task(base.scanner(config["CONFIG"]))
        tasks.add(portscan)
        portscan.add_done_callback(tasks.discard)
        if config["CONFIG"]["vuln_discovery"]:
            vulnscan = asyncio.create_task(
                base.check_vulnerable_services(config["CONFIG"])
            )
            tasks.add(vulnscan)
            vulnscan.add_done_callback(tasks.discard)
    else:
        print("\nPortScan is disabled, enable scanning to use Heimdall")
        print("This can be done from the config/config.yml file\n")


if __name__ == "__main__":
    asyncio.run(main())
