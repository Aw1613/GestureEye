"""Flowing silver-white particle wave canvas background component for the hero section."""

import textwrap
import streamlit as st


def render_canvas_wave() -> None:
    """Render high-performance HTML5 Canvas silver-white particle wave background."""
    canvas_html = textwrap.dedent(
        """
        <div class="vesper-canvas-wrapper" aria-hidden="true">
            <canvas id="vesper-particle-canvas"></canvas>
        </div>
        <script>
        (function() {
            const canvas = document.getElementById('vesper-particle-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            let animationFrameId;
            let width, height;
            let time = 0;
            const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

            function resize() {
                const parent = canvas.parentElement;
                width = canvas.width = (parent ? parent.clientWidth : window.innerWidth) || window.innerWidth;
                height = canvas.height = 540;
            }

            resize();
            window.addEventListener('resize', resize, { passive: true });

            // Ambient floating silver dust particles
            const dustCount = 45;
            const dustParticles = [];
            for (let i = 0; i < dustCount; i++) {
                dustParticles.push({
                    x: Math.random() * (width || 1200),
                    y: Math.random() * (height || 540),
                    radius: Math.random() * 1.5 + 0.6,
                    speedY: -Math.random() * 0.35 - 0.1,
                    speedX: (Math.random() - 0.5) * 0.25,
                    alpha: Math.random() * 0.55 + 0.2
                });
            }

            // Layer wave configs for ethereal silver depth
            const waves = [
                { amp: 46, freq: 0.0032, speed: 0.016, yOffset: 0.44, color: 'rgba(255, 255, 255, 0.45)', step: 18 },
                { amp: 62, freq: 0.0024, speed: -0.012, yOffset: 0.48, color: 'rgba(215, 220, 235, 0.32)', step: 22 },
                { amp: 35, freq: 0.0045, speed: 0.022, yOffset: 0.40, color: 'rgba(180, 185, 205, 0.25)', step: 16 },
                { amp: 52, freq: 0.0028, speed: 0.009, yOffset: 0.52, color: 'rgba(240, 240, 255, 0.20)', step: 24 }
            ];

            function draw() {
                ctx.clearRect(0, 0, width, height);

                // 1. Draw floating ambient dust
                for (let i = 0; i < dustParticles.length; i++) {
                    const p = dustParticles[i];
                    p.y += p.speedY;
                    p.x += p.speedX;
                    if (p.y < 0) { p.y = height; p.x = Math.random() * width; }
                    if (p.x < 0) p.x = width;
                    if (p.x > width) p.x = 0;

                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fillStyle = `rgba(235, 240, 255, ${p.alpha})`;
                    ctx.shadowColor = 'rgba(255, 255, 255, 0.6)';
                    ctx.shadowBlur = 6;
                    ctx.fill();
                }

                // 2. Draw undulating particle waves
                for (let w = 0; w < waves.length; w++) {
                    const wave = waves[w];
                    const baseY = height * wave.yOffset;
                    const points = [];

                    for (let x = 0; x <= width + wave.step; x += wave.step) {
                        const y = baseY + 
                            Math.sin(x * wave.freq + time * wave.speed) * wave.amp + 
                            Math.cos(x * wave.freq * 0.7 - time * wave.speed * 0.8) * (wave.amp * 0.45);
                        points.push({ x, y });
                    }

                    // Draw connecting luminous ribbon line
                    ctx.beginPath();
                    ctx.moveTo(points[0].x, points[0].y);
                    for (let i = 1; i < points.length; i++) {
                        const xc = (points[i - 1].x + points[i].x) / 2;
                        const yc = (points[i - 1].y + points[i].y) / 2;
                        ctx.quadraticCurveTo(points[i - 1].x, points[i - 1].y, xc, yc);
                    }
                    ctx.strokeStyle = wave.color;
                    ctx.lineWidth = 1.2;
                    ctx.shadowColor = 'rgba(255, 255, 255, 0.35)';
                    ctx.shadowBlur = 8;
                    ctx.stroke();

                    // Draw luminous nodes / particles along the wave crests
                    for (let i = 0; i < points.length; i += 2) {
                        const pt = points[i];
                        const particleGlow = 0.4 + 0.5 * Math.sin(i * 0.4 + time * 0.05);
                        ctx.beginPath();
                        ctx.arc(pt.x, pt.y, 1.8, 0, Math.PI * 2);
                        ctx.fillStyle = `rgba(255, 255, 255, ${particleGlow})`;
                        ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
                        ctx.shadowBlur = 10;
                        ctx.fill();
                    }
                }

                // Reset shadow after wave draw
                ctx.shadowBlur = 0;

                if (!prefersReducedMotion) {
                    time += 1;
                    animationFrameId = requestAnimationFrame(draw);
                }
            }

            // Start animation loop
            draw();

            // Pause when page is not visible to conserve battery & GPU
            document.addEventListener('visibilitychange', function() {
                if (document.hidden) {
                    if (animationFrameId) cancelAnimationFrame(animationFrameId);
                } else if (!prefersReducedMotion) {
                    draw();
                }
            });
        })();
        </script>
        """
    ).strip()

    st.html(canvas_html, unsafe_allow_javascript=True)
