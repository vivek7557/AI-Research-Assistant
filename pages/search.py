import streamlit as st
from pathlib import Path
import json

def search_page():
    st.markdown("<h1 class='page-title'>Search</h1>", unsafe_allow_html=True)

    keyword = st.text_input("Search keyword")
    if not keyword:
        return

    output_dir = Path("outputs")
    if not output_dir.exists():
        st.info("No files to search.")
        return

    results = []
    for f in output_dir.glob("*.json"):
        with open(f) as fd:
            data = json.load(fd)
            if keyword.lower() in json.dumps(data).lower():
                results.append((f.stem, data.get("query", "Untitled")))

    st.markdown(f"### {len(results)} Results found")

    for sid, title in results:
        st.markdown(f"**{title}** — `{sid}`")

