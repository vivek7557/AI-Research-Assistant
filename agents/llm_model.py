"""
Universal LLM Wrapper
Supports:
- Groq (FREE)
- Gemini (FREE)
- HuggingFace Inference API (FREE)

Function exposed:
    call_llm(prompt, max_tokens=8000)
"""

import os
import requests


# ==========================================================
# SELECT DEFAULT FREE MODEL HERE
# ==========================================================
DEFAULT_MODEL = "groq"     # groq / gemini / hf


# ==========================================================
# MAIN CALL FUNCTION
# ==========================================================
def call_llm(prompt: str, max_tokens: int = 8000) -> str:
    model = DEFAULT_MODEL

    if model == "groq":
        return call_groq(prompt, max_tokens)

    elif model == "gemini":
        return call_gemini(prompt, max_tokens)

    elif model == "hf":
        return call_huggingface(prompt)

    else:
        return "Error: Unknown LLM model selected."


# ==========================================================
# GROQ (FREE) — llama3-70b / mixtral-8x7b
# ==========================================================
def call_groq(prompt: str, max_tokens: int = 8000):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY") or ""

    if not GROQ_API_KEY:
        return "[ERROR] GROQ_API_KEY missing"

    url = "https://api.groq.com/openai/v1/chat/completions"

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    try:
        r = requests.post(url, json=payload, headers=headers)
        out = r.json()
        return out["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[Groq Error] {str(e)}"


# ==========================================================
# GEMINI (FREE)
# ==========================================================
def call_gemini(prompt: str, max_tokens: int = 8000):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""

    if not GEMINI_API_KEY:
        return "[ERROR] GEMINI_API_KEY missing"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens}
    }

    try:
        res = requests.post(url, json=data)
        out = res.json()
        return out["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"[Gemini Error] {str(e)}"


# ==========================================================
# HuggingFace FREE API — Mixtral / Llama / Mistral
# ==========================================================
def call_huggingface(prompt: str, model="mistralai/Mixtral-8x7B-Instruct-v0.1"):
    HF_API_KEY = os.getenv("HF_API_KEY") or ""

    if not HF_API_KEY:
        return "[ERROR] HF_API_KEY missing"

    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 4000, "temperature": 0.4}
    }

    try:
        r = requests.post(url, json=payload, headers=headers)
        out = r.json()

        if isinstance(out, list) and "generated_text" in out[0]:
            return out[0]["generated_text"]

        return str(out)

    except Exception as e:
        return f"[HF Error] {str(e)}"
