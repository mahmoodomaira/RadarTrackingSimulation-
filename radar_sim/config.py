# config.py

WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 800
CENTER        = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
RADAR_RADIUS  = 350
FPS           = 60

# Colors
BLACK      = (0,   0,   0)
DARK_GREEN = (0,   40,  0)
GREEN      = (0,   255, 100)

# --- Measurement Noise ---
MEASUREMENT_NOISE_STD_EASY   = 2.0   # pixels, tight radar
MEASUREMENT_NOISE_STD_MEDIUM = 6.0   # pixels, moderate
MEASUREMENT_NOISE_STD_HARD   = 12.0  # pixels, noisy radar

# --- Alpha-Beta Filter ---
ALPHA_BETA_ALPHA = 0.2
ALPHA_BETA_BETA  = 0.05

# --- Kalman Filter ---
KALMAN_PROCESS_NOISE_STD = 0.5   # sigma_a — tune this for aircraft maneuverability

# --- Visualization ---
TRAIL_LENGTH = 20   # number of past filtered positions to display

# --- Filter ---
FILTER_REINIT_THRESHOLD = 80.0  # pixels — jump larger than this triggers re-init

# --- Behaviors ---
CONSTANT_TURN_RATE  = 40.0   # degrees per second
EVASIVE_MIN_STRAIGHT = 1.0   # seconds
EVASIVE_MAX_STRAIGHT = 3.0   # seconds