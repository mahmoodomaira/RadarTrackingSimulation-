from abc import ABC, abstractmethod

class BaseBehavior(ABC):
    @abstractmethod
    def move(
        self,
        x: float,
        y: float,
        speed: float,
        direction: float,
        delta_time: float
    ) -> tuple[float, float, float]:
        """
        Returns (new_x, new_y, new_direction).
        direction: angle in degrees (0 = right, 90 = down)
        delta_time: seconds since last frame
        """
        pass