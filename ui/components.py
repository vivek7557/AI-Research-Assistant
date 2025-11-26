from pathlib import Path
import json

# --- Metric card ---
def metric_card(icon, title, value):
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
    </div>
    """

# --- Recent item ---
def recent_item(title, sid):
    return f"""
    <div class="recent-item">
        <div class="recent-text">{title}</div>
        <a class="recent-btn" href='?session={sid}'>Open</a>
    </div>
    """

# --- Evaluation score bar ---
def eval_bar(name, score):
    nm = name.replace("_", " ").title()
    return f"""
    <div class="eval-row">
        <div class="eval-label">{nm}</div>
        <div class="eval-bar">
            <div class="eval-fill" style="width:{score}%"></div>
        </div>
        <div class="eval-score">{score}</div>
    </div>
    """

