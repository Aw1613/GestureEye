"""Desktop application execution guide and keyboard controls reference."""

import textwrap
import streamlit as st


def render_desktop_guide() -> None:
    """Render terminal commands, controls, and rehearsal instructions for the desktop app."""
    header_html = textwrap.dedent(
        """
        <div id="desktop-run" class="section-header">
            <span class="section-tag">LIVE DEPLOYMENT</span>
            <h2 class="section-title">Running the Live Desktop App</h2>
            <p class="section-desc">
                For the full 30 FPS OpenCV experience with real-time MediaPipe hand tracking and local Text-to-Speech audio, 
                run the desktop pipeline directly on your machine.
            </p>
        </div>
        """
    ).strip()
    st.html(header_html)

    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        cli_html = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">DESKTOP CLI COMMANDS</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #FFFFFF; margin-bottom: 12px;">
                    1. Launch with Physical Webcam:
                </div>
                <div class="vesper-terminal">
                    <div class="terminal-header">
                        <span class="terminal-dot dot-red"></span>
                        <span class="terminal-dot dot-yellow"></span>
                        <span class="terminal-dot dot-green"></span>
                        <span style="font-size: 0.72rem; color: #5E5E68; margin-left: 8px;">PowerShell / Terminal</span>
                    </div>
                    python scripts/run_app.py
                </div>

                <div style="font-size: 0.95rem; font-weight: 600; color: #FFFFFF; margin: 18px 0 12px 0;">
                    2. Presentation / Synthetic Stream (No Webcam Required):
                </div>
                <div class="vesper-terminal">
                    <div class="terminal-header">
                        <span class="terminal-dot dot-red"></span>
                        <span class="terminal-dot dot-yellow"></span>
                        <span class="terminal-dot dot-green"></span>
                        <span style="font-size: 0.72rem; color: #5E5E68; margin-left: 8px;">Presentation Mode</span>
                    </div>
                    python scripts/run_app.py --mock
                </div>

                <div style="font-size: 0.95rem; font-weight: 600; color: #FFFFFF; margin: 18px 0 12px 0;">
                    3. Run Automated 41-Test Suite:
                </div>
                <div class="vesper-terminal">
                    <div class="terminal-header">
                        <span class="terminal-dot dot-red"></span>
                        <span class="terminal-dot dot-yellow"></span>
                        <span class="terminal-dot dot-green"></span>
                        <span style="font-size: 0.72rem; color: #5E5E68; margin-left: 8px;">Pytest Suite</span>
                    </div>
                    python -m pytest tests/ -v
                </div>
            </div>
            """
        ).strip()
        st.html(cli_html)

    with col2:
        shortcuts_html = textwrap.dedent(
            """
            <div class="vesper-card">
                <div class="card-agent-badge">INTERACTIVE SHORTCUTS</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #FFFFFF; margin-bottom: 12px;">
                    In-App Real-Time Keyboard Controls:
                </div>
                
                <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem; color: #E6E6EF;">
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[S]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Speak smoothed sentence via async TTS (&lt;0.001s non-blocking)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[C]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Clear word buffer, sentence, and stability filter</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[Backspace]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Undo last accepted word and recalculate grammar</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[M]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Toggle dynamically between live webcam and mock feed</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[1] – [5]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Inject 5-frame stable signs: 1:hello, 2:thank_you, 3:please, 4:water, 5:help</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 6px; font-weight: 700; color: #FFFFFF;">[Q] / [ESC]</td>
                        <td style="padding: 10px 6px; color: #90909A;">Clean shutdown of background threads and window</td>
                    </tr>
                </table>
            </div>
            """
        ).strip()
        st.html(shortcuts_html)
