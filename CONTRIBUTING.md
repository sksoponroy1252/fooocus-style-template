# Contributing

Thanks for considering a contribution to Bangla AI Image Studio.

## Development setup

Use Python 3.10+ and create an isolated virtual environment. Install runtime dependencies with `pip install -r requirements.txt`. The unit tests use Python's standard library and do not download the image model.

## Before opening a pull request

```bash
python -m compileall -q app.py studio_utils.py tests
python -m unittest discover -s tests -v
```

Please keep changes focused, explain the user impact, update docs when behavior changes, and include screenshots for UI changes. Never commit secrets, model weights, generated personal content, `.env`, or Hugging Face credentials.

## Reporting issues

Include reproduction steps, expected and actual behavior, OS, Python version, GPU, model ID, and relevant sanitized logs. Do not post access tokens or private prompts.
