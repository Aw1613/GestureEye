"""Unit and integration test verifying the Streamlit landing page rendering."""

import os
import sys
import pytest
from streamlit.testing.v1 import AppTest


def test_landing_page_renders_html_not_code_blocks():
    """Verify that streamlit_app.py renders the hero section as HTML, not as literal code."""
    app_path = os.path.abspath("streamlit_app.py")
    at = AppTest.from_file(app_path)
    at.run()

    # 1. App must run with zero exceptions
    assert not at.exception, f"Streamlit app raised an exception: {at.exception}"

    # 2. Hero must NOT be rendered inside any st.code block
    code_blocks = [c.value for c in at.code]
    for cb in code_blocks:
        assert "hero-title" not in cb, "hero-title was incorrectly found inside an st.code block!"
        assert "<h1" not in cb, "<h1 tag was incorrectly found inside an st.code block!"

    # 3. Hero must NOT be rendered inside any markdown element as escaped source code
    for md in at.markdown:
        md_text = md.value
        assert "<h1 class=\"hero-title\">" not in md_text, (
            "hero-title was passed to st.markdown as unrendered raw text!"
        )

    # 4. Extract all rendered Html bodies
    html_elements = []
    for el in at.main:
        p = getattr(el, "proto", None)
        if p and type(p).__name__ == "Html":
            html_elements.append(p.body)

    # 5. Verify headline, badge, and particle canvas wave
    all_html = " ".join(html_elements)
    assert "vesper-particle-canvas" in all_html, "Particle wave canvas was not rendered!"
    assert "AI-Powered Sign Language Assistant" in all_html, "Badge text was not found!"
    assert "Breaking barriers with" in all_html, "Headline text was not found!"
    assert "Sign-Bridge." in all_html, "Italic title Sign-Bridge was not found!"
    assert "Explore the Demo" in all_html, "Primary CTA was not found!"
    assert "How It Works" in all_html, "Secondary CTA was not found!"
