# behaviors/straight_behavior.py
import math
from behaviors.base_behavior import BaseBehavior
class ConstantTurnBehavior(BaseBehavior):
    """
    Turns the aircraft at a fixed angular rate each frame.
    Produces a smooth circular arc.

    Parameters
    ----------
    turn_rate : float
        Degrees per second. Positive = clockwise, negative = counter-clockwise.
    """

    def __init__(self, turn_rate: float):
        self.turn_rate = turn_rate

    def move(self, x: float, y: float, speed: float, direction: float, dt: float) -> tuple[float, float, float]:
        """
        Advance position and rotate heading by turn_rate * dt.

        Parameters
        ----------
        x, y : float
            Current position.
        speed : float
            Pixels per second.
        direction : float
            Current heading in degrees.
        dt : float
            Seconds since last frame.

        Returns
        -------
        tuple[float, float, float]
            (new_x, new_y, new_direction)

        Notes
        -----
        Check your BaseBehavior and StraightBehavior return signature
        carefully — match it exactly.
        """
        new_direction = (direction + self.turn_rate * dt) % 360
        radians = math.radians(new_direction)
        new_x = x + math.cos(radians) * speed * dt
        new_y = y + math.sin(radians) * speed * dt
        return (new_x, new_y, new_direction)