"""Dependency-free validation and prompt preset helpers for the image studio."""

import math
import secrets

ASPECT_RATIOS = {
    "Square · 1:1": (512, 512),
    "Portrait · 2:3": (512, 768),
    "Landscape · 3:2": (768, 512),
    "Wide · 16:9": (768, 432),
}

STYLE_PRESETS = {
    "None": "",
    "Photographic": "photorealistic, natural lighting, professional photography, detailed",
    "Cinematic": "cinematic composition, dramatic lighting, film still, rich color grading",
    "Illustration": "high-quality digital illustration, expressive details, refined art",
    "Anime": "anime illustration, clean line art, vibrant colors, expressive character",
    "Watercolor": "watercolor painting, soft pigment texture, artistic brushwork",
    "3D render": "high-quality 3D render, detailed materials, studio lighting",
}

PROMPT_PRESETS = {
    "Custom": "",
    "Portrait": "professional portrait photo, soft natural light, detailed face, shallow depth of field",
    "Landscape": "beautiful landscape, atmospheric perspective, detailed environment, golden hour",
    "Product photo": "premium product photography, clean studio background, softbox lighting, sharp focus",
    "Fantasy art": "fantasy concept art, intricate worldbuilding, dramatic light, rich details",
}


def _bounded_int(value, label, minimum, maximum):
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{label} অবশ্যই পূর্ণসংখ্যা হতে হবে।") from exc
    if not minimum <= number <= maximum:
        raise ValueError(f"{label} {minimum} থেকে {maximum}-এর মধ্যে দিন।")
    return number


def parse_generation_inputs(prompt, negative_prompt, aspect_ratio, steps, guidance, seed, batch_count, style):
    prompt = (prompt or "").strip()
    if not prompt:
        raise ValueError("একটি prompt লিখুন।")
    if len(prompt) > 2000:
        raise ValueError("Prompt সর্বোচ্চ ২০০০ অক্ষরের হতে পারে।")
    negative_prompt = (negative_prompt or "").strip()
    if len(negative_prompt) > 2000:
        raise ValueError("Negative prompt সর্বোচ্চ ২০০০ অক্ষরের হতে পারে।")
    if aspect_ratio not in ASPECT_RATIOS:
        raise ValueError("তালিকা থেকে বৈধ aspect ratio বেছে নিন।")
    if style not in STYLE_PRESETS:
        raise ValueError("তালিকা থেকে বৈধ style preset বেছে নিন।")
    try:
        guidance = float(guidance)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Guidance scale অবশ্যই সংখ্যা হতে হবে।") from exc
    if not math.isfinite(guidance) or not 1 <= guidance <= 15:
        raise ValueError("Guidance scale 1 থেকে 15-এর মধ্যে দিন।")
    try:
        seed = int(seed)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("Seed অবশ্যই পূর্ণসংখ্যা হতে হবে।") from exc
    if seed < -1 or seed > 2**31 - 1:
        raise ValueError("Seed -1 থেকে 2147483647-এর মধ্যে দিন।")
    if seed == -1:
        seed = secrets.randbelow(2**31)
    return {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "aspect_ratio": aspect_ratio,
        "steps": _bounded_int(steps, "Steps", 10, 60),
        "guidance": guidance,
        "seed": seed,
        "batch_count": _bounded_int(batch_count, "Image count", 1, 4),
        "style": style,
    }


def build_effective_prompt(prompt, style):
    suffix = STYLE_PRESETS[style]
    return f"{prompt}, {suffix}" if suffix else prompt


def apply_prompt_preset(prompt, preset):
    """Append a selected prompt idea while preserving text already entered."""
    suffix = PROMPT_PRESETS.get(preset)
    if suffix is None:
        raise ValueError("অজানা prompt preset।")
    prompt = (prompt or "").strip()
    if not suffix:
        return prompt
    return f"{prompt}, {suffix}" if prompt else suffix
