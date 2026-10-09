"""Vocabulary explorer displaying the verified 20-word Indian Sign Language lexicon."""

import textwrap
import streamlit as st
from app.recognition.labels import VOCABULARY


def render_vocabulary() -> None:
    """Render categorized dictionary of supported ISL vocabulary tokens."""
    header_html = textwrap.dedent(
        """
        <div id="vocabulary" class="section-header">
            <span class="section-tag">SUPPORTED LEXICON</span>
            <h2 class="section-title">Verified 20-Word ISL Vocabulary</h2>
            <p class="section-desc">
                The SignBridge MVP is trained on 20 critical everyday communication signs. 
                Below is the complete set of recognized gesture classes.
            </p>
        </div>
        """
    ).strip()
    st.html(header_html)

    categories = {
        "🤝 Greetings & Politeness": ["hello", "thank_you", "please", "sorry"],
        "💧 Essential Needs": ["water", "food", "bathroom", "help"],
        "✅ Responses & States": ["yes", "no", "good", "bad", "fine"],
        "❓ Questions & Identity": ["what", "where", "when", "who", "how", "name", "i_am"],
    }

    cols = st.columns(len(categories))
    for col, (cat_name, words) in zip(cols, categories.items()):
        with col:
            chips = "".join([f'<div class="vocab-chip" style="margin-bottom: 8px;">{w.replace("_", " ").title()}</div>' for w in words])
            cat_html = textwrap.dedent(
                f"""
                <div class="vesper-card" style="padding: 20px 16px;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #A0A0AD; margin-bottom: 14px; text-transform: uppercase;">
                        {cat_name}
                    </div>
                    <div>
                        {chips}
                    </div>
                </div>
                """
            ).strip()
            st.html(cat_html)

    meta_html = textwrap.dedent(
        f"""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.85rem; color: #5E5E68;">
            Total Classes: <b>{len(VOCABULARY)}</b> | Feature Representation: <b>30 frames &times; 126 coordinates</b>
        </div>
        """
    ).strip()
    st.html(meta_html)
