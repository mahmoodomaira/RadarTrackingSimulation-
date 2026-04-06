# core/simulation.py
from core.radar_object import RadarObject
from core.aircraft import Aircraft
from core.render_snapshot import RenderSnapshot
import config

class Simulation:
    def __init__(self, noise_std: float = 0.0):
        self._objects: list[RadarObject] = []
        self.noise_std = noise_std
        self._render_cache: list[RenderSnapshot] = []

    def add_object(self, obj: RadarObject):
        self._objects.append(obj)

    def update(self, delta_time: float):
        for obj in self._objects:
            obj.update(delta_time)

    def get_objects(self) -> list[RadarObject]:
        return self._objects

    def update_render_positions(self, dt: float) -> None:
        self._render_cache = []
        for obj in self._objects:
            if isinstance(obj, Aircraft):
                mx, my = obj.get_measured_position(self.noise_std)

                # Wrap-around detection
                if hasattr(obj, '_filter') and obj._filter.is_initialized():
                    ex, ey = obj._filter.position
                    if abs(mx - ex) > config.FILTER_REINIT_THRESHOLD or \
                    abs(my - ey) > config.FILTER_REINIT_THRESHOLD:
                        obj.reset_filter(mx, my)

                rx, ry = obj.get_filtered_position(mx, my, dt)
                obj.update_trail(rx, ry, config.TRAIL_LENGTH)
                self._render_cache.append(RenderSnapshot(
                    obj=obj, rx=rx, ry=ry,
                    raw_x=mx, raw_y=my,
                    trail=obj.get_trail().copy()
                ))
            else:
                self._render_cache.append(RenderSnapshot(
                    obj=obj, rx=obj.x, ry=obj.y
                ))

    def get_cached_render_positions(self) -> list[RenderSnapshot]:
        return self._render_cache