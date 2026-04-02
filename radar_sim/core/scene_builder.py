# core/scene_builder.py
import random
from core.simulation import Simulation
from core.aircraft import Aircraft
from core.noise_blip import NoiseBlip
from core.difficulty import DifficultyPreset
from behaviors.straight_behavior import StraightBehavior
from behaviors.random_behavior import RandomBehavior
import config

class SceneBuilder:
    """
    Builds a populated Simulation from a DifficultyPreset.
    Separates scene construction from simulation logic.
    """

    def build(self, preset: DifficultyPreset) -> Simulation:
        sim = Simulation()

        for i in range(preset.aircraft_count):
            x, y = self._random_position()
            sim.add_object(Aircraft(
                obj_id    = f"AC{i+1:03d}",
                x         = x,
                y         = y,
                speed     = preset.aircraft_speed,
                direction = random.uniform(0, 360),
                behavior  = StraightBehavior()
            ))

        for i in range(preset.noise_count):
            x, y = self._random_position()
            sim.add_object(NoiseBlip(
                obj_id        = f"N{i+1:03d}",
                x             = x,
                y             = y,
                speed         = preset.noise_speed,
                behavior      = RandomBehavior(drift_degrees=preset.noise_drift),
                flicker_chance= preset.flicker_chance
            ))

        return sim

    def _random_position(self) -> tuple[float, float]:
        """Return a random position inside the radar circle."""
        cx, cy = config.CENTER
        r      = config.RADAR_RADIUS

        while True:
            x = random.uniform(cx - r, cx + r)
            y = random.uniform(cy - r, cy + r)
            # Reject positions outside the circle
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                return x, y