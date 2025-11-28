"""
Universal LLM Wrapper
Supports:
- Groq (FREE)
- Gemini (FREE)
- HuggingFace (FREE)

Main Function:
    call_llm(prompt, max_tokens=8000)
"""

import os
import requests
from loguru import logger

# ==========================================================
# SELECT DEFAULT FREE MODEL HERE: groq / gemini / hf
# ==========================================================
DEFAULT_BACKEND = "groq"


# ==========================================================
# PUBLIC ENTRYPOINT
# ==========================================================
def call_llm(prompt: str, max_tokens: int = 8000) -> str:
    """
    Main LLM caller – decides which backend to use.
    """

    backend = DEFAULT_BACKEND.lower()

    if backend == "groq":
        return call_groq(prompt, max_tokens)

    if backend == "gemini":
        return call_gemini(prompt, max_tokens)

    if backend == "hf":
        return call_huggingface(prompt, max_tokens)

    return "❌ ERROR: Invalid DEFAULT_BACKEND value."


# ==========================================================
# GROQ — Latest models (Dec 2025)
# ==========================================================
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

# Modern Groq models
GROQ_PRIMARY = "llama-3.3-70b-versatile"     # Best
GROQ_FALLBACK = "llama-3.3-8b-instant"       # Fast + stable


def call_groq(prompt, max_tokens=4096, temperature=0.6):
    """
    Groq LLM wrapper with fallback models.
    """

    if not groq_client:
        return "❌ [Groq Error] GROQ_API_KEY missing"

    for model in [GROQ_PRIMARY, GROQ_FALLBACK]:
        try:
            response = groq_client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            logger.info(f"[Groq] Model used: {model}")
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.warning(f"[Groq] Model {model} failed: {e}")

    return "❌ Groq: All models failed."


# ==========================================================
# GEMINI FREE API
# ==========================================================
def call_gemini(prompt: str, max_tokens: int = 8000):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        return "❌ GEMINI_API_KEY missing"

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-pro:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens},
    }

    try:
        res = requests.post(url, json=payload)
        out = res.json()

        return (
            out["candidates"][0]["content"]["parts"][0]["text"]
            if "candidates" in out
            else str(out)
        )

    except Exception as e:
        return f"❌ [Gemini Error] {e}"


# ==========================================================
# HUGGINGFACE FREE API (Mistral / Mixtral / Llama)
# ==========================================================
def call_huggingface(prompt: str, max_tokens: int = 4000, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    HF_API_KEY = os.getenv("HF_API_KEY")

    if not HF_API_KEY:
        return "❌ HF_API_KEY missing"

    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens, "temperature": 0.5},
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        out = r.json()

        # HF outputs can vary → normalize
        if isinstance(out, list) and "generated_text" in out[0]:
            return out[0]["generated_text"]

        if "error" in out:
            return f"❌ HF Error: {out['error']}"

        return str(out)

    except Exception as e:
        return f"❌ [HF Error] {e}"
