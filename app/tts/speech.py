"""
Text-to-Speech Module (Agent 3 - Milestone M3)
Implements non-blocking, queued speech synthesis so that speech output
never freezes camera frame capture or model inference loops (Contract F).
"""

import logging
import queue
import threading
import time
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Non-blocking Text-to-Speech manager.
    Runs speech synthesis on a dedicated background worker thread
    using an asynchronous thread-safe queue.
    """

    def __init__(
        self,
        rate: int = 160,
        volume: float = 1.0,
        voice_index: Optional[int] = None,
        enabled: bool = True
    ):
        """
        Args:
            rate: Speech rate (words per minute). Default is 160.
            volume: Speech volume (0.0 to 1.0). Default is 1.0.
            voice_index: Optional index to select voice (male/female).
            enabled: If False, speech is simulated/silent without failing.
        """
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index
        self.enabled = enabled

        self._queue: queue.Queue = queue.Queue()
        self._is_speaking = False
        self._shutdown_event = threading.Event()
        self._engine = None
        self._is_available = False

        # History of spoken utterances (useful for inspection and testing)
        self.spoken_history = []

        # Start background worker thread
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name="SignBridge-TTS-Worker",
            daemon=True
        )
        self._worker_thread.start()

    def _init_engine(self):
        """Initialize pyttsx3 within the worker thread."""
        try:
            # On Windows, ensure COM is initialized for the worker thread
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except ImportError:
                pass

            import pyttsx3
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", self.rate)
            self._engine.setProperty("volume", self.volume)

            if self.voice_index is not None:
                voices = self._engine.getProperty("voices")
                if voices and 0 <= self.voice_index < len(voices):
                    self._engine.setProperty("voice", voices[self.voice_index].id)

            self._is_available = True
            logger.info("pyttsx3 engine initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not initialize pyttsx3 ({e}). Falling back to silent mode.")
            self._engine = None
            self._is_available = False

    def _worker_loop(self):
        """Dedicated background loop that processes speech requests."""
        if self.enabled:
            self._init_engine()

        while not self._shutdown_event.is_set():
            try:
                item = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if item is None:
                # Sentinel to stop worker
                self._queue.task_done()
                break

            text = str(item).strip()
            if text:
                self._is_speaking = True
                self.spoken_history.append(text)

                if self.enabled and self._is_available and self._engine is not None:
                    try:
                        self._engine.say(text)
                        self._engine.runAndWait()
                    except Exception as e:
                        logger.error(f"TTS playback error: {e}")
                else:
                    # In mock/fallback mode, simulate brief speech time
                    time.sleep(0.05)

                self._is_speaking = False

            self._queue.task_done()

        # Clean up COM when thread terminates
        try:
            import pythoncom
            pythoncom.CoUninitialize()
        except (ImportError, Exception):
            pass

    def speak(self, text: str) -> bool:
        """
        Non-blocking call to queue a string for spoken output.
        Returns immediately to prevent blocking the caller.

        Args:
            text: The sentence or word to speak.

        Returns:
            bool: True if queued successfully.
        """
        if not text or not str(text).strip():
            return False

        if self._shutdown_event.is_set():
            logger.warning("Attempted to speak on a shutdown TTS instance.")
            return False

        self._queue.put(str(text).strip())
        return True

    def speak_sentence(self, sentence_data: Union[str, Dict[str, Any]]) -> bool:
        """
        Queue a sentence for speech from a string or Contract E / F dictionary:
            {"text": "Hello, thank you for the water."}

        Args:
            sentence_data: String or dictionary containing "text".

        Returns:
            bool: True if successfully queued.
        """
        if isinstance(sentence_data, dict):
            text = sentence_data.get("text", "")
        elif isinstance(sentence_data, str):
            text = sentence_data
        else:
            return False

        return self.speak(text)

    def stop(self):
        """Stop current speech and clear pending queued speech."""
        # Drain queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
            except (queue.Empty, ValueError):
                break

        if self._engine is not None and self._is_available:
            try:
                self._engine.stop()
            except Exception as e:
                logger.warning(f"Error stopping TTS engine: {e}")

        self._is_speaking = False

    def is_busy(self) -> bool:
        """Return True if currently speaking or if items remain in queue."""
        return self._is_speaking or not self._queue.empty()

    def is_available(self) -> bool:
        """Return True if pyttsx3 engine is operational."""
        return self._is_available

    def wait_until_done(self, timeout: Optional[float] = None) -> bool:
        """
        Block until all queued utterances have finished speaking.
        Helpful in tests and clean shutdown procedures.
        """
        start = time.time()
        while self.is_busy():
            if timeout and (time.time() - start) > timeout:
                return False
            time.sleep(0.02)
        return True

    def shutdown(self, timeout: float = 2.0):
        """Cleanly terminate worker thread."""
        self._shutdown_event.set()
        self._queue.put(None)
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=timeout)
