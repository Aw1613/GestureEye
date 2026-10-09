"""Footer component for the SignBridge landing page."""

import textwrap
import streamlit as st


def render_footer() -> None:
    """Render footer with repository links, license, and team attribution."""
    footer_html = textwrap.dedent(
        """
        <div class="footer-container">
            <div class="footer-links">
                <a href="https://github.com/ujjwal-mahajan/Sign-Bridge" target="_blank">GitHub Repository</a>
                <a href="#how-it-works">Pipeline Architecture</a>
                <a href="#vocabulary">ISL Vocabulary</a>
                <a href="#simulator">Sentence Simulator</a>
                <a href="#desktop-run">Desktop Setup</a>
            </div>
            <div>
                SignBridge &bull; Indian Sign Language Real-Time Communication Assistant<br>
                Built under the MIT License &bull; Verified against 41 Automated Tests
            </div>
        </div>
        """
    ).strip()
    st.html(footer_html)
