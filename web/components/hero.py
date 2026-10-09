"""Hero section with metallic typography, action buttons, and verified system metrics."""

import textwrap
import streamlit as st


def render_hero() -> None:
    """Render the hero section with Vesper.ai aesthetic and Sign-Bridge content."""
    hero_html = textwrap.dedent(
        """
        <div class="hero-container animate-in-2">
            <div class="pill-badge">
                <span class="badge-dot"></span>
                <span>AI-Powered Sign Language Assistant</span>
            </div>
            
            <h1 class="hero-title">
                Breaking barriers with<br>
                <span class="hero-title-italic">Sign-Bridge.</span>
            </h1>
            
            <p class="hero-subtitle">
                Translate Indian Sign Language gestures into spoken English with real-time AI assistance.
            </p>
            
            <div class="btn-row">
                <a href="#simulator" class="vesper-btn-primary" aria-label="Explore the interactive demo">
                    <span>Explore the Demo</span>
                    <span class="btn-arrow" aria-hidden="true">&rarr;</span>
                </a>
                <a href="#how-it-works" class="vesper-btn-secondary" aria-label="Learn how SignBridge works">
                    <span>How It Works</span>
                </a>
            </div>
        </div>

        <div class="stats-ribbon animate-in-3">
            <div class="stat-card">
                <div class="stat-value">30 FPS</div>
                <div class="stat-label">Paced Capture Loop</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">126 Dim</div>
                <div class="stat-label">Hand Landmark Vector</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">5 Frames</div>
                <div class="stat-label">Stability Window (&ge;0.60)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">41 / 41</div>
                <div class="stat-label">Passing Pytest Tests</div>
            </div>
        </div>
        """
    ).strip()

    st.html(hero_html)
