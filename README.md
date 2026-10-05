# AI-Powered Retail Surveillance & Shoplifting Detection System

Portfolio computer-vision prototype for retail loss-prevention support using YOLO, OpenCV and Streamlit.

## Current MVP
- Recorded CCTV/video upload
- YOLO person detection and multi-object tracking
- Adjustable detection confidence and frame sampling
- Two configurable monitoring zones: **Checkout** and **Exit / Review**
- Per-zone dwell-time based **Review Required** events
- Live operational metrics and zone-event analytics
- Incident snapshot capture, preview and JPG download
- Incident review table and CSV export
- Processing limits, video validation and temporary-file cleanup for cloud deployment

> The system does **not** identify a person as a shoplifter and does not perform face recognition. Alerts are neutral decision-support signals that require human verification.

## How the demo works
The left and right portions of the video can be configured as checkout and exit/review zones. When a tracked person remains in either monitored zone longer than the selected dwell threshold, the system creates a review event and captures an incident snapshot. This is a transparent demonstration rule, not a claim that theft occurred.

## Tech Stack
Python · Ultralytics YOLO · OpenCV · Streamlit · Pandas

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Sign in to Streamlit Community Cloud with GitHub.
2. Create a new app from this repository.
3. Select branch `main` and entrypoint `app.py`.
4. Deploy. The first run can take longer because Ultralytics downloads the YOLO weights.
5. For the public demo, use short authorized/sample videos and conservative processing limits.

## Responsible-use note
Use sample, synthetic, licensed, or otherwise authorized footage. This portfolio project avoids identity recognition and automated accusations. Any event must be reviewed by a human with the surrounding video context.

## Portfolio positioning
**AI-Powered Retail Surveillance | Python · YOLO · OpenCV · Streamlit**

Demonstrates computer vision, object tracking, configurable operational rules, incident logging, dashboard analytics and responsible human-in-the-loop alerting.
