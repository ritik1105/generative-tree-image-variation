import json
import shutil
from pathlib import Path
from datetime import datetime


class RunTracker:
    """
    Tracks and stores all artifacts generated during a pipeline run.
    """

    def __init__(self, output_root="outputs"):

        self.output_root = Path(output_root)
        self.output_root.mkdir(exist_ok=True)

        self.run_dir = None
        self.images_dir = None
        self.prompts_dir = None
        self.metadata_dir = None
        self.input_dir = None

    # -------------------------------------------------------
    # Run Management
    # -------------------------------------------------------

    def create_run(self):

        existing_numbers = []

        for path in self.output_root.iterdir():

            if path.is_dir() and path.name.startswith("run_"):

                try:
                    existing_numbers.append(
                        int(path.name.split("_")[1])
                    )

                except (IndexError, ValueError):
                    continue

        run_number = max(existing_numbers, default=0) + 1

        self.run_dir = self.output_root / f"run_{run_number:03d}"

        self.images_dir = self.run_dir / "images"
        self.prompts_dir = self.run_dir / "prompts"
        self.metadata_dir = self.run_dir / "metadata"
        self.input_dir = self.run_dir / "input"

        self.images_dir.mkdir(parents=True)
        self.prompts_dir.mkdir()
        self.metadata_dir.mkdir()
        self.input_dir.mkdir()

        return self.run_dir

    # -------------------------------------------------------
    # Input
    # -------------------------------------------------------

    def save_input_image(self, image_path):

        image_path = Path(image_path)

        destination = self.input_dir / image_path.name

        shutil.copy2(
            image_path,
            destination
        )

    # -------------------------------------------------------
    # Prompt
    # -------------------------------------------------------

    def save_prompt(
        self,
        prompt,
        image_index
    ):

        filename = (
            self.prompts_dir
            / f"prompt_{image_index:03d}.txt"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(prompt)

    # -------------------------------------------------------
    # Metadata
    # -------------------------------------------------------

    def save_metadata(
        self,
        metadata,
        image_index
    ):

        filename = (
            self.metadata_dir
            / f"metadata_{image_index:03d}.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

    # -------------------------------------------------------
    # Image
    # -------------------------------------------------------

    def save_image(
        self,
        image,
        image_index
    ):

        filename = (
            self.images_dir
            / f"image_{image_index:03d}.png"
        )

        image.save(filename)

    # -------------------------------------------------------
    # Combined Save
    # -------------------------------------------------------

    def save_generation(
        self,
        result,
        variation,
        image_index
    ):

        self.save_prompt(
            result.prompt,
            image_index
        )

        metadata = {
            **variation,
            **result.to_metadata_dict()
        }

        self.save_metadata(
            metadata,
            image_index
        )

        self.save_image(
            result.image,
            image_index
        )

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------

    def finalize(
        self,
        summary
    ):

        summary["completed_at"] = (
            datetime.now().isoformat()
        )

        filename = (
            self.run_dir
            / "summary.json"
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4
            )