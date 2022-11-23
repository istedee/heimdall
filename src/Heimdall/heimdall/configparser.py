import yaml
from .utils import return_path


class ConfigManager:
    """
    Manages config of Heimdall
    """

    def __init__(self) -> None:
        self.settings = ""
        self.confPath = return_path("../config/config.yml")

    def set_config(self) -> None:
        """Set the configuration of Heimdall"""
        with open(self.confPath, "r") as config:
            settings = yaml.safe_load(config)
            self.settings = settings

    def get_config(self) -> dict:
        """Return current configuration from class"""
        return self.settings

    def check_configuration(self, current_conf) -> bool:
        """Compare configuration objects for differences"""
        return current_conf == self.load_config()

    def load_config(self) -> dict:
        """Load configuration file for inspection"""
        with open(self.confPath, "r") as config:
            settings = yaml.safe_load(config)
            return settings
