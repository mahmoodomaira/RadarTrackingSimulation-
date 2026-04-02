# core/radar_object.py
from abc import ABC, abstractmethod

class RadarObject(ABC):
    """
    Abstract base for anything that appears on the radar screen.
    All radar objects have a position, an id, and must be updatable.
    """
    TAG_CYCLE = [None, "real", "noise"]
    def __init__(self, obj_id: str, x: float, y: float):
        self.obj_id = obj_id
        self.x = x
        self.y = y
        self.tag = None
        
    def cycle_tag(self):
        """Advance to the next tag in the cycle."""
        current_index = self.TAG_CYCLE.index(self.tag)
        next_index = (current_index + 1) % len(self.TAG_CYCLE)
        self.tag = self.TAG_CYCLE[next_index] 

    @abstractmethod
    def update(self, delta_time: float):
        """
        Advance the object's state by one timestep.
        delta_time: seconds elapsed since last frame.
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """
        Return a string label for this object's type.
        e.g. 'aircraft', 'noise', 'unknown'
        """
        pass

    def get_position(self) -> tuple:
        """Return current (x, y) position."""
        return (self.x, self.y)