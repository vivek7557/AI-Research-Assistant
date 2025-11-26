import streamlit as st
from pathlib import Path
import json
import os

def dashboard_page():
    st.markdown("<h1 class='page-title'>Dashboard</h1>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(metric_card("📚", "Total Papers", count_json_files("outputs")), unsafe_allow_html=True)
    col2.markdown(metric_card("🧠", "AI Summaries", count_json_files("summaries")), unsafe_allow_html=True)
    col3.markdown(metric_card("⭐", "Favorites", count_json_files("favorites")), unsafe_allow_html=True)
    col4.markdown(metric_card("📅", "This Month", "12"), unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Recent Papers</div>", unsafe_allow_html=True)

    output_dir = Path("outputs")

    if not output_dir.exists():
        st.info("No research sessions yet.")
        return

    files = sorted(output_dir.glob("*.json"), key=os.path.getmtime, reverse=True)[:5]

    for f in files:
        try:
            data = json.loads(f.read_text())
            q = data.get("query", "Untitled Research")
            st.markdown(recent_item(q, f.stem), unsafe_allow_html=True)
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
    p = Path(folder)
    return len(list(p.glob("*.json"))) if p.exists() else 0

