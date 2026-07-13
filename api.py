from pathlib import Path
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)
from fastapi.middleware.cors import CORSMiddleware

from models.generation_request import GenerationRequest
from pipeline.image_generation_pipeline import ImageGenerationPipeline
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = ImageGenerationPipeline()

@app.get("/")
def home():
    return {
        "message": "Synthetic Tree Generator API Running"
    }


@app.get("/test")
def test():
    return {
        "status": "Backend Connected!"
    }

@app.post("/generate")
async def generate(

    prompt: str = Form(""),

    generation_mode: str = Form(...),

    species: str = Form(...),

    season: str = Form(""),

    weather: str = Form(""),

    lighting: str = Form(""),

    camera_angle: str = Form(""),

    health: str = Form(""),

    time_of_day: str = Form(""),

    num_images: int = Form(1),

    image: UploadFile | None = File(None),

):

    image_path = None

    # Save uploaded image (if provided)
    if image is not None:

        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        image_path = upload_dir / image.filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    request = GenerationRequest(

        generation_mode=generation_mode,

        species=species,

        prompt=prompt,

        input_image=str(image_path) if image_path else None,

        season=season.split(",") if season else [],

        weather=weather.split(",") if weather else [],

        lighting=lighting.split(",") if lighting else [],

        camera_angle=camera_angle.split(",") if camera_angle else [],

        health=health.split(",") if health else [],

        time_of_day=time_of_day.split(",") if time_of_day else [],

        num_images=num_images,
    )

    result = pipeline.run(request)

    result["images"] = [
        "/" + image.replace("\\", "/")
        for image in result["images"]
    ]

    return result