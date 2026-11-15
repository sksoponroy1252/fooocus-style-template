# Angular + Python AI Image Studio

This repository is a modern local AI image generator UI built with Angular on the frontend and Python on the backend.

## Structure

```text
.
├── frontend/
│   ├── angular.json
│   ├── package.json
│   ├── src/
│   └── ...
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model_utils.py
│   └── outputs/
├── docker-compose.yml
├── README.md
├── .env.example
└── .gitignore
```

## Features

- Angular dashboard UI
- Python backend with Diffusers model generation
- prompt, negative prompt, seeds, style presets, aspect ratio controls
- generation history and metadata save
- responsive design
- local-only setup by default
- Docker support

## Quick start

### 1) Frontend

```bash
cd frontend
npm install
npm start
```

### 2) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3) Docker

```bash
docker-compose up --build
```

## Notes

- The backend uses Hugging Face Diffusers and downloads the model on first run.
- Keep `.env` files private and do not commit credentials.
- Model terms and generated image usage remain subject to the chosen model license.
