import time
import streamlit as st
import cv2
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

# Import our custom logic
from app.keypoints.extractor import HandKeypointExtractor
from app.keypoints.buffer import SequenceBuffer
from app.recognition.inference import ModelInference
from app.sentence.filter import PredictionFilter
from app.sentence.builder import SentenceBuilder
from app.keypoints.preprocessing import FEATURE_DIM

st.set_page_config(page_title="SignBridge Web App", layout="wide")
st.title("dY\"SignBridge: Live Web Translator")
st.markdown("This is the cloud-hosted version of SignBridge using `streamlit-webrtc`.")

class SignBridgeProcessor(VideoProcessorBase):
    def __init__(self):
        # Initialize the exact same AI engines used in our desktop app
        self.extractor = HandKeypointExtractor()
        self.seq_buffer = SequenceBuffer(sequence_length=30, feature_dim=FEATURE_DIM)
        self.inference = ModelInference()
        self.pred_filter = PredictionFilter(stability_window=15, timing_gap=0.5)
        self.builder = SentenceBuilder()
        self.last_fetch_time = None
        self.last_fetched_sign = None
        self.fetch_gap = 0.5

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Convert web frame to OpenCV format
        img = frame.to_ndarray(format="bgr24")
        
        # 1. Extract hand keypoints
        feat_vector, info, annotated_img = self.extractor.extract_keypoints(img, draw=True)
        
        # 2. Build temporal sequence window
        self.seq_buffer.add_frame(feat_vector)
        
        current_pred = "Waiting..."
        
        if self.seq_buffer.is_ready():
            # 3. AI Prediction
            seq = self.seq_buffer.get_sequence()
            pred = self.inference.predict(seq)
            pred_label = pred["label"]
            pred_conf = pred["confidence"]
            now = time.time()

            # Check timing gap
            time_since_fetch = (now - self.last_fetch_time) if self.last_fetch_time else float("inf")
            in_gap = time_since_fetch < self.fetch_gap

            if in_gap:
                mode_tag = "[DISPLAY ONLY]" if pred_label != self.last_fetched_sign else "[COOLDOWN]"
                current_pred = f"{pred_label} ({pred_conf*100:.1f}%) {mode_tag}"
                self.pred_filter.process_prediction(pred)
            else:
                current_pred = f"{pred_label} ({pred_conf*100:.1f}%)"
                # 4. Temporal Filter
                stable_event = self.pred_filter.process_prediction(pred)
                if stable_event:
                    self.last_fetch_time = now
                    self.last_fetched_sign = stable_event["word"]
                    self.builder.add_word(stable_event["word"])

        # 5. Draw UI on the web frame
        sentence = self.builder.get_current_sentence()
        if not sentence:
            sentence = "[Start Signing]"
            
        cv2.putText(annotated_img, sentence, (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)
        cv2.putText(annotated_img, current_pred, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Return processed frame back to the browser
        return av.VideoFrame.from_ndarray(annotated_img, format="bgr24")

# Start the WebRTC stream
webrtc_streamer(
    key="signbridge",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=SignBridgeProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    async_processing=True
)

st.markdown("---")
st.markdown("### How to use:")
st.markdown("1. Click **Start** to allow webcam access.")
st.markdown("2. Hold a sign steady for half a second.")
st.markdown("3. The AI will translate it into a sentence drawn directly on your video feed.")
