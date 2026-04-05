# core/scene_builder.py
import random
from core.simulation import Simulation
from core.aircraft import Aircraft
from core.noise_blip import NoiseBlip
from core.difficulty import DifficultyPreset
from behaviors.straight_behavior import StraightBehavior
from behaviors.random_behavior import RandomBehavior
import config
from behaviors.constant_turn_behavior import ConstantTurnBehavior
from behaviors.evasive_behavior import EvasiveBehavior


class SceneBuilder:
    """
    Builds a populated Simulation from a DifficultyPreset.
    Separates scene construction from simulation logic.
    """

    def build(self, preset: DifficultyPreset) -> Simulation:
        sim = Simulation(noise_std=preset.measurement_noise_std)

        # for i in range(preset.aircraft_count):
        #     x, y = self._random_position()
        #     aircraft = Aircraft(
        #         obj_id    = f"AC{i+1:03d}",
        #         x         = x,
        #         y         = y,
        #         speed     = preset.aircraft_speed,
        #         direction = random.uniform(0, 360),
        #         behavior  = StraightBehavior()
        #     )
        #     aircraft.attach_alpha_beta_filter(config.ALPHA_BETA_ALPHA, config.ALPHA_BETA_BETA)
        #     sim.add_object(aircraft)
            
        for i in range(preset.aircraft_count):
            x, y = self._random_position()
            aircraft = Aircraft(
                obj_id    = f"AC{i+1:03d}",
                x         = x,
                y         = y,
                speed     = preset.aircraft_speed,
                direction = random.uniform(0, 360),
                behavior  = self._make_behavior(preset)
            )
            aircraft.attach_kalman_filter(
                process_noise_std     = config.KALMAN_PROCESS_NOISE_STD,
                measurement_noise_std = preset.measurement_noise_std
            )
            sim.add_object(aircraft)

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
            
    def _make_behavior(self, preset: DifficultyPreset):
        if preset.behavior_mode == "turn":
            return ConstantTurnBehavior(
                turn_rate=random.choice([-1, 1]) * config.CONSTANT_TURN_RATE
            )
        elif preset.behavior_mode == "evasive":
            return EvasiveBehavior(
                min_straight=config.EVASIVE_MIN_STRAIGHT,
                max_straight=config.EVASIVE_MAX_STRAIGHT
            )
        return StraightBehavior()