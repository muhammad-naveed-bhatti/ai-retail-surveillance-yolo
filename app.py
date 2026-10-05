import tempfile

import cv2
import pandas as pd
import streamlit as st

from detector import RetailDetector

st.set_page_config(page_title="AI Retail Surveillance", layout="wide")
st.title("AI-Powered Retail Surveillance")
st.caption("YOLO-based detection and tracking for human-reviewed retail loss-prevention alerts.")

st.warning(
    "Decision-support prototype: detections and alerts require human review. "
    "The system does not identify a person as a shoplifter."
)

confidence = st.sidebar.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
uploaded = st.file_uploader("Upload sample/authorized retail video", type=["mp4", "avi", "mov"])

frame_box = st.empty()
status_box = st.empty()

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded.read())
        video_path = tmp.name

    detector = RetailDetector(confidence=confidence)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        frame_count += 1
        results = detector.track(frame)

        if results:
            annotated = results[0].plot()
            annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            frame_box.image(annotated, channels="RGB", use_container_width=True)

        status_box.info(f"Processed frame: {frame_count}")

    cap.release()
    st.success("Video analysis complete.")

st.subheader("Review Events")
st.dataframe(
    pd.DataFrame(columns=["timestamp", "track_id", "event_type", "confidence", "reason"]),
    use_container_width=True,
)
