import os
import tempfile
import time

import cv2
import pandas as pd
import streamlit as st

from detector import RetailDetector
from event_engine import EventEngine, draw_zone

st.set_page_config(page_title="AI Retail Surveillance", layout="wide")
st.title("AI-Powered Retail Surveillance")
st.caption("YOLO tracking, monitored-zone analytics and human-reviewed loss-prevention alerts.")
st.warning("Decision-support prototype: alerts require human review and do not identify anyone as a shoplifter.")

confidence = st.sidebar.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
zone_width = st.sidebar.slider("Exit-zone width (%)", 10, 50, 25, 5)
dwell_seconds = st.sidebar.slider("Alert dwell time (seconds)", 1, 15, 4, 1)
uploaded = st.file_uploader("Upload sample/authorized retail video", type=["mp4", "avi", "mov"])

if uploaded:
    suffix = os.path.splitext(uploaded.name)[1] or ".mp4"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        video_path = tmp.name

    detector = RetailDetector(confidence=confidence)
    engine = EventEngine(dwell_seconds=dwell_seconds)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    frame_box = st.empty()
    metrics = st.empty()
    events_box = st.empty()
    events = []
    frame_count = 0
    unique_tracks = set()

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        frame_count += 1
        h, w = frame.shape[:2]
        zone = (int(w * (1 - zone_width / 100)), 0, w - 1, h - 1)
        results = detector.track(frame)
        annotated = frame.copy()

        if results:
            result = results[0]
            annotated = result.plot()
            boxes = result.boxes
            if boxes is not None and boxes.id is not None:
                ids = boxes.id.int().cpu().tolist()
                classes = boxes.cls.int().cpu().tolist()
                confs = boxes.conf.cpu().tolist()
                xyxy = boxes.xyxy.cpu().tolist()

                for track_id, cls_id, conf, box in zip(ids, classes, confs, xyxy):
                    if cls_id != 0:
                        continue
                    unique_tracks.add(track_id)
                    x1, y1, x2, y2 = map(int, box)
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    event = engine.observe(
                        track_id=track_id,
                        center=center,
                        zone=zone,
                        confidence=float(conf),
                        video_time=frame_count / fps,
                    )
                    if event:
                        events.append(event.to_dict())

        draw_zone(annotated, zone, "REVIEW ZONE")
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        frame_box.image(rgb, channels="RGB", use_container_width=True)

        metrics.markdown(
            f"**Frames:** {frame_count:,} &nbsp;&nbsp; "
            f"**Tracked people:** {len(unique_tracks)} &nbsp;&nbsp; "
            f"**Review events:** {len(events)}"
        )
        if events:
            events_box.dataframe(pd.DataFrame(events), use_container_width=True)

    cap.release()
    st.success("Video analysis complete.")

    df = pd.DataFrame(events)
    st.subheader("Incident Review Log")
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download review events CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="retail_review_events.csv",
        mime="text/csv",
        disabled=df.empty,
    )
else:
    st.info("Upload a sample or authorized retail video to start the demonstration.")
