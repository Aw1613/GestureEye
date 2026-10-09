"""Floating silver liquid-metal navbar component."""

import textwrap
import streamlit as st


def render_navbar() -> None:
    """Render slim glossy silver pill navigation bar with brand, links, and status."""
    navbar_html = textwrap.dedent(
        """
        <header class="liquid-navbar-wrapper animate-in-1" role="banner">
            <nav class="liquid-navbar" aria-label="Main Navigation">
                <a href="#" class="nav-brand" aria-label="SignBridge Home">
                    <span class="nav-brand-logo" aria-hidden="true">🌉</span>
                    <span class="nav-brand-text">SignBridge</span>
                </a>
                <div class="nav-links">
                    <a href="#how-it-works" class="nav-link">How it Works</a>
                    <a href="#architecture" class="nav-link">Architecture</a>
                    <a href="#vocabulary" class="nav-link">Vocabulary</a>
                    <a href="#simulator" class="nav-link">Demo</a>
                    <a href="#desktop-run" class="nav-link">Desktop App</a>
                </div>
                <div class="nav-right">
                    <a href="#simulator" class="nav-pill-cta" aria-label="Jump to interactive demo">
                        <span>Try Demo</span>
                    </a>
                </div>
            </nav>
        </header>
        """
    ).strip()

    st.html(navbar_html)
