# core/render_snapshot.py
from dataclasses import dataclass, field
from core.radar_object import RadarObject

@dataclass
class RenderSnapshot:
    """
    All rendering data for one radar object for one frame.
    Computed once per frame, consumed by renderer and tagger.
    """
    obj:   RadarObject
    rx:    float
    ry:    float
    raw_x: float | None = None
    raw_y: float | None = None
    trail: list[tuple[float, float]] = field(default_factory=list)