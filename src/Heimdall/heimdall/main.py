import asyncio, json, datetime

from . import base

from . import configparser


class MainClass:
    """Sets stage ready for Heimdall"""

    def __init__(self) -> None:
        """Inits the class ready for looping"""
        self.config = self.set_configuration()
        print(json.dumps(self.config, indent=4))

    def timestamp(self) -> str:
        """Returns timestamp for Scanner"""
        return datetime.datetime.now().isoformat(sep="T", timespec="seconds")

    def set_configuration(self):
        set = configparser.ConfigManager()
        set.set_config()
        config = set.get_config()
        return config

    async def main(self):
        """Main loop for Heimdall"""
        timestamp = self.timestamp()
        portscan = asyncio.create_task(base.scanner(self.config, timestamp))
        await portscan


if __name__ == "__main__":
    try:
        asyncio.run(MainClass().main())
    except KeyboardInterrupt:
        print("\nExiting scanner...\nGoodbye!\n")
