from abc import ABC, abstractmethod
from generation_result import GenerationResult


class BaseAdapter(ABC):
    """
    Abstract base class for all image generation adapters.

    Every model-specific adapter (SDXL, FLUX, ComfyUI, etc.)
    should implement these methods.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    # -------------------------------------------------------
    # Pipeline Loading
    # -------------------------------------------------------

    @abstractmethod
    def load_text_pipeline(self):
        """
        Load the text-to-image pipeline.
        """
        pass

    @abstractmethod
    def load_img2img_pipeline(self):
        """
        Load the image-to-image pipeline.
        """
        pass

    # -------------------------------------------------------
    # Generation
    # -------------------------------------------------------

    @abstractmethod
    def generate_text_to_image(
        self,
        prompt: str,
        negative_prompt: str = None,
        seed: int = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate an image from a text prompt.
        """
        pass

    @abstractmethod
    def generate_image_to_image(
        self,
        image_path: str,
        prompt: str,
        negative_prompt: str = None,
        seed: int = None,
        **kwargs
    ) -> GenerationResult:
        """
        Generate an image from an input image and prompt.
        """
        pass