# core/simulation.py
from core.radar_object import RadarObject

class Simulation:
    """
    Owns and manages all active radar objects.
    Responsible for advancing simulation state each frame.
    """

    def __init__(self):
        self._objects: list[RadarObject] = []

    def add_object(self, obj: RadarObject):
        """Register a new radar object into the simulation."""
        self._objects.append(obj)

    def update(self, delta_time: float):
        """Advance all objects by one timestep."""
        for obj in self._objects:
            obj.update(delta_time)

    def get_objects(self) -> list[RadarObject]:
        """Return all active radar objects for rendering."""
        return self._objects