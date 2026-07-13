from pathlib import Path
import yaml


class NegativePromptBuilder:
    """
    Builds reusable negative prompts.
    """

    def __init__(self):

        config_path = Path(
            "config/negative_prompts.yaml"
        )

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.config = yaml.safe_load(file)

    def build(self):

        negatives = []

        for profile in self.config.values():

            negatives.extend(
                profile.get(
                    "descriptors",
                    []
                )
            )

        return ", ".join(negatives)