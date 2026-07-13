from dataclasses import dataclass
from PIL import Image


@dataclass
class GenerationResult:

    image: Image.Image
    model: str
    prompt: str
    negative_prompt: str | None
    seed: int | None
    guidance_scale: float
    num_inference_steps: int
    width: int
    height: int
    generation_time: float

    def to_metadata_dict(self):
        return {
            "model": self.model,
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "guidance_scale": self.guidance_scale,
            "num_inference_steps": self.num_inference_steps,
            "width": self.width,
            "height": self.height,
            "generation_time": self.generation_time,
        }