from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenerationRequest:
    """
    Represents a complete image generation request.
    """

    generation_mode: str

    species: str

    input_image: Optional[str] = None

    season: list[str] = field(default_factory=list)

    weather: list[str] = field(default_factory=list)

    health: list[str] = field(default_factory=list)

    lighting: list[str] = field(default_factory=list)

    camera_angle: list[str] = field(default_factory=list)

    time_of_day: list[str] = field(default_factory=list)

    num_images: int = 1

    random_seed: Optional[int] = None

    strength: Optional[float] = None