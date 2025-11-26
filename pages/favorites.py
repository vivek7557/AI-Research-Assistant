import streamlit as st
from pathlib import Path
import json
from ui.theme import load_theme
load_theme()


FAV_FILE = Path("favorites/fav.json")

def favorites_page():
    st.markdown("<h1 class='page-title'>Favorites</h1>", unsafe_allow_html=True)

    if not FAV_FILE.exists():
        st.info("No favorites marked yet.")
        return

    with open(FAV_FILE, "r") as f:
        favs = json.load(f)

    if not favs:
        st.info("You have no favorite items.")
        return

    for item in favs:
        st.markdown(f"⭐ **{item['title']}**")

