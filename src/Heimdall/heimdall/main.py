import asyncio
import json

from . import base

from . import configparser

from Heimdall.heimdall.logger_config import Logger

logger = Logger(__name__)


class MainClass:
    """Sets stage ready for Heimdall"""

    def __init__(self) -> None:
        """Inits the class ready for looping"""
        self.config = self.set_configuration()
        logger.info(json.dumps(self.config, indent=4))

    def set_configuration(self):
        set = configparser.ConfigManager()
        set.set_config()
        config = set.get_config()
        return config

    async def main(self):
        """Main loop for Heimdall"""
        portscan = asyncio.create_task(base.scanner(self.config))
        await portscan


if __name__ == "__main__":
    try:
        asyncio.run(MainClass().main())
    except KeyboardInterrupt:
        logger.info("Exiting scanner... Goodbye!")
