"""Unit tests for CameraCapture module (Agent 1)."""

import unittest
import numpy as np
from app.capture.camera import CameraCapture


class TestCameraCapture(unittest.TestCase):
    """Test suite for CameraCapture class."""

    def test_mock_camera_read(self):
        """Verify that the mock camera generates expected frame dimensions."""
        width, height = 320, 240
        cam = CameraCapture(width=width, height=height, fps=30, mock=True)
        self.assertTrue(cam.is_opened())

        success, frame = cam.read()
        self.assertTrue(success)
        self.assertIsNotNone(frame)
        self.assertEqual(frame.shape, (height, width, 3))
        self.assertEqual(frame.dtype, np.uint8)
        cam.release()
        self.assertFalse(cam.is_opened())

    def test_context_manager(self):
        """Verify camera context manager opens and releases cleanly."""
        with CameraCapture(width=640, height=480, mock=True) as cam:
            self.assertTrue(cam.is_opened())
            success, frame = cam.read()
            self.assertTrue(success)
            self.assertEqual(frame.shape, (480, 640, 3))

        # Should be released after exiting context
        self.assertFalse(cam.is_opened())


if __name__ == "__main__":
    unittest.main()
