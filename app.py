import os
import secrets
from pathlib import Path

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = os.getenv("MODEL_ID", "stable-diffusion-v1-5/stable-diffusion-v1-5")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

_pipe = None


def load_pipeline():
    """Load the model on first generation and reuse it for later requests."""
    global _pipe
    if _pipe is not None:
        return _pipe

    if torch.cuda.is_available():
        device, dtype = "cuda", torch.float16
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device, dtype = "mps", torch.float16
    else:
        device, dtype = "cpu", torch.float32

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        use_safetensors=True,
    )
    pipe = pipe.to(device)
    if device == "cuda":
        pipe.enable_attention_slicing()
    _pipe = pipe
    return _pipe


def generate(prompt, negative_prompt, width, height, steps, guidance, seed):
    prompt = (prompt or "").strip()
    if not prompt:
        raise gr.Error("একটি prompt লিখুন।")

    seed = int(seed)
    if seed < 0:
        seed = secrets.randbelow(2**31)
    generator_device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        generator_device = "mps"
    generator = torch.Generator(device=generator_device).manual_seed(seed)

    pipe = load_pipeline()
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt or None,
        width=int(width),
        height=int(height),
        num_inference_steps=int(steps),
        guidance_scale=float(guidance),
        generator=generator,
    )
    image = result.images[0]
    output_path = OUTPUT_DIR / f"image-{seed}.png"
    # Avoid overwriting an earlier image created with the same seed.
    if output_path.exists():
        output_path = OUTPUT_DIR / f"image-{seed}-{secrets.token_hex(3)}.png"
    image.save(output_path)
    return image, str(output_path), seed


with gr.Blocks(title="Bangla AI Image Studio", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Bangla AI Image Studio\nPrompt লিখে AI ছবি তৈরি করুন। প্রথমবার Generate চাপলে model download হবে।")
    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(label="Prompt", lines=4, placeholder="Describe the image you want...")
            negative_prompt = gr.Textbox(label="Negative prompt (optional)", lines=2)
            with gr.Row():
                width = gr.Dropdown([512, 640, 768], value=512, label="Width")
                height = gr.Dropdown([512, 640, 768], value=512, label="Height")
            steps = gr.Slider(10, 50, value=25, step=1, label="Steps")
            guidance = gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance scale")
            seed = gr.Number(value=-1, precision=0, label="Seed (-1 = random)")
            button = gr.Button("ছবি তৈরি করুন", variant="primary")
        with gr.Column(scale=1):
            image = gr.Image(label="Generated image", type="pil")
            saved_file = gr.Textbox(label="Saved file")
            used_seed = gr.Number(label="Used seed", precision=0)

    button.click(
        fn=generate,
        inputs=[prompt, negative_prompt, width, height, steps, guidance, seed],
        outputs=[image, saved_file, used_seed],
    )

demo.queue().launch(server_name="127.0.0.1", server_port=7860)
