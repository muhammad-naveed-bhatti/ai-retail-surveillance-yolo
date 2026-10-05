from ultralytics import YOLO


class RetailDetector:
    """YOLO detector/tracker wrapper for portfolio demonstration."""

    def __init__(self, model_name: str = "yolo11n.pt", confidence: float = 0.35):
        self.model = YOLO(model_name)
        self.confidence = confidence

    def track(self, frame):
        return self.model.track(
            frame,
            persist=True,
            conf=self.confidence,
            verbose=False,
        )
