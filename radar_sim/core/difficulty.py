from dataclasses import dataclass
import config
from config import (
    MEASUREMENT_NOISE_STD_EASY,
    MEASUREMENT_NOISE_STD_MEDIUM,
    MEASUREMENT_NOISE_STD_HARD
)

@dataclass(frozen=True)
class DifficultyPreset:
    name:                  str
    aircraft_count:        int
    aircraft_speed:        float
    noise_count:           int
    noise_speed:           float
    noise_drift:           float
    flicker_chance:        float
    measurement_noise_std: float = 0.0
    behavior_mode:         str   = "straight"  # "straight" | "turn" | "evasive"

EASY = DifficultyPreset(
    name="Easy",
    aircraft_count=3, aircraft_speed=60.0,
    noise_count=2,    noise_speed=25.0,
    noise_drift=20.0, flicker_chance=0.4,
    measurement_noise_std=MEASUREMENT_NOISE_STD_EASY,
    behavior_mode="straight"
)

MEDIUM = DifficultyPreset(
    name="Medium",
    aircraft_count=4, aircraft_speed=90.0,
    noise_count=4,    noise_speed=45.0,
    noise_drift=45.0, flicker_chance=0.25,
    measurement_noise_std=MEASUREMENT_NOISE_STD_MEDIUM,
    behavior_mode="turn"
)

HARD = DifficultyPreset(
    name="Hard",
    aircraft_count=5, aircraft_speed=130.0,
    noise_count=6,    noise_speed=70.0,
    noise_drift=80.0, flicker_chance=0.1,
    measurement_noise_std=MEASUREMENT_NOISE_STD_HARD,
    behavior_mode="evasive"
)

ALL_PRESETS = [EASY, MEDIUM, HARD]
