import yaml


class ConfigManager:

    @classmethod
    def _load_yaml(cls, path):
        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    @classmethod
    def defaults(cls):
        data = cls._load_yaml("config/defaults.yaml")
        return data.get("defaults", {})

    @classmethod
    def prompt_templates(cls):
        return cls._load_yaml("config/prompt_templates.yaml")

    @classmethod
    def negative_prompts(cls):
        return cls._load_yaml("config/negative_prompts.yaml")

    @classmethod
    def species_profiles(cls):
        return cls._load_yaml("config/species_profiles.yaml")

    @classmethod
    def season_profiles(cls):
        return cls._load_yaml("config/season_profiles.yaml")

    @classmethod
    def weather_profiles(cls):
        return cls._load_yaml("config/weather_profiles.yaml")

    @classmethod
    def camera_profiles(cls):
        return cls._load_yaml("config/camera_profiles.yaml")

    @classmethod
    def lighting_profiles(cls):
        return cls._load_yaml("config/lighting_profiles.yaml")

    @classmethod
    def realism_profiles(cls):
        return cls._load_yaml("config/realism_profiles.yaml")
    
    @classmethod
    def composition_profiles(cls):
        return cls._load_yaml("config/composition_profiles.yaml")