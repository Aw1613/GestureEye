"""SignBridge — Real-Time Indian Sign Language Assistant.

Web Landing Page & Interactive Showcase (Vesper-Inspired Aesthetic).
Deployable on Streamlit Community Cloud.
"""

import os
import sys
import importlib

# Ensure repository root is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

import web.styles
import web.components.navbar
import web.components.canvas_wave
import web.components.hero
import web.components.overview
import web.components.pipeline
import web.components.vocabulary
import web.components.simulator
import web.components.desktop_guide
import web.components.footer

# Force module reload on every rerun to prevent stale in-memory imports
importlib.reload(web.styles)
importlib.reload(web.components.navbar)
importlib.reload(web.components.canvas_wave)
importlib.reload(web.components.hero)
importlib.reload(web.components.overview)
importlib.reload(web.components.pipeline)
importlib.reload(web.components.vocabulary)
importlib.reload(web.components.simulator)
importlib.reload(web.components.desktop_guide)
importlib.reload(web.components.footer)

from web.styles import get_vesper_css
from web.components.navbar import render_navbar
from web.components.canvas_wave import render_canvas_wave
from web.components.hero import render_hero
from web.components.overview import render_overview
from web.components.pipeline import render_pipeline
from web.components.vocabulary import render_vocabulary
from web.components.simulator import render_simulator
from web.components.desktop_guide import render_desktop_guide
from web.components.footer import render_footer


def main() -> None:
    """Main Streamlit execution entrypoint."""
    st.set_page_config(
        page_title="SignBridge — Real-Time ISL Assistant",
        page_icon="🌉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Inject Vesper-inspired styling and animations via st.html
    st.html(get_vesper_css())

    # Render floating liquid-metal navbar
    render_navbar()

    # Render flowing silver-white particle wave background
    render_canvas_wave()

    # Render hero section
    render_hero()

    # Render project-specific content sections
    render_overview()
    render_pipeline()
    render_vocabulary()
    render_simulator()
    render_desktop_guide()
    render_footer()


if __name__ == "__main__":
    main()
