# AI-Powered Retail Surveillance & Shoplifting Detection System

A portfolio-ready computer-vision prototype for retail loss-prevention support using YOLO, OpenCV and Streamlit.

## Purpose
The system analyzes recorded retail video, detects and tracks people and relevant objects, monitors configurable zones, and creates **Review Required** events for human verification.

> This project does not identify a person as a shoplifter or make automated accusations. Alerts are decision-support signals that require human review.

## Planned MVP
- Upload recorded CCTV/video
- YOLO person/object detection
- Multi-object tracking
- Configurable checkout/exit monitoring zones
- Rule-based suspicious-event alerts
- Event timestamp and confidence
- Incident snapshots
- Streamlit review dashboard
- CSV event export

## Tech Stack
Python · Ultralytics YOLO · OpenCV · Streamlit · Pandas

## Project Structure
```
app.py
detector.py
event_engine.py
requirements.txt
.gitignore
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Portfolio Note
Use only sample, synthetic, licensed, or otherwise authorized video. The prototype is designed around event review rather than identity recognition.
