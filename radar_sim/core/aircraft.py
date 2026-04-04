# core/aircraft.py
from core.radar_object import RadarObject
from behaviors.base_behavior import BaseBehavior
import config
import numpy as np
from core.alpha_beta_filter import AlphaBetaFilter

class Aircraft(RadarObject):
    """
    A real radar target. Moves according to an injected behavior.
    """

    def __init__(
        self,
        obj_id: str,
        x: float,
        y: float,
        speed: float,
        direction: float,
        behavior: BaseBehavior
    ):
        super().__init__(obj_id, x, y)
        self.speed = speed
        self.direction = direction
        self.behavior = behavior   # ← injected, not hardcoded

    def update(self, delta_time: float):
        self.x, self.y = self.behavior.move(
            self.x, self.y,
            self.speed, self.direction,
            delta_time
        )
        self._wrap_around()

    def get_type(self) -> str:
        return "aircraft"

    def _wrap_around(self):
        """
        If the aircraft flies off one edge, it re-enters from the opposite side.
        """
        cx, cy = config.CENTER
        r = config.RADAR_RADIUS

        if self.x < cx - r: self.x = cx + r
        if self.x > cx + r: self.x = cx - r
        if self.y < cy - r: self.y = cy + r
        if self.y > cy + r: self.y = cy - r
        
    def get_measured_position(self, noise_std: float) -> tuple[float, float]:
        """
            Return a noisy observation of this aircraft's true position.

            Models radar measurement error as additive white Gaussian noise
            applied independently to each axis.

            Parameters
            ----------
            noise_std : float
                Standard deviation of the measurement noise in pixels.
                A value of 0.0 must return the true position exactly.

            Returns
            -------
            tuple[float, float]
                (measured_x, measured_y) — the noisy radar return.
                These values may fall outside screen bounds; callers are
                responsible for any clamping if needed.

            Notes
            -----
            The true position (self.x, self.y) must remain unmodified.
            Use numpy or the standard library `random` module — your choice,
            but numpy will be the natural fit once the Kalman Filter arrives.
        """
        noisy_x = self.x + np.random.normal(0, noise_std)
        noisy_y = self.y + np.random.normal(0, noise_std)   
        return noisy_x, noisy_y
    
    def attach_alpha_beta_filter(self, alpha: float, beta: float) -> None:
        """
        Attach an Alpha-Beta filter to this aircraft.
        Creates two independent filter instances — one per axis.
        Does not initialize them; initialization happens on first measurement.

        Parameters
        ----------
        alpha : float
            Position gain passed to both filters.
        beta : float
            Velocity gain passed to both filters.
        """
        self._alpha_beta_filter_x = AlphaBetaFilter(alpha, beta)
        self._alpha_beta_filter_y = AlphaBetaFilter(alpha, beta)
        
    def get_filtered_position(self, measurement_x: float, measurement_y: float, dt: float) -> tuple[float, float]:
        """
        Feed the latest noisy measurement into the filters and return
        the smoothed position estimate.

        If no filter is attached, return the raw measurements unchanged —
        this keeps the aircraft usable without a filter.

        Parameters
        ----------
        measurement_x : float
            Noisy x observation (output of get_measured_position).
        measurement_y : float
            Noisy y observation (output of get_measured_position).
        dt : float
            Time since last update in seconds.

        Returns
        -------
        tuple[float, float]
            (filtered_x, filtered_y) smoothed position estimate.
        """
        if hasattr(self, '_alpha_beta_filter_x'):
            filtered_x = self._alpha_beta_filter_x.update(measurement_x, dt)
            filtered_y = self._alpha_beta_filter_y.update(measurement_y, dt)
            return filtered_x, filtered_y
        return measurement_x, measurement_y
            