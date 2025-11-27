"""
Brochure Generator Agent
Creates a marketing-style brochure using LLM.
Outputs Markdown + auto-generated PDF.
"""

import os
from fpdf import FPDF
from groq import Groq


class BrochureAgent:

    def __init__(self):
        # Load Groq client (free LLMs)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, title: str, sections: dict, sources: list):
        """
        Create a brochure-style PDF + generate text using LLM.
        """

        # -------------------------------------------------------------
        # 1. LLM: Turn sections into brochure-style narrative
        # -------------------------------------------------------------
        prompt = f"""
        Create a clean, simple brochure-style content for:

        TITLE: {title}

        SECTIONS:
        {sections}

        Make it readable, structured, and friendly.
        """

        try:
            llm = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200
            )
            brochure_text = llm.choices[0].message["content"]
        except Exception:
            brochure_text = "Brochure content unavailable. PDF contains section summaries only."

        # -------------------------------------------------------------
        # 2. Generate PDF using FPDF
        # -------------------------------------------------------------
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()

        # --- Title ---
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 12, title, ln=True, align="C")
        pdf.ln(6)

        # --- LLM Generated Text ---
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 6, brochure_text)
        pdf.ln(6)

        # --- Section Details ---
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Sections", ln=True)
        pdf.set_font("Arial", size=12)

        for section_title, content in sections.items():
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 8, section_title, ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 6, content)
            pdf.ln(3)

        # --- Sources ---
        if sources:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, "Sources", ln=True)

            pdf.set_font("Arial", size=10)
            for src in sources:
                line = f"- {src.get('title', 'Unknown')} ({src.get('url', '')})"
                pdf.multi_cell(0, 5, line)

        # --- PDF output ---
        pdf_bytes = pdf.output(dest="S").encode("latin1")

        return {
            "brochure_title": title,
            "brochure_text": brochure_text,
            "pdf_bytes": pdf_bytes
        }
