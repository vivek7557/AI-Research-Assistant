"""
Brochure Generator Agent
Creates a marketing-style brochure using LLM.
Outputs Markdown + auto-generated PDF.
"""

from fpdf import FPDF
from openai import OpenAI


class BrochureGeneratorAgent:

    def __init__(self):
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_brochure_text(self, title, content):
        prompt = f"""
        Create a modern 1-page product brochure.

        Title: {title}

        Key Research Insights:
        {content}

        Structure:
        - Hero title
        - Tagline
        - 3 highlight sections
        - Key facts
        - CTA (Call To Action)
        - Minimal marketing tone
        """

        response = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900
        )

        return response.choices[0].message["content"]

    def generate_pdf(self, brochure_text, file_path="brochure.pdf"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", size=12)

        for line in brochure_text.split("\n"):
            pdf.multi_cell(0, 8, line)

        pdf.output(file_path)
        return file_path
