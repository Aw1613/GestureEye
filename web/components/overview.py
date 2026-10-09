"""System overview and operational flow section."""

import textwrap
import streamlit as st


def render_overview() -> None:
    """Render the 'How It Works' section and scope disclaimer."""
    header_html = textwrap.dedent(
        """
        <div id="how-it-works" class="section-header">
            <span class="section-tag">ENGINEERING PIPELINE</span>
            <h2 class="section-title">How SignBridge Works</h2>
            <p class="section-desc">
                From raw video capture to synthesized speech, every frame passes through 
                a deterministic, decoupled data pipeline designed for sub-millisecond thread safety.
            </p>
        </div>
        """
    ).strip()
    st.html(header_html)

    col1, col2, col3 = st.columns(3)

    with col1:
        card1_html = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">STEP 01 — CAPTURE & KEYPOINTS</div>
                <div class="card-title">Hand Landmark Extraction</div>
                <div class="card-text">
                    Threaded video acquisition isolates camera sensor latency. 
                    MediaPipe Hand tracking extracts 21 three-dimensional landmarks per hand, 
                    normalized and packaged into a 126-dimensional feature vector.
                </div>
                <div class="card-meta">Output: (30, 126) Sliding Window</div>
            </div>
            """
        ).strip()
        st.html(card1_html)

    with col2:
        card2_html = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">STEP 02 — TEMPORAL ML</div>
                <div class="card-title">Temporal Sequence Inference</div>
                <div class="card-text">
                    A PyTorch 2-layer LSTM neural network analyzes temporal motion dynamics 
                    over rolling 30-frame sequence windows, generating probability distributions 
                    across the 20-sign Indian Sign Language vocabulary.
                </div>
                <div class="card-meta">Contract C: Label + Confidence</div>
            </div>
            """
        ).strip()
        st.html(card2_html)

    with col3:
        card3_html = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">STEP 03 — SMOOTHING & AUDIO</div>
                <div class="card-title">Stability & Speech Output</div>
                <div class="card-text">
                    Temporal stability filtering eliminates transition noise by requiring 5 agreeing 
                    frames (&ge;0.60 conf). SentenceBuilder formats tokens into natural English, 
                    queued to a non-blocking background TTS daemon (<0.001s).
                </div>
                <div class="card-meta">Contract E & F: Smoothed Text + Audio</div>
            </div>
            """
        ).strip()
        st.html(card3_html)

    # Engineering Scope Disclaimer
    disclaimer_html = textwrap.dedent(
        """
        <div style="margin-top: 2rem; padding: 18px 24px; background: rgba(255, 255, 255, 0.02); 
                    border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; text-align: left;">
            <div style="display: flex; align-items: center; gap: 10px; font-weight: 600; color: #FFFFFF; font-size: 0.92rem; margin-bottom: 6px;">
                <span>ℹ️</span>
                <span>Explicit Engineering Scope (MVP)</span>
            </div>
            <div style="font-size: 0.88rem; color: #90909A; line-height: 1.5;">
                SignBridge is designed as a focused Minimum Viable Product (MVP) supporting a defined 20-word vocabulary of 
                frequently used Indian Sign Language gestures. It does not claim universal unconstrained sign-language 
                translation, but rather demonstrates a production-grade, low-latency foundation for real-time assistive communication.
            </div>
        </div>
        """
    ).strip()
    st.html(disclaimer_html)
