"""
Brochure Generator Agent
Creates a marketing-style brochure using LLM.
Outputs Markdown + auto-generated PDF.
"""

from fpdf import FPDF
from openai import OpenAI


from fpdf import FPDF

class BrochureAgent:

    def generate(self, title: str, sections: dict, sources: list):
        """
        Create a simple brochure-style PDF.
        """

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(5)

        # Sections
        pdf.set_font("Arial", size=12)

        for section_title, content in sections.items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 8, section_title, ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 6, content)
            pdf.ln(4)

        # Sources
        if sources:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 8, "Sources", ln=True)
            pdf.set_font("Arial", size=11)

            for src in sources:
                txt = f"- {src.get('title', 'Unknown')} ({src.get('url', '')})"
                pdf.multi_cell(0, 6, txt)

        # Export as bytes
        pdf_bytes = pdf.output(dest="S").encode("latin1")

        return {
            "brochure_title": title,
            "pdf_bytes": pdf_bytes
        }

