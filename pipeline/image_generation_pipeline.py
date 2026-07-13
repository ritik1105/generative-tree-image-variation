
from generators.variation_engine import VariationEngine
from generators.prompt_builder import PromptBuilder
from adapters.sdxl_adapter import SDXLAdapter
from metadata.tracker import RunTracker
from validators.request_validator import RequestValidator
from utils.logger import logger
from generators.negative_prompt_builder import NegativePromptBuilder

class ImageGenerationPipeline:
    """
    Orchestrates the complete image generation workflow.
    """

    def __init__(self):

        self.variation_engine = VariationEngine()

        self.prompt_builder = PromptBuilder()

        self.adapter = SDXLAdapter()

        self.tracker = RunTracker()

        self.negative_prompt_builder = NegativePromptBuilder()

    def run(self, request):

        # ------------------------------------------
        # Validate request
        # ------------------------------------------

        RequestValidator.validate(request)

        # ------------------------------------------
        # Determine generation mode
        # ------------------------------------------

        mode = request.generation_mode

        if mode == "text2image":

            self.adapter.load_text_pipeline()

        elif mode == "img2img":

            self.adapter.load_img2img_pipeline()

        else:

            raise ValueError(
                f"Unsupported mode: {mode}"
            )

        # ------------------------------------------
        # Normalize request
        # ------------------------------------------

        normalized_request = self.variation_engine.normalize_request(
            request.__dict__
        )

        combinations = self.variation_engine.generate_combinations(
            normalized_request
        )

        selected = self.variation_engine.sample_combinations(
            combinations,
            request.num_images
        )

        # ------------------------------------------
        # Create output run
        # ------------------------------------------

        self.tracker.create_run()

        if mode == "img2img":

            self.tracker.save_input_image(
                request.input_image
            )

        generation_times = []

        logger.info(
            f"Generating {len(selected)} image(s)..."
        )

        # ------------------------------------------
        # Generate
        # ------------------------------------------

        for index, variation in enumerate(
            selected,
            start=1
        ):

            try:

                logger.info(
                    f"[{index}/{len(selected)}]"
                )

                prompt = self.prompt_builder.build_prompt(
                    variation=variation,
                    template=request.template,
                    realism=request.realism_profile
                )

                # Prepend user prompt if provided
                if request.prompt.strip():
                    prompt = f"{request.prompt}, {prompt}"
                negative_prompt = self.negative_prompt_builder.build()

                if mode == "text2image":

                    result = self.adapter.generate_text_to_image(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        seed=request.random_seed
                    )

                else:

                    result = self.adapter.generate_image_to_image(
                        image_path=request.input_image,
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        seed=request.random_seed,
                        strength=request.strength
                )

                self.tracker.save_generation(
                    result,
                    variation,
                    index
                )

                generation_times.append(
                    result.generation_time
                )

                logger.info(
                    f"Completed image {index}"
                )

            except Exception as error:

                logger.exception(error)

                continue

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        average_time = (
            sum(generation_times)
            / len(generation_times)
            if generation_times
            else 0
        )

        summary = {

            "model": self.adapter.model_name,

            "generation_mode": mode,

            "species": request.species,

            "requested_images": request.num_images,

            "generated_images": len(generation_times),

            "average_generation_time": average_time,

            "total_generation_time": sum(generation_times),
        }

        self.tracker.finalize(summary)

        logger.info(
            "Generation completed successfully."
        )
        images_folder = self.tracker.images_dir

        generated_images = sorted(images_folder.glob("*.png"))

        return {
            "summary": summary,
            "images": [str(image) for image in generated_images]
        }