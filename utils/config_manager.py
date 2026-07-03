from pathlib import Path
import yaml


class ConfigManager:

    _config = None

    @classmethod
    def load(cls):

        if cls._config is None:

            with open(
                Path("config/defaults.yaml"),
                "r",
                encoding="utf-8"
            ) as file:

                cls._config = yaml.safe_load(file)

        return cls._config

    @classmethod
    def defaults(cls):
        return cls.load()["defaults"]

    @classmethod
    def variations(cls):
        return cls.load()["variations"]