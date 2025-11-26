import streamlit as st
import PyPDF2
import json
from pathlib import Path
from ui.theme import load_theme
load_theme()

def upload_page():
    st.markdown("<h1 class='page-title'>Upload Paper</h1>", unsafe_allow_html=True)

    file = st.file_uploader("Upload PDF", type=["pdf"])

    if file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n\n"

        st.text_area("Extracted Text", text, height=300)

        if st.button("Save to Library"):
            save_path = Path("uploads")
            save_path.mkdir(exist_ok=True)
            filename = save_path / f"{file.name}.txt"
            filename.write_text(text)
            st.success("Saved!")

