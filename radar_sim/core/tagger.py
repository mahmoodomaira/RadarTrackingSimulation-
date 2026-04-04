# core/tagger.py
import math
from core.radar_object import RadarObject

class Tagger:
    """
    Handles user click input.
    Finds the closest radar object to a click and cycles its tag.
    Uses rendered positions so hit detection matches what the user sees.
    """

    def __init__(self, hit_radius: float = 15.0):
        self.hit_radius = hit_radius

    def handle_click(
        self,
        click_x: float,
        click_y: float,
        render_positions: list[tuple[RadarObject, float, float]]
    ) -> RadarObject | None:
        """
        Find the closest object within hit_radius of the click,
        using rendered positions (not true positions) for distance checks.
        If found, cycle its tag and return it.
        If nothing is close enough, return None.
        """
        closest = None
        closest_dist = float('inf')

        for obj, rx, ry in render_positions:
            dist = self._distance(click_x, click_y, rx, ry)
            if dist < self.hit_radius and dist < closest_dist:
                closest = obj
                closest_dist = dist

        if closest is not None:
            closest.cycle_tag()

        return closest

    def _distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)