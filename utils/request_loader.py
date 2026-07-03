import json
from pathlib import Path

from models.generation_request import GenerationRequest


class RequestLoader:
    """
    Loads generation requests from JSON files.
    """

    @staticmethod
    def load(path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Request file not found: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return GenerationRequest(**data)