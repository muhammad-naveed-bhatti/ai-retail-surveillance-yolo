# AI-Powered Retail Surveillance & Shoplifting Detection System

Portfolio computer-vision prototype for retail loss-prevention support using YOLO, OpenCV and Streamlit.

## Current MVP
- Recorded CCTV/video upload
- YOLO person detection and multi-object tracking
- Adjustable detection confidence
- Configurable exit/review zone
- Dwell-time based **Review Required** events
- Unique tracked-person and event metrics
- Incident review table
- CSV event export

> The system does **not** identify a person as a shoplifter and does not perform face recognition. Alerts are neutral decision-support signals that require human verification.

## How the demo works
The right side of the video is treated as a configurable monitored zone. When a tracked person remains in that zone longer than the selected dwell threshold, the system creates one review event. This is intentionally a transparent demonstration rule, not a claim that theft occurred.

## Tech Stack
Python · Ultralytics YOLO · OpenCV · Streamlit · Pandas

## Files
- `app.py` — Streamlit dashboard and video-processing loop
- `detector.py` — YOLO detection/tracking wrapper
- `event_engine.py` — zone and human-review event logic
- `requirements.txt` — dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

The YOLO model weights are downloaded by Ultralytics on first use.

## Responsible-use note
Use sample, synthetic, licensed, or otherwise authorized footage. This portfolio project avoids identity recognition and automated accusations. Any event must be reviewed by a human with the surrounding video context.

## Next planned improvements
Incident snapshots, configurable multi-zone layout, richer analytics, demo video, and deployment hardening.
