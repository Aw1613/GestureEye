"""Four-agent architecture specification and data contracts section."""

import textwrap
import streamlit as st


def render_pipeline() -> None:
    """Render the 4-Agent modular architecture cards with verified contracts."""
    header_html = textwrap.dedent(
        """
        <div id="architecture" class="section-header">
            <span class="section-tag">SYSTEM SPECIFICATION</span>
            <h2 class="section-title">The 4-Agent Modular Architecture</h2>
            <p class="section-desc">
                SignBridge is built by four specialized engineering domains, decoupled by strict data contracts 
                to eliminate race conditions and enable independent validation.
            </p>
        </div>
        """
    ).strip()
    st.html(header_html)

    col1, col2 = st.columns(2)

    with col1:
        card_a1 = textwrap.dedent(
            """
            <div class="vesper-card" style="margin-bottom: 20px;">
                <div class="card-agent-badge">AGENT 1 — INPUT & KEYPOINTS</div>
                <div class="card-title">Camera & Landmark Pipeline</div>
                <div class="card-text">
                    <b>Ownership:</b> Threaded video capture (DirectShow on Windows), MediaPipe Hand landmark 
                    extraction, coordinate normalization relative to wrist reference, and rolling sequence buffer.
                </div>
                <div class="card-meta">
                    <b>Contract B Output:</b> Normalized Array shape <code>(30, 126)</code><br>
                    <b>Modules:</b> <code>app/capture/</code>, <code>app/keypoints/</code>
                </div>
            </div>
            """
        ).strip()
        st.html(card_a1)

        card_a3 = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">AGENT 3 — SENTENCE & SPEECH</div>
                <div class="card-title">Temporal Filter & TTS Engine</div>
                <div class="card-text">
                    <b>Ownership:</b> Temporal stability filter (requiring 5 consecutive agreeing frames &ge;0.60 conf), 
                    duplicate suppression, sentence smoothing heuristics, and asynchronous non-blocking TTS daemon.
                </div>
                <div class="card-meta">
                    <b>Contracts D & E:</b> <code>{"words": [...], "text": "..."}</code><br>
                    <b>Contract F:</b> Audio queued in &lt;0.001s without blocking video<br>
                    <b>Modules:</b> <code>app/sentence/</code>, <code>app/tts/</code>
                </div>
            </div>
            """
        ).strip()
        st.html(card_a3)

    with col2:
        card_a2 = textwrap.dedent(
            """
            <div class="vesper-card" style="margin-bottom: 20px;">
                <div class="card-agent-badge">AGENT 2 — DATASET & MODEL</div>
                <div class="card-title">Temporal ML Classification</div>
                <div class="card-text">
                    <b>Ownership:</b> Vocabulary definition (20 classes), PyTorch 2-layer LSTM temporal network, 
                    sequence tensor formatting, model weights persistence, and inference wrapper.
                </div>
                <div class="card-meta">
                    <b>Contract C Output:</b> <code>{"label": "water", "confidence": 0.91}</code><br>
                    <b>Modules:</b> <code>app/recognition/</code>, <code>training/</code>
                </div>
            </div>
            """
        ).strip()
        st.html(card_a2)

        card_a4 = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">AGENT 4 — UI & INTEGRATION</div>
                <div class="card-title">Live HUD & System Integration</div>
                <div class="card-text">
                    <b>Ownership:</b> Real-time 1000x680 OpenCV composite HUD overlay, Contract G state assembly, 
                    keyboard controls (undo, speak, clear, mock toggle), and end-to-end testing.
                </div>
                <div class="card-meta">
                    <b>Contract G Output:</b> Unified <code>ui_state</code> payload<br>
                    <b>Modules:</b> <code>app/ui/overlay.py</code>, <code>app/ui/app.py</code>
                </div>
            </div>
            """
        ).strip()
        st.html(card_a4)
