import math
import random
from behaviors.base_behavior import BaseBehavior

class RandomBehavior(BaseBehavior):
    def __init__(self, drift_degrees: float = 30.0):
        self._drift = drift_degrees
        self._current_direction = random.uniform(0, 360)

    def move(self, x, y, speed, direction, delta_time) -> tuple[float, float, float]:
        self._current_direction += random.uniform(-self._drift, self._drift)
        radians = math.radians(self._current_direction)
        new_x = x + math.cos(radians) * speed * delta_time
        new_y = y + math.sin(radians) * speed * delta_time
        return (new_x, new_y, self._current_direction)