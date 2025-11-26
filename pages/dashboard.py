import streamlit as st
from pathlib import Path
import json
import os

def dashboard_page():
    st.markdown("<h1 class='page-title'>Dashboard</h1>", unsafe_allow_html=True)

    # ---- METRIC CARDS ----
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(metric_card("📚", "Total Papers", count_json_files("outputs")))
    col2.markdown(metric_card("🧠", "AI Summaries", count_json_files("summaries")))
    col3.markdown(metric_card("⭐", "Favorites", count_json_files("favorites")))
    col4.markdown(metric_card("📅", "This Month", "12"))

    st.markdown("<div class='section-title'>Recent Papers</div>", unsafe_allow_html=True)

    # ---- RECENT ACTIVITY LIST ----
    output_dir = Path("outputs")

    if not output_dir.exists():
        st.info("No research sessions yet.")
        return

    files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:5]

    for f in files:
        try:
            with open(f, "r") as fd:
                data = json.load(fd)
                q = data.get("query", "Untitled Research")
                st.markdown(recent_item(q, f.stem))
        except:
            pass


def metric_card(icon, title, value):
    return f"""
    <div class='metric-card'>
        <div class='metric-icon'>{icon}</div>
        <div class='metric-content'>
            <div class='metric-title'>{title}</div>
            <div class='metric-value'>{value}</div>
        </div>
    </div>
    """


def recent_item(text, sid):
    return f"""
    <div class='recent-item'>
        <div class='recent-text'>{text}</div>
        <a class='recent-btn' href='?session={sid}'>Open</a>
    </div>
    """


def count_json_files(folder):
    f = Path(folder)
    if not f.exists():
        return 0
    return len(list(f.glob("*.json")))

