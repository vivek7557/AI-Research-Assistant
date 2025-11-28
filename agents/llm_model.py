"""
Universal LLM Wrapper
Supports:
- Groq
- Gemini
- HuggingFace
Provides one function:
    run_llm(system_prompt, user_prompt)
"""

import os
import requests
from groq import Groq
from loguru import logger


# ==========================================================
# CONFIG
# ==========================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# New stable Groq models (working as of Dec 2025)
GROQ_PRIMARY = "llama3-70b-8192"         # best
GROQ_FALLBACK = "gemma2-9b-it"           # stable small

MAX_TOKENS = 5000
TEMP = 0.4


# ==========================================================
# GROQ CLIENT
# ==========================================================
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None


# ==========================================================
# MAIN LLM ROUTER
# ==========================================================
def run_llm(system_prompt: str, user_prompt: str) -> str:
    """
    The ONLY function used by all agents.
    Tries:
        1) Groq primary model
        2) Groq fallback model
        3) Gemini
        4) HuggingFace
    Returns clean text.
    """

    # 1) ---------------- GROQ PRIMARY -------------------
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_PRIMARY,
                max_tokens=MAX_TOKENS,
                temperature=TEMP,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            logger.info(f"[LLM] Groq primary used: {GROQ_PRIMARY}")
            return response.choices[0].message["content"]

        except Exception as e:
            logger.warning(f"[Groq Primary Failed] {e}")

        # 2) -------------- GROQ FALLBACK -------------------
        try:
            response = groq_client.chat.completions.create(
                model=GROQ_FALLBACK,
                max_tokens=MAX_TOKENS,
                temperature=TEMP,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            logger.info(f"[LLM] Groq fallback used: {GROQ_FALLBACK}")
            return response.choices[0].message["content"]

        except Exception as e:
            logger.warning(f"[Groq Fallback Failed] {e}")

    # 3) ---------------- GEMINI FREE ---------------------
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

            data = {
                "contents": [{
                    "parts": [{"text": system_prompt + "\n" + user_prompt}]
                }],
                "generationConfig": {"maxOutputTokens": MAX_TOKENS}
            }

            r = requests.post(url, json=data)
            out = r.json()

            text = out["candidates"][0]["content"]["parts"][0]["text"]
            logger.info("[LLM] Gemini used")
            return text

        except Exception as e:
            logger.warning(f"[Gemini Failed] {e}")

    # 4) ---------------- HUGGINGFACE FREE ----------------
    if HF_API_KEY:
        try:
            model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}

            payload = {
                "inputs": system_prompt + "\n" + user_prompt,
                "parameters": {"max_new_tokens": 3000, "temperature": TEMP}
            }

            r = requests.post(url, json=payload, headers=headers)
            out = r.json()

            if isinstance(out, list) and "generated_text" in out[0]:
                logger.info("[LLM] HuggingFace used")
                return out[0]["generated_text"]

        except Exception as e:
            logger.warning(f"[HF Failed] {e}")

    # ---------------- TOTAL FAILURE ----------------
    return "[LLM ERROR] All models failed. Check API keys."
