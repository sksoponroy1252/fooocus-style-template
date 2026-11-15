import json
import logging
import os
import secrets
import threading
from datetime import datetime, timezone
from pathlib import Path

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

from studio_utils import ASPECT_RATIOS, STYLE_PRESETS, build_effective_prompt, parse_generation_inputs

APP_NAME = "Bangla AI Image Studio"
MODEL_ID = os.getenv("MODEL_ID", "stable-diffusion-v1-5/stable-diffusion-v1-5")
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

_pipe = None
_pipeline_lock = threading.Lock()
generation_lock = threading.Lock()


def get_device_and_dtype():
    if torch.cuda.is_available():
        return "cuda", torch.float16
    mps = getattr(torch.backends, "mps", None)
    if mps and mps.is_available():
        return "mps", torch.float16
    return "cpu", torch.float32


def load_pipeline():
    global _pipe
    if _pipe is not None:
        return _pipe

    with _pipeline_lock:
        if _pipe is not None:
            return _pipe
        device, dtype = get_device_and_dtype()
        logger.info("Loading model %s on %s", MODEL_ID, device)
        pipeline = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            use_safetensors=True,
        )
        pipeline = pipeline.to(device)
        if device == "cuda":
            pipeline.enable_attention_slicing()
        _pipe = pipeline
    return _pipe


def _save_result(image, metadata):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = OUTPUT_DIR / f"image-{stamp}-{secrets.token_hex(4)}.png"
    image.save(path, format="PNG")
    metadata_path = path.with_suffix(".json")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def get_history(limit=24):
    images = sorted(OUTPUT_DIR.glob("image-*.png"), key=lambda item: item.stat().st_mtime, reverse=True)
    return [(str(path), path.name) for path in images[:limit]]


def generate_images(prompt, negative_prompt, aspect_ratio, steps, guidance, seed, batch_count, style, progress=gr.Progress()):
    try:
        values = parse_generation_inputs(
            prompt=prompt,
            negative_prompt=negative_prompt,
            aspect_ratio=aspect_ratio,
            steps=steps,
            guidance=guidance,
            seed=seed,
            batch_count=batch_count,
            style=style,
        )
    except ValueError as exc:
        raise gr.Error(str(exc)) from exc

    effective_prompt = build_effective_prompt(values["prompt"], values["style"])
    device, _ = get_device_and_dtype()
    generator_device = "cuda" if device == "cuda" else "cpu"
    seeds = [values["seed"] + index for index in range(values["batch_count"])]
    generators = [torch.Generator(device=generator_device).manual_seed(item) for item in seeds]
    width, height = ASPECT_RATIOS[values["aspect_ratio"]]

    if not generation_lock.acquire(blocking=False):
        raise gr.Error("একটি generation চলছে। কিছুক্ষণ পরে আবার চেষ্টা করুন।")

    saved_paths = []
    try:
        pipeline = load_pipeline()

        def on_step_end(pipe, step, timestep, callback_kwargs):
            progress((step + 1, values["steps"]), desc=f"Generating image · step {step + 1}/{values['steps']}")
            return callback_kwargs

        result = pipeline(
            prompt=[effective_prompt] * values["batch_count"],
            negative_prompt=[values["negative_prompt"] or ""] * values["batch_count"],
            width=width,
            height=height,
            num_inference_steps=values["steps"],
            guidance_scale=values["guidance"],
            generator=generators,
            callback_on_step_end=on_step_end,
        )

        for image, image_seed in zip(result.images, seeds):
            metadata = {
                "prompt": values["prompt"],
                "effective_prompt": effective_prompt,
                "negative_prompt": values["negative_prompt"],
                "style": values["style"],
                "model_id": MODEL_ID,
                "width": width,
                "height": height,
                "steps": values["steps"],
                "guidance_scale": values["guidance"],
                "seed": image_seed,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            saved_paths.append(_save_result(image, metadata))

        gallery = [(str(path), f"Seed {seeds[index]} · {path.name}") for index, path in enumerate(saved_paths)]
        status = f"✅ {len(saved_paths)} image(s) generated · device: {device} · model: {MODEL_ID}"
        return gallery, [str(path) for path in saved_paths], status, get_history()
    except torch.cuda.OutOfMemoryError as exc:
        torch.cuda.empty_cache()
        logger.exception("CUDA out of memory")
        raise gr.Error("GPU memory শেষ হয়ে গেছে। কম resolution বা batch count ব্যবহার করুন।") from exc
    except Exception as exc:
        logger.exception("Image generation failed")
        raise gr.Error(f"Generation ব্যর্থ হয়েছে: {exc}") from exc
    finally:
        generation_lock.release()


CSS = """
:root { --studio-accent: #7357ff; }
.gradio-container { max-width: 1280px !important; margin: auto !important; }
#hero { text-align: center; padding: 1.6rem 1rem 1rem; }
#hero h1 { font-size: clamp(2rem, 5vw, 3.3rem); margin-bottom: .35rem; }
#hero p { opacity: .8; font-size: 1.05rem; }
#generate { min-height: 3.2rem; font-size: 1.05rem; }
"""

with gr.Blocks(title=APP_NAME, theme=gr.themes.Soft(primary_hue="violet"), css=CSS) as demo:
    gr.Markdown(
        "# Bangla AI Image Studio\n"
        "লোকাল মেশিনে prompt থেকে ছবি তৈরি করুন — নিজের model, style ও generation settings বেছে নিন।",
        elem_id="hero",
    )

    with gr.Row():
        with gr.Column(scale=6):
            prompt_input = gr.Textbox(
                label="Prompt",
                placeholder="যেমন: cinematic portrait of a Bengali woman in a garden, golden-hour light, detailed photography",
                lines=5,
                max_lines=10,
            )
            with gr.Row():
                style_input = gr.Dropdown(choices=list(STYLE_PRESETS), value="None", label="Style preset")
                aspect_input = gr.Dropdown(choices=list(ASPECT_RATIOS), value="Square · 1:1", label="Aspect ratio")
            negative_input = gr.Textbox(
                label="Negative prompt · optional",
                placeholder="blurry, low quality, distorted, watermark",
                lines=2,
            )
            with gr.Accordion("Advanced settings", open=True):
                with gr.Row():
                    steps_input = gr.Slider(10, 60, value=25, step=1, label="Inference steps")
                    guidance_input = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance scale")
                with gr.Row():
                    seed_input = gr.Number(value=-1, precision=0, label="Seed · -1 for random")
                    batch_input = gr.Slider(1, 4, value=1, step=1, label="Images per run")
            generate_button = gr.Button("✨ Generate images", variant="primary", elem_id="generate")
            status_output = gr.Markdown("Ready when you are.")

        with gr.Column(scale=5):
            result_gallery = gr.Gallery(label="New images", columns=2, height=480, object_fit="contain", preview=True)
            downloads_output = gr.File(label="Download generated files", file_count="multiple")

    with gr.Accordion("Recent generations", open=False):
        history_gallery = gr.Gallery(label="Saved locally in outputs/", columns=4, height=300, object_fit="contain")
        refresh_button = gr.Button("Refresh history")

    generate_button.click(
        fn=generate_images,
        inputs=[prompt_input, negative_input, aspect_input, steps_input, guidance_input, seed_input, batch_input, style_input],
        outputs=[result_gallery, downloads_output, status_output, history_gallery],
        concurrency_limit=1,
    )
    refresh_button.click(fn=get_history, inputs=None, outputs=history_gallery)
    demo.load(fn=get_history, inputs=None, outputs=history_gallery)

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=1).launch(server_name="127.0.0.1", server_port=int(os.getenv("PORT", "7860")))
