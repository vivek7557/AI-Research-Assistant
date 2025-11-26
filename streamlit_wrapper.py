import streamlit as st
from streamlit import session_state as state
import os
import json
from pathlib import Path
from ui.theme import load_theme
load_theme()


# Page imports
from pages.dashboard import dashboard_page
from pages.research import research_page
from pages.library import library_page
from pages.favorites import favorites_page
from pages.search import search_page
from pages.upload import upload_page

# Load Theme CSS
with open("theme.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# INITIAL CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# SIDEBAR BRANDING
# -----------------------------
st.markdown(
    """
    <div class="sidebar-header">
        <div class="sidebar-title">AI Research Assistant</div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# THEME TOGGLE
# -----------------------------
if "theme" not in state:
    state.theme = "light"

def toggle_theme():
    state.theme = "dark" if state.theme == "light" else "light"

st.sidebar.markdown("---")

if st.sidebar.button("🌗 Toggle Theme"):
    toggle_theme()

st.sidebar.markdown(
    f"<div class='theme-info'>Active Theme: <b>{state.theme.title()}</b></div>",
    unsafe_allow_html=True
)

# Add theme class to body
st.markdown(
    f"""
    <script>
    document.querySelector('body').setAttribute('data-theme', '{state.theme}');
    </script>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
PAGES = {
    "Dashboard": "📊 Dashboard",
    "Research": "🧪 Research",
    "Library": "📚 Library",
    "Favorites": "⭐ Favorites",
    "Search": "🔍 Search",
    "Upload": "📤 Upload Paper"
}

if "page" not in state:
    state.page = "Dashboard"

selected_page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    index=list(PAGES.keys()).index(state.page),
    format_func=lambda x: PAGES[x],
)

state.page = selected_page

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div class='sidebar-footer'>v2.0 • Multi-Agent Research System</div>",
    unsafe_allow_html=True
)

# -----------------------------
# PAGE ROUTING LOGIC
# -----------------------------
def router():
    if state.page == "Dashboard":
        dashboard_page()
    elif state.page == "Research":
        research_page()
    elif state.page == "Library":
        library_page()
    elif state.page == "Favorites":
        favorites_page()
    elif state.page == "Search":
        search_page()
    elif state.page == "Upload":
        upload_page()

router()
