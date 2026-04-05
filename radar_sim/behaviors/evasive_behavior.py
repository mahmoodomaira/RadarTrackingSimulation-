import random
import math
from behaviors.base_behavior import BaseBehavior


class EvasiveBehavior(BaseBehavior):
    """
    Flies straight for a random interval, then snaps to a new random heading.
    Models an aircraft actively trying to break tracking.

    Parameters
    ----------
    min_straight : float
        Minimum seconds before a heading change.
    max_straight : float
        Maximum seconds before a heading change.
    """

    def __init__(self, min_straight: float = 1.0, max_straight: float = 3.0):
        self._min_straight = min_straight
        self._max_straight = max_straight
        self._straight_timer = random.uniform(min_straight, max_straight)
        self._current_direction = random.uniform(0, 360)

    def move(self, x: float, y: float, speed: float, direction: float, dt: float) -> tuple[float, float, float]:
        """
        Advance position straight ahead. When the straight-flight timer
        expires, snap to a new random heading and reset the timer.

        Returns
        -------
        tuple[float, float, float]
            (new_x, new_y, new_direction)
        """
        self._straight_timer -= dt
        if self._straight_timer <= 0:
            self._current_direction = random.uniform(0, 360)
            self._straight_timer = random.uniform(self._min_straight, self._max_straight)
        radians = math.radians(self._current_direction)
        new_x = x + math.cos(radians) * speed * dt
        new_y = y + math.sin(radians) * speed * dt
        return (new_x, new_y, self._current_direction)