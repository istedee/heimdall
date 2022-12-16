"""Setup logger for project."""

import logging


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        self.addHandler(handler)

        formatter = logging.Formatter(
            "[%(asctime)s:%(filename)s:%(levelname)s:%(funcName)s]: %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
        )
        handler.setFormatter(formatter)
