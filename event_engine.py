from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewEvent:
    timestamp: str
    track_id: int
    event_type: str
    confidence: float
    reason: str


def make_review_event(track_id: int, event_type: str, confidence: float, reason: str):
    """Create a human-review event. This function does not classify theft."""
    return ReviewEvent(
        timestamp=datetime.now().isoformat(timespec="seconds"),
        track_id=track_id,
        event_type=event_type,
        confidence=confidence,
        reason=reason,
    )
