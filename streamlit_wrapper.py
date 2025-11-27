import streamlit as st
from streamlit import session_state as state
import json
from ui.theme import load_theme

# Page imports
from pages.dashboard import dashboard_page
from pages.research import research_page
from pages.library import library_page
from pages.favorites import favorites_page
from pages.search import search_page
from pages.upload import upload_page


# ----------------------------- #
# PAGE CONFIG MUST COME FIRST
# ----------------------------- #
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Theme
load_theme()


# ----------------------------- #
# SIDEBAR BRANDING (FIXED)
# ----------------------------- #
st.sidebar.markdown(
    """
    <div class="sidebar-header">
        <div class="sidebar-title">AI Research Assistant</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ----------------------------- #
# THEME TOGGLE
# ----------------------------- #
if "theme" not in state:
    state.theme = "light"

def toggle_theme():
    state.theme = "dark" if state.theme == "light" else "light"

st.sidebar.button("🌗 Toggle Theme", on_click=toggle_theme)
st.sidebar.markdown(
    f"<div class='theme-info'>Active Theme: <b>{state.theme.title()}</b></div>",
    unsafe_allow_html=True
)


# ----------------------------- #
# NAVIGATION
# ----------------------------- #

if "page" not in state:
    state.page = "Dashboard"

state.page = st.sidebar.radio(
    "Navigation",
    list(PAGES.keys()),
    format_func=lambda x: PAGES[x],
)


# ----------------------------- #
# ROUTING
# ----------------------------- #
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

from components.chat_agent import chat_agent
chat_agent()
