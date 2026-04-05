# core/simulation.py
from core.radar_object import RadarObject
from core.aircraft import Aircraft

class Simulation:
    def __init__(self, noise_std: float = 0.0):
        self._objects: list[RadarObject] = []
        self.noise_std = noise_std
        self._render_cache: list[tuple[RadarObject, float, float]] = []

    def add_object(self, obj: RadarObject):
        """Register a new radar object into the simulation."""
        self._objects.append(obj)

    def update(self, delta_time: float):
        """Advance all objects by one timestep."""
        for obj in self._objects:
            obj.update(delta_time)

    def get_objects(self) -> list[RadarObject]:
        """Return all active radar objects."""
        return self._objects

    def update_render_positions(self, dt: float) -> None:
        """
        Compute and cache the render position for every object.
        Aircraft: sample noise → filter → cache filtered position.
        Blips: use true position.
        dt is needed for the filter velocity update.
        """
        self._render_cache = []
        for obj in self._objects:
            if isinstance(obj, Aircraft):
                mx, my = obj.get_measured_position(self.noise_std)
                rx, ry = obj.get_kalman_position(mx, my, dt)
            else:
                rx, ry = obj.x, obj.y
            self._render_cache.append((obj, rx, ry))

    def get_cached_render_positions(self) -> list[tuple[RadarObject, float, float]]:
        """
        Return cached (obj, rx, ry) tuples from the last update_render_positions call.
        Renderer and tagger both consume this — never recompute mid-frame.
        """
        return self._render_cache