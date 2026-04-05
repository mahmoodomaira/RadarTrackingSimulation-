# core/noise_blip.py
import random
from core.radar_object import RadarObject
from behaviors.base_behavior import BaseBehavior

class NoiseBlip(RadarObject):
    """
    A false radar signal. Moves erratically and flickers on and off.
    """

    def __init__(
        self,
        obj_id: str,
        x: float,
        y: float,
        speed: float,
        behavior: BaseBehavior,
        flicker_chance: float = 0.3
    ):
        super().__init__(obj_id, x, y)
        self.speed = speed
        self.behavior = behavior
        self.flicker_chance = flicker_chance  # 0.0 to 1.0
        self.visible = True

    def update(self, delta_time: float):
        # Move erratically
        self.x, self.y, _ = self.behavior.move(
            self.x, self.y,
            self.speed, 0,
            delta_time
        )
        # Randomly toggle visibility
        self.visible = random.random() > self.flicker_chance

    def get_type(self) -> str:
        return "noise"