"""Vesper.ai-inspired CSS theme and animation engine for SignBridge."""

def get_vesper_css() -> str:
    """Return custom CSS for pure black, silver liquid-metal aesthetic."""
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

/* --- Root Color Tokens --- */
:root {
    --bg-pure-black: #000000;
    --bg-surface: #060608;
    --bg-card: rgba(12, 12, 16, 0.72);
    --border-metal: rgba(255, 255, 255, 0.12);
    --border-metal-glow: rgba(255, 255, 255, 0.32);
    --text-primary: #FFFFFF;
    --text-secondary: #8E8E98;
    --text-muted: #565660;
    --silver-light: #F4F4F8;
    --silver-mid: #A0A0AD;
    --silver-dark: #32323C;
    --accent-emerald: #00F59B;
}

/* Base Body & Streamlit Overrides */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: var(--bg-pure-black) !important;
    color: var(--text-primary) !important;
    scroll-behavior: smooth;
}

#MainMenu, header, footer {
    visibility: hidden;
    height: 0 !important;
}

.stApp {
    background-color: var(--bg-pure-black) !important;
    background: var(--bg-pure-black) !important;
    padding-top: 0.5rem;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
    max-width: 1200px !important;
    position: relative;
    z-index: 1;
}

/* Accessibility: Focus-Visible */
a:focus-visible, button:focus-visible {
    outline: 2px solid #FFFFFF !important;
    outline-offset: 3px !important;
    border-radius: 9999px !important;
}

/* --- Animated Canvas Wave Background --- */
.vesper-canvas-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 540px;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    -webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 50%, rgba(0, 0, 0, 0) 100%);
    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 50%, rgba(0, 0, 0, 0) 100%);
}

#vesper-particle-canvas {
    display: block;
    width: 100%;
    height: 100%;
}

/* --- Keyframe Animations --- */
@keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes buttonShine {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

.animate-in-1 { animation: fadeInUp 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0.05s both; }
.animate-in-2 { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both; }
.animate-in-3 { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both; }
.animate-in-4 { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both; }

/* Reduced Motion Preference */
@media (prefers-reduced-motion: reduce) {
    *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* --- Slim Liquid-Metal Silver Navbar --- */
.liquid-navbar-wrapper {
    position: sticky;
    top: 14px;
    z-index: 9999;
    display: flex;
    justify-content: center;
    width: 100%;
    margin-bottom: 2rem;
}

.liquid-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 22px;
    width: 100%;
    max-width: 940px;
    background: rgba(12, 12, 16, 0.65);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 9999px;
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.8),
                inset 0 1px 1px rgba(255, 255, 255, 0.28),
                inset 0 -1px 1px rgba(0, 0, 0, 0.6);
    transition: all 0.3s ease;
}

.liquid-navbar:hover {
    border-color: rgba(255, 255, 255, 0.24);
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.9),
                inset 0 1px 2px rgba(255, 255, 255, 0.4);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 1.0rem;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    text-decoration: none;
}

.nav-brand-logo {
    font-size: 1.15rem;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
}

.nav-link {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.86rem;
    font-weight: 500;
    transition: color 0.2s ease;
}

.nav-link:hover {
    color: #FFFFFF;
}

.nav-right {
    display: flex;
    align-items: center;
}

.nav-pill-cta {
    display: inline-flex;
    align-items: center;
    padding: 5px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.16);
    color: #FFFFFF;
    text-decoration: none;
    transition: all 0.2s ease;
}

.nav-pill-cta:hover {
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.3);
    color: #FFFFFF;
}

/* --- Hero Section & Typography --- */
.hero-container {
    text-align: center;
    padding: 4.5rem 1rem 3.5rem 1rem;
    position: relative;
    z-index: 2;
}

.pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 14px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.16);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: #E2E2EA;
    margin-bottom: 1.6rem;
}

.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--accent-emerald);
    box-shadow: 0 0 8px var(--accent-emerald);
}

.hero-title {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    font-size: 3.8rem;
    line-height: 1.12;
    font-weight: 700;
    letter-spacing: -0.04em;
    margin-bottom: 1.35rem;
    color: #FFFFFF;
}

.hero-title-italic {
    font-family: 'Instrument Serif', 'Newsreader', Georgia, serif;
    font-style: italic;
    font-weight: 400;
    letter-spacing: -0.01em;
    background: linear-gradient(135deg, #FFFFFF 0%, #E8E8F2 45%, #A8A8B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-left: 4px;
}

.hero-subtitle {
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 660px;
    margin: 0 auto 2.2rem auto;
    font-weight: 400;
}

/* --- Contrasting Buttons --- */
.btn-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
    margin-bottom: 2.8rem;
}

.vesper-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 28px;
    border-radius: 9999px;
    background: #FFFFFF;
    color: #000000 !important;
    font-weight: 600;
    font-size: 0.92rem;
    text-decoration: none;
    border: 1px solid #FFFFFF;
    box-shadow: 0 4px 20px rgba(255, 255, 255, 0.22);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
}

.vesper-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(255, 255, 255, 0.42);
    background: #F8F8FC;
    color: #000000 !important;
}

.btn-arrow {
    transition: transform 0.2s ease;
}

.vesper-btn-primary:hover .btn-arrow {
    transform: translateX(3px);
}

.vesper-btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 26px;
    border-radius: 9999px;
    background: rgba(18, 18, 24, 0.6);
    backdrop-filter: blur(14px);
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 0.92rem;
    text-decoration: none;
    border: 1px solid rgba(255, 255, 255, 0.16);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    cursor: pointer;
}

.vesper-btn-secondary:hover {
    transform: translateY(-2px);
    border-color: rgba(255, 255, 255, 0.32);
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.25);
    background: rgba(26, 26, 36, 0.8);
    color: #FFFFFF !important;
}

/* Streamlit Button Override */
div.stButton > button {
    background: rgba(18, 18, 24, 0.75) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 9999px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    border-color: rgba(255, 255, 255, 0.35) !important;
    box-shadow: 0 4px 18px rgba(255, 255, 255, 0.18) !important;
    transform: translateY(-1px) !important;
}

/* --- Metric Stats Ribbon --- */
.stats-ribbon {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 2rem 0 3.5rem 0;
    position: relative;
    z-index: 2;
}

.stat-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    border: 1px solid var(--border-metal);
    border-radius: 16px;
    padding: 18px 14px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: rgba(255, 255, 255, 0.25);
    transform: translateY(-3px);
}

.stat-value {
    font-size: 2.0rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 0.80rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* --- Section Headers --- */
.section-header {
    text-align: center;
    margin: 4.5rem 0 2.2rem 0;
    position: relative;
    z-index: 2;
}

.section-tag {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--silver-mid);
    margin-bottom: 8px;
}

.section-title {
    font-size: 2.3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 12px;
    color: #FFFFFF;
}

.section-desc {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.6;
}

/* --- Glassmorphism Cards --- */
.vesper-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-metal);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 36px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    height: 100%;
}

.vesper-card:hover {
    border-color: rgba(255, 255, 255, 0.28);
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.card-agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 9999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.12);
    font-size: 0.74rem;
    font-weight: 600;
    color: var(--silver-light);
    margin-bottom: 14px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
    letter-spacing: -0.02em;
}

.card-text {
    font-size: 0.92rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 16px;
}

.card-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--silver-mid);
    background: rgba(0, 0, 0, 0.4);
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

/* --- Vocabulary Grid Chips --- */
.vocab-chip {
    background: rgba(18, 18, 24, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 14px;
    text-align: center;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--silver-light);
    transition: all 0.2s ease;
}

.vocab-chip:hover {
    border-color: rgba(255, 255, 255, 0.3);
    background: rgba(28, 28, 38, 0.95);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6);
}

/* --- Terminal / Code View --- */
.vesper-terminal {
    background: #060608;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 18px 22px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    color: #E6E6EF;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.7);
    margin: 1rem 0;
    overflow-x: auto;
}

.terminal-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.terminal-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}
.dot-red { background: #FF5F56; }
.dot-yellow { background: #FFBD2E; }
.dot-green { background: #27C93F; }

/* --- Interactive Simulator Card --- */
.sim-display {
    background: #040406;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 20px;
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 1.45rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 1rem 0;
    letter-spacing: -0.01em;
}

.sim-buffer-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    min-height: 36px;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    margin-bottom: 1rem;
}

.token-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #FFFFFF;
}

/* --- Footer --- */
.footer-container {
    margin-top: 5rem;
    padding: 2.5rem 0 1.5rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85rem;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 24px;
    margin-bottom: 1rem;
}

.footer-links a {
    color: var(--text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
}

.footer-links a:hover {
    color: #FFFFFF;
}

/* --- Media Queries for Mobile Responsiveness --- */
@media (max-width: 768px) {
    .liquid-navbar {
        padding: 8px 16px;
    }
    .nav-links {
        display: none;
    }
    .hero-title {
        font-size: 2.5rem;
    }
    .hero-subtitle {
        font-size: 1.0rem;
    }
    .stats-ribbon {
        grid-template-columns: repeat(2, 1fr);
    }
    .section-title {
        font-size: 1.8rem;
    }
    .btn-row {
        flex-direction: column;
        width: 100%;
    }
    .vesper-btn-primary, .vesper-btn-secondary {
        width: 100%;
        justify-content: center;
    }
}
</style>
"""
