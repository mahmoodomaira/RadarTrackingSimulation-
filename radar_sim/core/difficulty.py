# core/difficulty.py
from dataclasses import dataclass

from config import MEASUREMENT_NOISE_STD_EASY, MEASUREMENT_NOISE_STD_HARD, MEASUREMENT_NOISE_STD_MEDIUM

@dataclass(frozen=True)
class DifficultyPreset:
    """
    A named configuration for one session.
    frozen=True means values cannot be changed after creation.
    """
    name:             str
    aircraft_count:   int
    aircraft_speed:   float   # pixels per second
    noise_count:      int
    noise_speed:      float
    noise_drift:      float   # degrees of random drift
    flicker_chance:   float   # 0.0 to 1.0
    measurement_noise_std: float = 0.0  # default, can be overridden by config


# --- Presets ---

EASY = DifficultyPreset(
    name           = "Easy",
    aircraft_count = 3,
    aircraft_speed = 60.0,
    noise_count    = 2,
    noise_speed    = 25.0,
    noise_drift    = 20.0,
    flicker_chance = 0.4,    # noise flickers often — easy to spot
    measurement_noise_std = MEASUREMENT_NOISE_STD_EASY

)

MEDIUM = DifficultyPreset(
    name           = "Medium",
    aircraft_count = 4,
    aircraft_speed = 90.0,
    noise_count    = 4,
    noise_speed    = 45.0,
    noise_drift    = 45.0,
    flicker_chance = 0.25,   # noise more persistent — harder to spot
    measurement_noise_std = MEASUREMENT_NOISE_STD_MEDIUM
)

HARD = DifficultyPreset(
    name           = "Hard",
    aircraft_count = 5,
    aircraft_speed = 130.0,
    noise_count    = 6,
    noise_speed    = 70.0,
    noise_drift    = 80.0,
    flicker_chance = 0.1,    # noise barely flickers — very hard to spot
    measurement_noise_std = MEASUREMENT_NOISE_STD_HARD
)

ALL_PRESETS = [EASY, MEDIUM, HARD]