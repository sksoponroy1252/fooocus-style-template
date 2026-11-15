# Bangla AI Image Studio

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Gradio-5.x-orange" alt="Gradio 5.x" />
  <img src="https://img.shields.io/badge/Diffusers-0.32.x-8A2BE2" alt="Diffusers 0.32.x" />
  <img src="https://img.shields.io/badge/Status-Starter%20Template-success" alt="Starter Template" />
</div>

Bangla AI Image Studio is a local, prompt-to-image starter built with Python, Gradio, and Diffusers. It is inspired by the workflow of tools like Fooocus, but it is a lightweight independent template for local experimentation and learning.

This repository is designed for users who want a clean starting point to generate AI images from text prompts on their own machine.

## Overview

- Prompt-based image generation
- Optional negative prompt
- Width, height, steps, guidance scale, and seed controls
- Local model loading with Hugging Face Diffusers
- Generated files saved into the `outputs/` folder
- Works with CUDA, MPS, or CPU fallback

## Why this project exists

Many users want a simple local AI image generation workflow without the complexity of a full production application. This project provides a clean starter template that is:

- easy to run locally
- easy to customize
- suitable for experimentation and learning
- lightweight compared to full-featured desktop tools

## Download

Clone the repository:

```bash
git clone https://github.com/sksoponroy1252/fooocus-style-template.git
cd fooocus-style-template
```

## Quick Start

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

You can also launch directly with:

```powershell
run_windows.bat
```

After startup, open:

```text
http://127.0.0.1:7860
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## Model Setup

This project uses a Hugging Face Diffusers model by default:

```text
stable-diffusion-v1-5/stable-diffusion-v1-5
```

### Use another model

PowerShell:

```powershell
$env:MODEL_ID="your-org/your-model-name"
python app.py
```

Bash:

```bash
MODEL_ID="your-org/your-model-name" python app.py
```

If the model is gated, authenticate first:

```bash
huggingface-cli login
```

## Features

### Image generation controls

- Prompt text
- Negative prompt
- Width and height
- Steps and guidance scale
- Random or fixed seed

### Local workflow

- Model loads only once and stays cached on disk
- Generated output saved to `outputs/`
- Easy to customize based on project needs

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── run_windows.bat
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── outputs/
├── .gitignore
└── .venv/
```

## Hardware Notes

- NVIDIA GPU: recommended for the best performance
- Apple Silicon / MPS: supported when available
- CPU fallback: works but may be slow for larger generations

## Output Directory

Generated images are saved under:

```text
outputs/
```

## Troubleshooting

### Model download is slow

- Check your internet connection
- Confirm you have enough disk space
- Use a smaller model if needed

### CUDA not detected

- Verify your GPU driver is installed
- Install the correct PyTorch build for your hardware
- Launch in CPU mode if needed

### Application does not open

- Ensure dependencies are installed with `pip install -r requirements.txt`
- Re-create the virtual environment if the setup is inconsistent

## Contribution

Contributions are welcome. Please open an issue or submit a pull request if you want to improve the project.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Important Notice

This project is a starter template for local experimentation and learning. It does not contain official Fooocus commercial assets, proprietary model bundles, or any bundled paid software. Model licensing and generated image usage remain subject to the respective model license and applicable local laws.

## Status

Production-ready for local experimentation and customization, but not intended as a full replacement for professional image generation stack or commercial deployment tooling.
