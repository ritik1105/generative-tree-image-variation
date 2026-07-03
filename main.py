from pipeline.image_generation_pipeline import ImageGenerationPipeline
from utils.request_loader import RequestLoader


def main():

    request = RequestLoader.load(
        "sample_inputs/requests/img2img.json"
    )

    pipeline = ImageGenerationPipeline()

    pipeline.run(request)


if __name__ == "__main__":
    main()  