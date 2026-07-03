from pathlib import Path


class RequestValidator:

    @staticmethod
    def validate(request):

        if request.generation_mode not in (
            "text2image",
            "img2img",
        ):
            raise ValueError(
                f"Unsupported mode: {request.generation_mode}"
            )

        if not request.species:
            raise ValueError(
                "Species is required."
            )

        if request.num_images < 1:
            raise ValueError(
                "num_images must be at least 1."
            )

        if (
            request.generation_mode == "img2img"
            and not Path(request.input_image).exists()
        ):
            raise FileNotFoundError(
                request.input_image
            )