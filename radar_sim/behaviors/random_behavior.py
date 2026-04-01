# behaviors/random_behavior.py
import math
import random
from behaviors.base_behavior import BaseBehavior

class RandomBehavior(BaseBehavior):
    """
    Moves erratically by randomly adjusting direction each frame.
    Simulates noise or an unstable signal.
    """

    def __init__(self, drift_degrees: float = 30.0):
        """
        drift_degrees: max random angle change per second.
        Higher = more chaotic movement.
        """
        self._drift = drift_degrees
        self._current_direction = random.uniform(0, 360)

    def move(
        self,
        x: float,
        y: float,
        speed: float,
        direction: float,
        delta_time: float
    ) -> tuple[float, float]:

        # Randomly drift the direction each frame
        self._current_direction += random.uniform(
            -self._drift, self._drift
        )

        radians = math.radians(self._current_direction)
        new_x = x + math.cos(radians) * speed * delta_time
        new_y = y + math.sin(radians) * speed * delta_time
        return (new_x, new_y)