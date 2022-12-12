"""Setup logger for project."""

import logging


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        self.addHandler(handler)

        formatter = logging.Formatter(
            "[%(asctime)s:%(name)s:%(levelname)s:%(funcName)s]: %(message)s"
        )
        handler.setFormatter(formatter)
