# Bangla AI Image Studio

AI image generation starter app inspired by Fooocus — designed for local prompt-to-image workflows with a simple Gradio interface.

This project is a lightweight starter template and is not affiliated with the official Fooocus project or its model files.

## Features

- Prompt and negative prompt input
- Width / height controls
- Inference steps and guidance scale controls
- Seed-based reproducible generation
- Saves generated output to the `outputs/` folder
- Works with CUDA, MPS, or CPU fallback
- Easy local startup in one command

## Download

You can download the project source from GitHub:

- https://github.com/sksoponroy1252/fooocus-style-template

To get the latest files locally:

```bash
git clone https://github.com/sksoponroy1252/fooocus-style-template.git
cd fooocus-style-template
```

## Quick start

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Or use the included launcher:

```powershell
run_windows.bat
```

Then open:

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

## Model configuration

The project uses Hugging Face Diffusers by default:

```text
stable-diffusion-v1-5/stable-diffusion-v1-5
```

To use a different model:

### PowerShell

```powershell
$env:MODEL_ID="your-org/your-model-name"
python app.py
```

### Bash

```bash
MODEL_ID="your-org/your-model-name" python app.py
```

If the model is gated, sign in with Hugging Face first:

```bash
huggingface-cli login
```

## Hardware notes

- NVIDIA GPU: recommended for faster generation
- Apple Silicon / MPS: supported if available
- CPU mode: works but can be slow

## Output folder

Generated images are saved in:

```text
outputs/
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── run_windows.bat
├── README.md
├── outputs/
└── .gitignore
```

## Important notice

This is a starter project for learning and local experimentation. It does not ship with an official Fooocus model or secure commercial license. Please respect model licensing, platform rules, and local legal requirements before publishing or sharing generated output.

## License

This repository is provided as a starter template for educational use. Add an appropriate license if you plan to distribute it publicly or commercially.
