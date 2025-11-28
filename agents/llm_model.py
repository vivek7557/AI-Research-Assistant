"""
Universal LLM Wrapper
Supports:
- Groq (FREE, stable models)
- Gemini (FREE)
- HuggingFace Inference API (FREE)

Function exposed:
    call_llm(prompt, max_tokens=8000)
"""

import os
import requests
from groq import Groq


# ==========================================================
# DEFAULT MODEL SELECTION
# ==========================================================
DEFAULT_PROVIDER = "groq"     # groq / gemini / hf


# ==========================================================
# GROQ (FREE) — STABLE MODELS AS OF 2025
# ==========================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

# SAFE MODELS (Not deprecated)
GROQ_PRIMARY = "llama-3.1-70b-versatile"
GROQ_FALLBACK = "llama-3.1-8b-instant"

def call_groq(prompt: str, max_tokens: int = 8000):
    """
    Groq LLM runner with fallback.
    """

    for model in [GROQ_PRIMARY, GROQ_FALLBACK]:
        try:
            res = groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.4
            )
            return res.choices[0].message["content"]

        except Exception as e:
            # Continue trying fallback models
            continue

    return "[Groq Error] All Groq models failed."


# ==========================================================
# GEMINI (FREE)
# ==========================================================
def call_gemini(prompt: str, max_tokens: int = 8000):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

    if not GEMINI_API_KEY:
        return "[Gemini Error] API key missing"

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-pro:generateContent?key=" + GEMINI_API_KEY
    )

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens}
    }

    try:
        r = requests.post(url, json=data)
        out = r.json()
        return out["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"[Gemini Error] {str(e)}"


# ==========================================================
# HUGGINGFACE (FREE)
# ==========================================================
def call_huggingface(prompt: str, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    HF_API_KEY = os.getenv("HF_API_KEY") or ""

    if not HF_API_KEY:
        return "[HF Error] API key missing"

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 2000,
            "temperature": 0.4,
        }
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        result = r.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return str(result)

    except Exception as e:
        return f"[HF Error] {str(e)}"


# ==========================================================
# MASTER WRAPPER FUNCTION
# ==========================================================
def call_llm(prompt: str, max_tokens: int = 8000) -> str:
    """
    Main unified LLM function.
    Chooses provider based on DEFAULT_PROVIDER.
    """

    if DEFAULT_PROVIDER == "groq":
        return call_groq(prompt, max_tokens)

    if DEFAULT_PROVIDER == "gemini":
        return call_gemini(prompt, max_tokens)

    if DEFAULT_PROVIDER == "hf":
        return call_huggingface(prompt)

    return "[LLM Error] Unknown model provider."
