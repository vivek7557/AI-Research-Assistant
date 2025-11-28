from groq import Groq
import os
from loguru import logger

PRIMARY_MODEL = "llama-3.1-70b-versatile"
FALLBACK_MODEL = "llama-3.3-8b-instant"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_llm(system_prompt, user_prompt, max_tokens=5000):
    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",    "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.4
            )
            return response.choices[0].message["content"]

        except Exception as e:
            logger.warning(f"[Groq Failed] {model}: {e}")

    logger.error("[LLM ERROR] All models failed")
    return "ERROR: LLM unavailable."
