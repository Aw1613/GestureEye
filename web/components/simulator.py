"""Interactive in-browser sentence smoothing simulator using the production SentenceBuilder."""

import json
import textwrap
import streamlit as st
from app.sentence.builder import SentenceBuilder
from app.recognition.labels import VOCABULARY


def get_builder() -> SentenceBuilder:
    """Retrieve or initialize SentenceBuilder in Streamlit session state."""
    if "sentence_builder" not in st.session_state:
        st.session_state.sentence_builder = SentenceBuilder(suppress_consecutive_duplicates=True)
    return st.session_state.sentence_builder


def render_simulator() -> None:
    """Render interactive sentence construction demo powered by Agent 3 logic."""
    header_html = textwrap.dedent(
        """
        <div id="simulator" class="section-header">
            <span class="section-tag">LIVE AGENT 3 LOGIC</span>
            <h2 class="section-title">Interactive Sentence Simulator</h2>
            <p class="section-desc">
                Test the actual Agent 3 heuristic smoothing rules in real-time. 
                Discrete signs are assembled into grammatically natural English phrases with duplicate suppression.
            </p>
        </div>
        """
    ).strip()
    st.html(header_html)

    builder = get_builder()

    with st.container(border=True):
        words_in_buffer = builder.get_words()
        current_sentence = builder.get_sentence()
        buffer_count = len(words_in_buffer)

        status_html = textwrap.dedent(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 0.85rem; font-weight: 600; color: #90909A; text-transform: uppercase; letter-spacing: 0.05em;">
                    Accepted Word Buffer ({buffer_count} Tokens)
                </div>
                <div style="font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; color: #00F59B;">
                    ● Contract E Active
                </div>
            </div>
            """
        ).strip()
        st.html(status_html)

        # Word Buffer Chips
        if words_in_buffer:
            chips_html = "".join([f'<span class="token-tag">#{i+1} {w}</span>' for i, w in enumerate(words_in_buffer)])
        else:
            chips_html = '<span style="color: #5E5E68; font-size: 0.86rem; font-style: italic;">Buffer empty. Add signs below to start building a sentence...</span>'

        buffer_row_html = textwrap.dedent(f'<div class="sim-buffer-row">{chips_html}</div>').strip()
        st.html(buffer_row_html)

        # Primary Sentence Display
        display_text = current_sentence if current_sentence else "Awaiting sign events..."
        display_html = textwrap.dedent(
            f"""
            <div style="text-align: left; font-size: 0.8rem; font-weight: 600; color: #A0A0AD; margin-bottom: 4px;">
                SMOOTHED SENTENCE OUTPUT:
            </div>
            <div class="sim-display">
                <span>&ldquo;{display_text}&rdquo;</span>
            </div>
            """
        ).strip()
        st.html(display_html)

        # Action Controls: Undo and Clear
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 2])
        with col_ctrl1:
            if st.button("⌫ Undo Last Word", use_container_width=True):
                builder.remove_last_word()
                st.rerun()

        with col_ctrl2:
            if st.button("🗑️ Clear Buffer", use_container_width=True):
                builder.clear()
                st.rerun()

        with col_ctrl3:
            preset_choice = st.selectbox(
                "Load Demo Preset Sequence:",
                [
                    "-- Choose Preset --",
                    "Preset A: hello → water → please",
                    "Preset B: hello → thank_you",
                    "Preset C: help → bathroom → where",
                    "Preset D: name → what",
                ],
                label_visibility="collapsed",
            )
            if preset_choice.startswith("Preset A"):
                builder.clear()
                builder.add_word("hello")
                builder.add_word("water")
                builder.add_word("please")
                st.rerun()
            elif preset_choice.startswith("Preset B"):
                builder.clear()
                builder.add_word("hello")
                builder.add_word("thank_you")
                st.rerun()
            elif preset_choice.startswith("Preset C"):
                builder.clear()
                builder.add_word("help")
                builder.add_word("bathroom")
                builder.add_word("where")
                st.rerun()
            elif preset_choice.startswith("Preset D"):
                builder.clear()
                builder.add_word("name")
                builder.add_word("what")
                st.rerun()

        divider_html = textwrap.dedent("<hr style='border-color: rgba(255, 255, 255, 0.08); margin: 20px 0;'>").strip()
        st.html(divider_html)

        prompt_html = textwrap.dedent(
            """
            <div style="font-size: 0.85rem; font-weight: 600; color: #90909A; text-transform: uppercase; margin-bottom: 10px;">
                Tap to Inject Sign Event into Pipeline:
            </div>
            """
        ).strip()
        st.html(prompt_html)

        # Quick sign tap buttons in columns
        quick_sample_words = [
            "hello", "thank_you", "please", "water", 
            "food", "help", "bathroom", "yes", 
            "no", "good", "fine", "what", "where"
        ]
        
        pad_cols = st.columns(len(quick_sample_words) // 2 + 1)
        for idx, word in enumerate(quick_sample_words):
            col_idx = idx % len(pad_cols)
            with pad_cols[col_idx]:
                if st.button(word.replace("_", " "), key=f"btn_sign_{word}", use_container_width=True):
                    builder.add_word(word)
                    st.rerun()

        # Raw Contract Data Viewer
        contract_e_payload = builder.build_sentence()
        with st.expander("🔍 Inspect Live Contract E Schema Payload"):
            st.code(json.dumps(contract_e_payload, indent=2), language="json")

    # Cloud limitation clarity
    note_html = textwrap.dedent(
        """
        <div style="font-size: 0.82rem; color: #5E5E68; text-align: center; margin-top: 10px;">
            ℹ️ <b>Cloud Execution Note:</b> This simulator runs pure-Python Agent 3 heuristic smoothing logic in the browser. 
            Direct hardware camera capture and asynchronous SAPI5 speech audio run on the desktop client via 
            <code>python scripts/run_app.py</code>.
        </div>
        """
    ).strip()
    st.html(note_html)
