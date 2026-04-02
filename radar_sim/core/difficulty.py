# core/difficulty.py
from dataclasses import dataclass

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


# --- Presets ---

EASY = DifficultyPreset(
    name           = "Easy",
    aircraft_count = 3,
    aircraft_speed = 60.0,
    noise_count    = 2,
    noise_speed    = 25.0,
    noise_drift    = 20.0,
    flicker_chance = 0.4,    # noise flickers often — easy to spot
)

MEDIUM = DifficultyPreset(
    name           = "Medium",
    aircraft_count = 4,
    aircraft_speed = 90.0,
    noise_count    = 4,
    noise_speed    = 45.0,
    noise_drift    = 45.0,
    flicker_chance = 0.25,   # noise more persistent — harder to spot
)

HARD = DifficultyPreset(
    name           = "Hard",
    aircraft_count = 5,
    aircraft_speed = 130.0,
    noise_count    = 6,
    noise_speed    = 70.0,
    noise_drift    = 80.0,
    flicker_chance = 0.1,    # noise barely flickers — very hard to spot
)

ALL_PRESETS = [EASY, MEDIUM, HARD]