# 🌳 Synthetic Tree Image Generator

A modular AI-powered application for generating realistic synthetic tree images using Stable Diffusion XL (SDXL). The project supports both **Text-to-Image** and **Image-to-Image** generation through a React-based frontend and a FastAPI backend.

## Features

- Text-to-Image generation
- Image-to-Image generation using a reference image
- Modular image generation pipeline
- YAML-driven prompt engineering
- Configurable variation generation
- React frontend for user interaction
- FastAPI backend API
- Automatic metadata and prompt tracking
- Extensible architecture for future model integrations

## Tech Stack

### Frontend
- React (Vite)
- Axios

### Backend
- Python
- FastAPI
- Stable Diffusion XL (Diffusers)
- Hugging Face Transformers
- Pillow

## Project Structure

```text
generative-tree-image-variation/
│
├── frontend/                 # React frontend
├── adapters/                 # Model adapters
├── config/                   # YAML configuration files
├── generators/               # Prompt & variation generation
├── metadata/                 # Run tracking
├── models/                   # Request models
├── pipeline/                 # Image generation pipeline
├── validators/               # Request validation
├── outputs/                  # Generated images and metadata
├── uploads/                  # Uploaded reference images
├── api.py                    # FastAPI server
└── main.py                   # Standalone pipeline entry point
```

## Current Workflow

```text
React UI
      │
      ▼
 FastAPI Backend
      │
      ▼
Generation Request
      │
      ▼
Image Generation Pipeline
      │
 ┌────┼──────────────┐
 ▼    ▼              ▼
Variation Engine
Prompt Builder
Negative Prompt Builder
      │
      ▼
SDXL Adapter
      │
      ▼
Run Tracker
      │
      ▼
Generated Images
```

## Current UI Features

- Prompt input
- Reference image upload
- Species selection
- Weather selection
- Lighting selection
- Camera angle selection
- Health condition selection
- Time of day selection
- Generated image preview

## Running the Backend

```bash
python -m uvicorn api:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

## Running the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

## Supported Generation Modes

### Text-to-Image

Generate tree images from textual descriptions.

### Image-to-Image

Generate variations using an uploaded reference image.

## Output

Each generation creates a new run inside:

```text
outputs/
└── run_xxx/
    ├── images/
    ├── prompts/
    ├── metadata/
    ├── input/
    └── summary.json
```

## Configuration

The generation pipeline is driven by YAML configuration files located in the `config/` directory, including:

- Prompt templates
- Species profiles
- Weather profiles
- Season profiles
- Camera profiles
- Lighting profiles
- Realism profiles
- Negative prompts
- Default generation settings

## Current Status

Implemented:

- ✅ React frontend
- ✅ FastAPI backend
- ✅ Text-to-Image generation
- ✅ Image-to-Image generation
- ✅ Prompt Builder
- ✅ Negative Prompt Builder
- ✅ Variation Engine
- ✅ Run Tracker
- ✅ Metadata generation
- ✅ Image upload
- ✅ Generated image preview

Planned:

- Dynamic UI options from backend
- Prompt preview
- Improved image quality
- ControlNet integration
- LoRA support
- Additional model adapters (FLUX, ComfyUI)

## License

This project was developed as part of a synthetic tree image generation challenge and is intended for research and development purposes.