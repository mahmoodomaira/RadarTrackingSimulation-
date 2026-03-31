# behaviors/base_behavior.py
from abc import ABC, abstractmethod

class BaseBehavior(ABC):
    """
    Contract for all movement behaviors.
    A behavior takes a position + direction + speed
    and returns a new position.
    """

    @abstractmethod
    def move(
        self,
        x: float,
        y: float,
        speed: float,
        direction: float,
        delta_time: float
    ) -> tuple[float, float]:
        """
        Calculate and return the new (x, y) position.
        direction: angle in degrees (0 = right, 90 = down)
        delta_time: seconds since last frame
        """
        pass