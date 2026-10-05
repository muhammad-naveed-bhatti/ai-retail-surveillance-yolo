# AI-Powered Retail Surveillance & Shoplifting Detection System

Portfolio computer-vision prototype for retail loss-prevention support using YOLO, OpenCV and Streamlit.

## Current MVP
- Recorded CCTV/video upload
- YOLO person detection and multi-object tracking
- Adjustable detection confidence
- Two configurable monitoring zones: **Checkout** and **Exit / Review**
- Per-zone dwell-time based **Review Required** events
- Unique tracked-person, frame, event and video-time metrics
- Incident snapshot capture and preview
- Incident review table
- CSV event export
- Individual JPG snapshot download

> The system does **not** identify a person as a shoplifter and does not perform face recognition. Alerts are neutral decision-support signals that require human verification.

## How the demo works
The left and right portions of the video can be configured as checkout and exit/review zones. When a tracked person remains in either monitored zone longer than the selected dwell threshold, the system creates a review event and captures an incident snapshot. This is intentionally a transparent demonstration rule, not a claim that theft occurred.

## Tech Stack
Python · Ultralytics YOLO · OpenCV · Streamlit · Pandas

## Files
- `app.py` — Streamlit dashboard, video loop, metrics and snapshots
- `detector.py` — YOLO detection/tracking wrapper
- `event_engine.py` — multi-zone and human-review event logic
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
Dashboard analytics, incident severity/rule configuration, demo assets, automated tests, and Streamlit deployment hardening.
