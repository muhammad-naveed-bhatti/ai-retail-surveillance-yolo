import os
import tempfile

import cv2
import pandas as pd
import streamlit as st

from detector import RetailDetector
from event_engine import EventEngine, draw_zone

st.set_page_config(page_title="AI Retail Surveillance", page_icon="🛡️", layout="wide")
st.title("AI-Powered Retail Surveillance")
st.caption("YOLO tracking, multi-zone analytics and human-reviewed loss-prevention alerts.")
st.warning("Decision-support prototype: alerts require human review and do not identify anyone as a shoplifter.")

with st.sidebar:
    st.header("Detection controls")
    confidence = st.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
    dwell_seconds = st.slider("Alert dwell time (seconds)", 1, 15, 4, 1)
    st.header("Monitoring zones")
    exit_width = st.slider("Exit zone width (%)", 10, 40, 20, 5)
    checkout_width = st.slider("Checkout zone width (%)", 10, 40, 20, 5)
    st.caption("Checkout = left side · Exit = right side")

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
    metric_box = st.empty()
    live_events = st.empty()
    events = []
    snapshots = []
    frame_count = 0
    unique_tracks = set()

    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break

        frame_count += 1
        h, w = frame.shape[:2]
        zones = {
            "CHECKOUT": (0, 0, int(w * checkout_width / 100), h - 1),
            "EXIT": (int(w * (1 - exit_width / 100)), 0, w - 1, h - 1),
        }

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

                    for zone_name, zone in zones.items():
                        event = engine.observe(
                            track_id=track_id,
                            center=center,
                            zone_name=zone_name,
                            zone=zone,
                            confidence=float(conf),
                            video_time=frame_count / fps,
                        )
                        if event:
                            row = event.to_dict()
                            ok_jpg, encoded = cv2.imencode(".jpg", annotated)
                            if ok_jpg:
                                snapshot_index = len(snapshots)
                                snapshots.append(encoded.tobytes())
                                row["snapshot"] = f"incident_{snapshot_index + 1:03d}.jpg"
                            events.append(row)

        draw_zone(annotated, zones["CHECKOUT"], "CHECKOUT ZONE", (60, 180, 75))
        draw_zone(annotated, zones["EXIT"], "EXIT / REVIEW ZONE", (0, 165, 255))
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        frame_box.image(rgb, channels="RGB", use_container_width=True)

        with metric_box.container():
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Frames", f"{frame_count:,}")
            c2.metric("Tracked people", len(unique_tracks))
            c3.metric("Review events", len(events))
            c4.metric("Video time", f"{frame_count / fps:.1f}s")

        if events:
            live_events.dataframe(pd.DataFrame(events).tail(10), use_container_width=True)

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

    if snapshots:
        st.subheader("Incident Snapshots")
        cols = st.columns(3)
        for i, snapshot in enumerate(snapshots):
            with cols[i % 3]:
                st.image(snapshot, caption=f"Review event {i + 1}", use_container_width=True)
                st.download_button(
                    f"Download snapshot {i + 1}",
                    data=snapshot,
                    file_name=f"incident_{i + 1:03d}.jpg",
                    mime="image/jpeg",
                    key=f"snapshot_{i}",
                )
else:
    st.info("Upload a sample or authorized retail video to start the demonstration.")
