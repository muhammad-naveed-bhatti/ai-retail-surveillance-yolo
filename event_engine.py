from dataclasses import asdict, dataclass


@dataclass
class ReviewEvent:
    video_time_seconds: float
    track_id: int
    zone: str
    event_type: str
    confidence: float
    reason: str

    def to_dict(self):
        return asdict(self)


def point_in_zone(point, zone):
    x, y = point
    x1, y1, x2, y2 = zone
    return x1 <= x <= x2 and y1 <= y <= y2


def draw_zone(frame, zone, label, color=(0, 165, 255)):
    import cv2

    x1, y1, x2, y2 = zone
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1 + 8, y1 + 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)


class EventEngine:
    """Creates neutral human-review events from configurable zone dwell behavior."""

    def __init__(self, dwell_seconds=4):
        self.dwell_seconds = dwell_seconds
        self.entered_at = {}
        self.alerted = set()

    def observe(self, track_id, center, zone_name, zone, confidence, video_time):
        key = (track_id, zone_name)

        if point_in_zone(center, zone):
            self.entered_at.setdefault(key, video_time)
            dwell = video_time - self.entered_at[key]

            if dwell >= self.dwell_seconds and key not in self.alerted:
                self.alerted.add(key)
                return ReviewEvent(
                    video_time_seconds=round(video_time, 2),
                    track_id=track_id,
                    zone=zone_name,
                    event_type="Review Required",
                    confidence=round(confidence, 3),
                    reason=f"Tracked person remained in {zone_name.lower()} zone for {dwell:.1f}s.",
                )
        else:
            self.entered_at.pop(key, None)
            self.alerted.discard(key)

        return None
