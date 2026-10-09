"""UI Overlay and Dashboard Renderer for SignBridge (Agent 4 - Contract G).

Renders a high-visibility, dark-themed dashboard combining the camera feed,
sign predictions, confidence meter, stability progress, recognized words buffer,
smoothed sentence, and subsystem health indicators.
"""

from typing import Dict, List, Optional, Tuple, Any
import time
import cv2
import numpy as np


# Palette (BGR format for OpenCV)
COLOR_BG = (28, 22, 18)           # Dark slate background
COLOR_PANEL = (42, 34, 28)        # Card / panel background
COLOR_BORDER = (65, 52, 44)       # Subtle card border
COLOR_HEADER = (20, 16, 12)       # Header banner background
COLOR_TEXT = (245, 245, 245)      # Primary crisp text
COLOR_MUTED = (160, 160, 160)     # Secondary / guide text
COLOR_SUCCESS = (90, 210, 110)    # Green (Operational / High Confidence)
COLOR_WARNING = (30, 180, 255)    # Amber/Orange (Moderate Confidence / Mock)
COLOR_DANGER = (70, 70, 240)      # Red (Offline / Error)
COLOR_ACCENT = (255, 185, 30)     # Vibrant Cyan / Blue accent
COLOR_SPEECH = (230, 130, 255)    # Violet / Magenta (TTS Active)
COLOR_CHIP_BG = (60, 48, 38)      # Word chip background


class UIOverlayRenderer:
    """Renders Contract G UI state and diagnostic metrics into a live display canvas."""

    def __init__(self, canvas_width: int = 1000, canvas_height: int = 680):
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Dimensions for layout
        self.header_height = 48
        self.camera_x = 20
        self.camera_y = 64
        self.camera_w = 600
        self.camera_h = 450

        self.panel_x = 636
        self.panel_y = 64
        self.panel_w = 344
        self.panel_h = 450

        self.bottom_x = 20
        self.bottom_y = 526
        self.bottom_w = 960
        self.bottom_h = 138

    def render(
        self,
        camera_frame: Optional[np.ndarray],
        ui_state: Dict[str, Any],
        fps: float = 0.0,
        toast_message: Optional[str] = None,
        stability_count: int = 0,
        stability_target: int = 5,
        is_mock_camera: bool = False,
        is_speaking: bool = False,
        error_message: Optional[str] = None,
    ) -> np.ndarray:
        """Render the complete composite dashboard.

        Args:
            camera_frame: Raw or annotated OpenCV BGR image from CameraCapture.
            ui_state: Dictionary conforming to Contract G.
            fps: Current frames-per-second metric.
            toast_message: Temporary status or notification text.
            stability_count: Number of consecutive agreeing frames.
            stability_target: Stability window threshold (default 5).
            is_mock_camera: Whether camera is in synthetic/mock mode.
            is_speaking: Whether TTS engine is actively talking.
            error_message: Optional persistent error string.

        Returns:
            np.ndarray: Composite dashboard image of shape (canvas_height, canvas_width, 3).
        """
        # Create base canvas
        canvas = np.full((self.canvas_height, self.canvas_width, 3), COLOR_BG, dtype=np.uint8)

        # 1. Render Header
        self._render_header(canvas, ui_state, fps, is_mock_camera, is_speaking)

        # 2. Render Camera Viewport
        self._render_camera_viewport(canvas, camera_frame, is_mock_camera)

        # 3. Render Right Diagnostic Panel (Sign, Confidence, Words, Status)
        self._render_side_panel(canvas, ui_state, stability_count, stability_target)

        # 4. Render Bottom Sentence & Controls Panel
        self._render_bottom_panel(canvas, ui_state, toast_message, error_message, is_speaking)

        return canvas

    def _render_header(
        self,
        canvas: np.ndarray,
        ui_state: Dict[str, Any],
        fps: float,
        is_mock: bool,
        is_speaking: bool,
    ) -> None:
        """Draw top banner with brand, FPS, and status badges."""
        cv2.rectangle(canvas, (0, 0), (self.canvas_width, self.header_height), COLOR_HEADER, -1)
        cv2.line(canvas, (0, self.header_height), (self.canvas_width, self.header_height), COLOR_BORDER, 1)

        # Title
        cv2.putText(
            canvas,
            "SignBridge",
            (20, 32),
            cv2.FONT_HERSHEY_DUPLEX,
            0.85,
            COLOR_ACCENT,
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            canvas,
            "| Real-Time Sign Language Translator",
            (175, 31),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            COLOR_MUTED,
            1,
            cv2.LINE_AA,
        )

        # FPS counter
        fps_text = f"FPS: {fps:4.1f}"
        cv2.putText(
            canvas,
            fps_text,
            (self.canvas_width - 450, 31),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            COLOR_TEXT,
            1,
            cv2.LINE_AA,
        )

        # Status Indicators
        status = ui_state.get("status", {})
        cam_ok = status.get("camera", False)
        model_ok = status.get("model", False)
        speech_ok = status.get("speech", False)

        # Badges
        x_badge = self.canvas_width - 340
        self._draw_pill_badge(canvas, x_badge, 12, 70, 24, "CAM", COLOR_WARNING if is_mock else (COLOR_SUCCESS if cam_ok else COLOR_DANGER))
        self._draw_pill_badge(canvas, x_badge + 80, 12, 75, 24, "MODEL", COLOR_SUCCESS if model_ok else COLOR_DANGER)
        
        speech_color = COLOR_SPEECH if is_speaking else (COLOR_SUCCESS if speech_ok else COLOR_DANGER)
        speech_text = "VOICE: SPK" if is_speaking else "VOICE"
        self._draw_pill_badge(canvas, x_badge + 165, 12, 85, 24, speech_text, speech_color)

    def _render_camera_viewport(
        self,
        canvas: np.ndarray,
        camera_frame: Optional[np.ndarray],
        is_mock: bool,
    ) -> None:
        """Embed camera frame into designated viewport with card border."""
        # Panel frame
        cv2.rectangle(
            canvas,
            (self.camera_x - 1, self.camera_y - 1),
            (self.camera_x + self.camera_w + 1, self.camera_y + self.camera_h + 1),
            COLOR_BORDER,
            1,
        )

        if camera_frame is not None and camera_frame.size > 0:
            resized_cam = cv2.resize(camera_frame, (self.camera_w, self.camera_h), interpolation=cv2.INTER_LINEAR)
            canvas[self.camera_y : self.camera_y + self.camera_h, self.camera_x : self.camera_x + self.camera_w] = resized_cam
        else:
            # Placeholder if no frame
            cv2.rectangle(
                canvas,
                (self.camera_x, self.camera_y),
                (self.camera_x + self.camera_w, self.camera_y + self.camera_h),
                (18, 14, 10),
                -1,
            )
            cv2.putText(
                canvas,
                "No Camera Feed Detected",
                (self.camera_x + 180, self.camera_y + 225),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                COLOR_MUTED,
                1,
                cv2.LINE_AA,
            )

        # Mode tag watermark
        mode_str = "MODE: MOCK SIMULATION" if is_mock else "MODE: LIVE CAMERA"
        tag_color = COLOR_WARNING if is_mock else COLOR_ACCENT
        cv2.rectangle(
            canvas,
            (self.camera_x + 10, self.camera_y + 10),
            (self.camera_x + 210, self.camera_y + 35),
            (0, 0, 0),
            -1,
        )
        cv2.putText(
            canvas,
            mode_str,
            (self.camera_x + 18, self.camera_y + 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            tag_color,
            1,
            cv2.LINE_AA,
        )

    def _render_side_panel(
        self,
        canvas: np.ndarray,
        ui_state: Dict[str, Any],
        stability_count: int,
        stability_target: int,
    ) -> None:
        """Render sign prediction, confidence meter, and recognized words list."""
        px, py, pw, ph = self.panel_x, self.panel_y, self.panel_w, self.panel_h

        # Panel Card
        cv2.rectangle(canvas, (px, py), (px + pw, py + ph), COLOR_PANEL, -1)
        cv2.rectangle(canvas, (px, py), (px + pw, py + ph), COLOR_BORDER, 1)

        # Section 1: Current Sign Recognition
        cv2.putText(canvas, "CURRENT SIGN", (px + 16, py + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_MUTED, 1, cv2.LINE_AA)

        current_sign = ui_state.get("current_sign")
        sign_text = str(current_sign).upper() if current_sign else "..."
        sign_color = COLOR_TEXT if current_sign else COLOR_MUTED

        cv2.putText(
            canvas,
            sign_text,
            (px + 16, py + 72),
            cv2.FONT_HERSHEY_DUPLEX,
            1.05,
            sign_color,
            2,
            cv2.LINE_AA,
        )

        # Section 2: Confidence Bar
        confidence = float(ui_state.get("confidence", 0.0))
        cv2.putText(
            canvas,
            f"CONFIDENCE: {confidence * 100:5.1f}%",
            (px + 16, py + 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            COLOR_MUTED,
            1,
            cv2.LINE_AA,
        )

        bar_w = pw - 32
        bar_h = 14
        bar_x = px + 16
        bar_y = py + 124
        
        # Color bar according to threshold
        if confidence >= 0.60:
            bar_color = COLOR_SUCCESS
        elif confidence >= 0.35:
            bar_color = COLOR_WARNING
        else:
            bar_color = COLOR_DANGER

        self._draw_progress_bar(canvas, bar_x, bar_y, bar_w, bar_h, confidence, bar_color)

        # Section 3: Stability Lock Progress
        cv2.putText(
            canvas,
            f"STABILITY FILTER: {stability_count}/{stability_target} FRAMES",
            (px + 16, py + 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            COLOR_MUTED,
            1,
            cv2.LINE_AA,
        )

        stab_ratio = min(1.0, max(0.0, stability_count / max(1, stability_target)))
        stab_color = COLOR_SUCCESS if stability_count >= stability_target else COLOR_ACCENT
        self._draw_progress_bar(canvas, bar_x, py + 174, bar_w, 10, stab_ratio, stab_color)

        # Divider Line
        cv2.line(canvas, (px + 16, py + 205), (px + pw - 16, py + 205), COLOR_BORDER, 1)

        # Section 4: Word Buffer (Contract D -> E)
        words = ui_state.get("recognized_words", [])
        cv2.putText(
            canvas,
            f"WORD BUFFER ({len(words)} ACCEPTED)",
            (px + 16, py + 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            COLOR_MUTED,
            1,
            cv2.LINE_AA,
        )

        # Render word chips or list
        if not words:
            cv2.putText(
                canvas,
                "No words in buffer yet.",
                (px + 20, py + 265),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.46,
                COLOR_MUTED,
                1,
                cv2.LINE_AA,
            )
        else:
            # Display last 8 words as readable tagged list
            display_words = words[-8:]
            chip_y = py + 250
            for idx, w in enumerate(display_words):
                chip_text = f"{idx + 1}. {w}"
                cv2.rectangle(
                    canvas,
                    (px + 16, chip_y),
                    (px + pw - 16, chip_y + 22),
                    COLOR_CHIP_BG,
                    -1,
                )
                cv2.putText(
                    canvas,
                    chip_text,
                    (px + 24, chip_y + 16),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.44,
                    COLOR_TEXT,
                    1,
                    cv2.LINE_AA,
                )
                chip_y += 24

    def _render_bottom_panel(
        self,
        canvas: np.ndarray,
        ui_state: Dict[str, Any],
        toast_message: Optional[str],
        error_message: Optional[str],
        is_speaking: bool,
    ) -> None:
        """Render constructed sentence box, action toast, and control shortcuts."""
        bx, by, bw, bh = self.bottom_x, self.bottom_y, self.bottom_w, self.bottom_h

        # Panel Card
        cv2.rectangle(canvas, (bx, by), (bx + bw, by + bh), COLOR_PANEL, -1)
        cv2.rectangle(canvas, (bx, by), (bx + bw, by + bh), COLOR_BORDER, 1)

        # Sentence Label
        sentence_label = "SMOOTHED SENTENCE OUTPUT (CONTRACT E):"
        cv2.putText(canvas, sentence_label, (bx + 20, by + 26), cv2.FONT_HERSHEY_SIMPLEX, 0.46, COLOR_MUTED, 1, cv2.LINE_AA)

        # Speaking indicator badge
        if is_speaking:
            self._draw_pill_badge(canvas, bx + 360, by + 10, 110, 20, "SPEAKING...", COLOR_SPEECH)

        # Active toast notification
        if toast_message:
            cv2.putText(
                canvas,
                f"[{toast_message}]",
                (bx + 520, by + 26),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.46,
                COLOR_ACCENT,
                1,
                cv2.LINE_AA,
            )
        elif error_message:
            cv2.putText(
                canvas,
                f"[Alert: {error_message}]",
                (bx + 520, by + 26),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.46,
                COLOR_DANGER,
                1,
                cv2.LINE_AA,
            )

        # Sentence Text Box
        sentence = ui_state.get("sentence", "")
        if not sentence:
            display_sentence = "Start signing in front of camera or use demo keys [1-5]..."
            sent_color = COLOR_MUTED
        else:
            display_sentence = f'"{sentence}"'
            sent_color = COLOR_TEXT

        # If sentence is very long, truncate or wrap
        if len(display_sentence) > 75:
            display_sentence = display_sentence[:72] + '..."'

        cv2.putText(
            canvas,
            display_sentence,
            (bx + 20, by + 68),
            cv2.FONT_HERSHEY_DUPLEX,
            0.80,
            sent_color,
            2,
            cv2.LINE_AA,
        )

        # Divider
        cv2.line(canvas, (bx + 20, by + 92), (bx + bw - 20, by + 92), COLOR_BORDER, 1)

        # Control Key Legend
        shortcuts = (
            "[S] Speak Sentence  |  [C] Clear Buffer  |  [E] Export  |  [Backspace] Undo Word  |  "
            "[M] Toggle Mock  |  [1-5] Quick Signs  |  [Q] Quit"
        )
        cv2.putText(
            canvas,
            shortcuts,
            (bx + 20, by + 118),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.44,
            COLOR_ACCENT,
            1,
            cv2.LINE_AA,
        )

    def _draw_progress_bar(
        self,
        canvas: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        ratio: float,
        fill_color: Tuple[int, int, int],
    ) -> None:
        """Draw a sleek, filled progress bar with background channel."""
        ratio = max(0.0, min(1.0, ratio))
        # Background
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (18, 14, 10), -1)
        cv2.rectangle(canvas, (x, y), (x + w, y + h), COLOR_BORDER, 1)
        # Filled portion
        fill_w = int(w * ratio)
        if fill_w > 0:
            cv2.rectangle(canvas, (x + 1, y + 1), (x + fill_w, y + h - 1), fill_color, -1)

    def _draw_pill_badge(
        self,
        canvas: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        label: str,
        color: Tuple[int, int, int],
    ) -> None:
        """Draw a status indicator pill badge."""
        cv2.rectangle(canvas, (x, y), (x + w, y + h), color, -1)
        cv2.putText(
            canvas,
            label,
            (x + 8, y + h - 7),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.36,
            (15, 15, 15),
            1,
            cv2.LINE_AA,
        )
