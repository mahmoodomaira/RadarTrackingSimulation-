import math
from core.radar_object import RadarObject

class Tagger:
    """
    Handles user click input.
    Finds the closest radar object to a click and cycles its tag.
    """
    
    def __init__(self, hit_radius: float = 15.0):
        self.hit_radius = hit_radius
        
    def handle_click(
        self,
        click_x: float,
        click_y: float,
        objects: list[RadarObject]
    ) -> RadarObject | None:
        """
        Find the closest object within hit_radius of the click.
        If found, cycle its tag and return it.
        If nothing is close enough, return None.
        """
        closest = None
        closest_distance = float('inf')

        for obj in objects:
            dist = self._distance(click_x, click_y, obj.x, obj.y)
            if dist < self.hit_radius and dist < closest_distance:
                closest = obj
                closest_distance = dist
                
        if closest is not None:
            closest.cycle_tag()
            
        return closest
    
    def _distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)