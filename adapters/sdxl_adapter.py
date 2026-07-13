import time
from pathlib import Path

from numpy import rint
from typer import prompt
from config.config_manager import ConfigManager
import torch
import yaml
from PIL import Image

from diffusers import (
    AutoPipelineForText2Image,
    AutoPipelineForImage2Image,
)

from adapters.base_adapter import BaseAdapter
from generation_result import GenerationResult


class SDXLAdapter(BaseAdapter):
    """
    Adapter for Stable Diffusion XL.

    Supports:
        • Text-to-Image
        • Image-to-Image
    """

    DEFAULT_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

    def __init__(
        self,
        model_name=None,
        device=None,
        torch_dtype=None,
    ):
        super().__init__(model_name or self.DEFAULT_MODEL)

        self.device = (
            device
            if device is not None
            else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        if torch_dtype is None:
            self.torch_dtype = (
                torch.float16
                if self.device == "cuda"
                else torch.float32
            )
        else:
            self.torch_dtype = torch_dtype

        self.text_pipeline = None
        self.img2img_pipeline = None

        self.config = ConfigManager.defaults()

    # -------------------------------------------------------
    # Configuration
    # -------------------------------------------------------

    def load_config(self):

        config_path = Path("config/defaults.yaml")

        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config.get("defaults", {})

    # -------------------------------------------------------
    # Pipeline Loading
    # -------------------------------------------------------

    def load_text_pipeline(self):

        if self.text_pipeline is not None:
            return

        self.text_pipeline = AutoPipelineForText2Image.from_pretrained(
            self.model_name,
            torch_dtype=self.torch_dtype,
            use_safetensors=True,
        )

        self.text_pipeline.to(self.device)

        if self.device == "cuda":
            self.text_pipeline.enable_attention_slicing()
            self.text_pipeline.enable_vae_slicing()

    def load_img2img_pipeline(self):

        if self.img2img_pipeline is not None:
            return

        self.img2img_pipeline = AutoPipelineForImage2Image.from_pretrained(
            self.model_name,
            torch_dtype=self.torch_dtype,
            use_safetensors=True,
        )

        self.img2img_pipeline.to(self.device)

        if self.device == "cuda":
            self.img2img_pipeline.enable_attention_slicing()
            self.img2img_pipeline.enable_vae_slicing()

    # -------------------------------------------------------
    # Text-to-Image
    # -------------------------------------------------------

    def generate_text_to_image(
        self,
        prompt,
        negative_prompt=None,
        seed=None,
        num_inference_steps=None,
        guidance_scale=None,
        width=None,
        height=None,
        **kwargs
    ):

        num_inference_steps = (
            num_inference_steps
            if num_inference_steps is not None
            else self.config["num_inference_steps"]
        )

        guidance_scale = (
            guidance_scale
            if guidance_scale is not None
            else self.config["guidance_scale"]
        )

        width = (
            width
            if width is not None
            else self.config["output_width"]
        )

        height = (
            height
            if height is not None
            else self.config["output_height"]
        )

        if self.text_pipeline is None:
            self.load_text_pipeline()

        generator = None

        if seed is not None:
            generator = torch.Generator(device=self.device)
            generator.manual_seed(seed)

        start = time.perf_counter()
        print("\n" + "="*80)
        print("POSITIVE PROMPT")
        print(prompt)

        print("\nNEGATIVE PROMPT")
        print(negative_prompt)
        print("="*80 + "\n")
        result = self.text_pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
            **kwargs
        )

        generation_time = time.perf_counter() - start

        return GenerationResult(
            image=result.images[0],
            model=self.model_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=width,
            height=height,
            generation_time=generation_time,
        )

    # -------------------------------------------------------
    # Image-to-Image
    # -------------------------------------------------------

    def generate_image_to_image(
        self,
        image_path,
        prompt,
        negative_prompt=None,
        seed=None,
        strength=None,
        num_inference_steps=None,
        guidance_scale=None,
        **kwargs
    ):

        strength = (
            strength
            if strength is not None
            else self.config["strength"]
        )

        num_inference_steps = (
            num_inference_steps
            if num_inference_steps is not None
            else self.config["num_inference_steps"]
        )

        guidance_scale = (
            guidance_scale
            if guidance_scale is not None
            else self.config["guidance_scale"]
        )

        if self.img2img_pipeline is None:
            self.load_img2img_pipeline()

        with Image.open(image_path) as img:
            image = img.convert("RGB")

        image = image.resize(
            (
                self.config["output_width"],
                self.config["output_height"],
            )
        )

        generator = None

        if seed is not None:
            generator = torch.Generator(device=self.device)
            generator.manual_seed(seed)

        start = time.perf_counter()
        print("\n" + "="*80)
        print("POSITIVE PROMPT")
        print(prompt)

        print("\nNEGATIVE PROMPT")
        print(negative_prompt)
        print("="*80 + "\n")
        result = self.img2img_pipeline(
            prompt=prompt,
            image=image,
            negative_prompt=negative_prompt,
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
            **kwargs
        )

        generation_time = time.perf_counter() - start

        return GenerationResult(
            image=result.images[0],
            model=self.model_name,
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            width=self.config["output_width"],
            height=self.config["output_height"],
            generation_time=generation_time,
        )