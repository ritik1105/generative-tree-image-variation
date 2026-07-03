# Synthetic Tree Image Generation Pipeline

## Overview

This feature branch implements a modular synthetic tree image generation pipeline using Stable Diffusion XL (SDXL).

The goal is to generate realistic tree images from structured generation requests while supporting both Text-to-Image and Image-to-Image workflows. The architecture is designed to be model-agnostic so that additional image generation backends (FLUX, ComfyUI, hosted APIs, etc.) can be integrated in the future with minimal changes.

---

# Features

## Supported Generation Modes

### Text-to-Image

Generate tree images from structured prompts.

Example:

- Species
- Season
- Weather
- Lighting
- Health
- Camera Angle
- Time of Day

↓

Photorealistic generated tree image.

---

### Image-to-Image

Generate variations from an existing tree image.

Example transformations:

- Summer → Winter
- Clear → Rainy
- Healthy → Stressed
- Morning → Evening

while preserving the overall tree structure.

---

# Generation Workflow

1. Load generation request.
2. Validate request.
3. Normalize missing values.
4. Generate variation combinations.
5. Sample requested combinations.
6. Build SDXL prompts.
7. Generate images.
8. Save images, prompts, metadata, and summary.

---

# Current Capabilities

- Text-to-Image generation
- Image-to-Image generation
- Config-driven defaults
- Modular SDXL adapter
- Generation metadata logging
- Prompt generation
- Request validation
- Run tracking
- JSON-based request loading

---

# Technologies

- Python
- Stable Diffusion XL
- Hugging Face Diffusers
- PyTorch
- Pillow
- YAML
- Dataclasses

---

# Future Improvements

- Negative prompt generation
- Prompt template engine
- Species-specific prompt tuning
- ControlNet integration
- Inpainting
- FLUX adapter
- ComfyUI adapter
- REST API
- Batch generation UI
