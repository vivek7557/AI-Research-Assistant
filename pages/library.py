import streamlit as st
from pathlib import Path
import json
import os

def library_page():
    st.markdown("<h1 class='page-title'>Library</h1>", unsafe_allow_html=True)

    output_dir = Path("outputs")

    if not output_dir.exists():
        st.info("No research papers yet.")
        return

    files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)

    for f in files:
        try:
            with open(f, "r") as fd:
                data = json.load(fd)
            query = data.get("query", "Untitled Research")

            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{query}**")

            if col2.button("Open", key=f"open_{f.stem}"):
                st.json(data)

        except:
            pass

