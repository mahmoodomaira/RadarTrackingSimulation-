# core/render_snapshot.py
from dataclasses import dataclass, field
from core.radar_object import RadarObject

@dataclass
class RenderSnapshot:
    """
    All rendering data for one radar object for one frame.
    Computed once per frame, consumed by renderer and tagger.
    """
    obj:            RadarObject
    rx:             float        # render x — filtered if available, else true
    ry:             float        # render y
    raw_x:          float | None = None   # noisy measurement (aircraft only)
    raw_y:          float | None = None
    trail:          list[tuple[float, float]] = field(default_factory=list)