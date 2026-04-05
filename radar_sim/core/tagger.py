# core/tagger.py
import math
from core.radar_object import RadarObject
from core.render_snapshot import RenderSnapshot

class Tagger:
    def __init__(self, hit_radius: float = 15.0):
        self.hit_radius = hit_radius

    def handle_click(
        self,
        click_x: float,
        click_y: float,
        snapshots: list[RenderSnapshot]
    ) -> RadarObject | None:
        closest = None
        closest_dist = float('inf')

        for snap in snapshots:
            dist = self._distance(click_x, click_y, snap.rx, snap.ry)
            if dist < self.hit_radius and dist < closest_dist:
                closest = snap.obj
                closest_dist = dist

        if closest is not None:
            closest.cycle_tag()

        return closest

    def _distance(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)