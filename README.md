# Bangla AI Image Studio

একটি সহজ, লোকাল AI image-generation starter app—Fooocus-এর মতো prompt লিখে ছবি তৈরি করার জন্য। এটি Fooocus-এর কপি নয় এবং Fooocus-এর কোড/মডেল অন্তর্ভুক্ত করে না। ছবি তৈরি করতে Hugging Face থেকে একটি Stable Diffusion model ডাউনলোড হবে; model-এর লাইসেন্স মেনে চলুন।

## ফিচার

- Prompt এবং negative prompt দিয়ে ছবি তৈরি
- Width/height, inference steps, guidance scale এবং seed নিয়ন্ত্রণ
- তৈরি ছবিগুলো `outputs/` ফোল্ডারে সংরক্ষণ
- CUDA GPU থাকলে সেটি ব্যবহার; না থাকলে CPU fallback (CPU-তে খুব ধীর হতে পারে)
- প্রথমবার model download করে local Hugging Face cache-এ রাখে

## Windows-এ চালানো

1. Python 3.10 বা 3.11 ইনস্টল করুন।
2. NVIDIA GPU থাকলে PyTorch-এর উপযুক্ত CUDA install command নিন [PyTorch-এর অফিসিয়াল পেজ](https://pytorch.org/get-started/locally/) থেকে। শুধু CPU-তে চালালে নিচের কমান্ড ব্যবহার করুন:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   pip install -r requirements.txt
   python app.py
   ```

3. ব্রাউজারে `http://127.0.0.1:7860` খুলুন। পরেরবার চালাতে `run_windows.bat` ব্যবহার করতে পারেন।

## Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
# NVIDIA GPU হলে PyTorch-এর উপযুক্ত command: https://pytorch.org/get-started/locally/
pip install -r requirements.txt
python app.py
```

macOS-এ MPS সমর্থিত হলে অ্যাপ সেটি ব্যবহার করার চেষ্টা করে।

## Model বেছে নেওয়া

ডিফল্ট model `stable-diffusion-v1-5/stable-diffusion-v1-5`। চাইলে `MODEL_ID` environment variable দিয়ে নিজের পছন্দের Diffusers-compatible model দিন। Model download-এর জন্য যথেষ্ট disk space ও internet দরকার। Gated model হলে Hugging Face-এ access অনুমোদন নিয়ে `huggingface-cli login` চালান.

PowerShell:

```powershell
$env:MODEL_ID="your-org/your-diffusers-model"
python app.py
```

Bash:

```bash
MODEL_ID="your-org/your-diffusers-model" python app.py
```

## Hardware

- NVIDIA GPU সুপারিশ করা হয়; VRAM-এর প্রয়োজন model ও image size-এর উপর নির্ভরশীল।
- CPU mode কাজ করতে পারে, কিন্তু generation দীর্ঘ সময় নিতে পারে।
- বড় resolution বা বেশি steps memory/time বাড়ায়।

## সতর্কতা

- তৈরি ছবির ব্যবহার model-এর লাইসেন্স এবং প্রযোজ্য আইন/নীতির অধীন।
- এটি একটি starter app, Fooocus-এর সমমানের feature set নয়।
- এটি `127.0.0.1`-এ local-only server চালায়; ইচ্ছাকৃতভাবে public sharing চালু করা নেই।
