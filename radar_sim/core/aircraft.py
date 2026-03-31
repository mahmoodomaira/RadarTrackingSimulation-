# core/aircraft.py
from core.radar_object import RadarObject
from behaviors.base_behavior import BaseBehavior
import config

class Aircraft(RadarObject):
    """
    A real radar target. Moves according to an injected behavior.
    """

    def __init__(
        self,
        obj_id: str,
        x: float,
        y: float,
        speed: float,
        direction: float,
        behavior: BaseBehavior
    ):
        super().__init__(obj_id, x, y)
        self.speed = speed
        self.direction = direction
        self.behavior = behavior   # ← injected, not hardcoded

    def update(self, delta_time: float):
        self.x, self.y = self.behavior.move(
            self.x, self.y,
            self.speed, self.direction,
            delta_time
        )
        self._wrap_around()

    def get_type(self) -> str:
        return "aircraft"

    def _wrap_around(self):
        """
        If the aircraft flies off one edge, it re-enters from the opposite side.
        """
        cx, cy = config.CENTER
        r = config.RADAR_RADIUS

        if self.x < cx - r: self.x = cx + r
        if self.x > cx + r: self.x = cx - r
        if self.y < cy - r: self.y = cy + r
        if self.y > cy + r: self.y = cy - r