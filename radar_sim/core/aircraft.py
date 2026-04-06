# core/aircraft.py
from core.radar_object import RadarObject
from behaviors.base_behavior import BaseBehavior
import config
import numpy as np
from collections import deque

from core.base_filter import BaseFilter

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
        self.x, self.y, self.direction = self.behavior.move(
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
    
    # def attach_alpha_beta_filter(self, alpha: float, beta: float) -> None:
    #     """
    #     Attach an Alpha-Beta filter to this aircraft.
    #     Creates two independent filter instances — one per axis.
    #     Does not initialize them; initialization happens on first measurement.

    #     Parameters
    #     ----------
    #     alpha : float
    #         Position gain passed to both filters.
    #     beta : float
    #         Velocity gain passed to both filters.
    #     """
    #     self._alpha_beta_filter_x = AlphaBetaFilter(alpha, beta)
    #     self._alpha_beta_filter_y = AlphaBetaFilter(alpha, beta)
        
    # def attach_kalman_filter(self, process_noise_std: float, measurement_noise_std: float) -> None:
    #     """
    #     Attach a Kalman Filter to this aircraft.
    #     Creates two independent KalmanFilter1D instances — one per axis.

    #     Parameters
    #     ----------
    #     process_noise_std : float
    #         Passed to both filters. Models unexpected maneuvers.
    #     measurement_noise_std : float
    #         Passed to both filters. Should match simulation noise_std.
    #     """
    #     self._kalman_filter_x = KalmanFilter1D(process_noise_std, measurement_noise_std)
    #     self._kalman_filter_y = KalmanFilter1D(process_noise_std, measurement_noise_std)

    # def get_filtered_position(self, measurement_x: float, measurement_y: float, dt: float) -> tuple[float, float]:
    #     """
    #     Feed the latest noisy measurement into the filters and return
    #     the smoothed position estimate.

    #     If no filter is attached, return the raw measurements unchanged —
    #     this keeps the aircraft usable without a filter.

    #     Parameters
    #     ----------
    #     measurement_x : float
    #         Noisy x observation (output of get_measured_position).
    #     measurement_y : float
    #         Noisy y observation (output of get_measured_position).
    #     dt : float
    #         Time since last update in seconds.

    #     Returns
    #     -------
    #     tuple[float, float]
    #         (filtered_x, filtered_y) smoothed position estimate.
    #     """
    #     if hasattr(self, '_alpha_beta_filter_x'):
    #         filtered_x = self._alpha_beta_filter_x.update(measurement_x, dt)
    #         filtered_y = self._alpha_beta_filter_y.update(measurement_y, dt)
    #         return filtered_x, filtered_y
    #     return measurement_x, measurement_y
    
    # def get_kalman_position(self, measurement_x: float, measurement_y: float, dt: float) -> tuple[float, float]:
    #     """
    #     Feed the latest noisy measurement into the Kalman filters
    #     and return the smoothed position estimate.

    #     If no Kalman filter is attached, return raw measurements unchanged.

    #     Parameters
    #     ----------
    #     measurement_x : float
    #         Noisy x observation.
    #     measurement_y : float
    #         Noisy y observation.
    #     dt : float
    #         Time since last update in seconds.

    #     Returns
    #     -------
    #     tuple[float, float]
    #         (filtered_x, filtered_y)
    #     """
    #     if hasattr(self, '_kalman_filter_x'):
    #         filtered_x = self._kalman_filter_x.update(measurement_x, dt)
    #         filtered_y = self._kalman_filter_y.update(measurement_y, dt)
    #         return filtered_x, filtered_y
    #     return measurement_x, measurement_y
    
    def update_trail(self, x: float, y: float, max_length: int) -> None:
        """
        Append (x, y) to this aircraft's position trail.
        If trail exceeds max_length, remove the oldest entry.
        Trail is initialized lazily on first call.

        Parameters
        ----------
        x : float
            Filtered x position to record.
        y : float
            Filtered y position to record.
        max_length : int
            Maximum number of positions to retain.
        """
        if not hasattr(self, 'trail') or self.trail.maxlen != max_length:
            self.trail = deque(maxlen=max_length)
        self.trail.append((x, y))
            
    def get_trail(self) -> list[tuple[float, float]]:
        """
        Return the current trail as a list of (x, y) tuples,
        oldest first.
        Returns empty list if trail has never been updated.
        """
        if not hasattr(self, 'trail'):
            return []
        return list(self.trail)
    
    # def reset_kalman_filter(self, position_x: float, position_y: float) -> None:
    #     """
    #     Re-initialize the Kalman filters at a new position.
    #     Called when a discontinuity is detected (e.g. wrap-around).
    #     Resets both axis filters and clears the trail.

    #     Parameters
    #     ----------
    #     position_x : float
    #         New x position to seed the filter with.
    #     position_y : float
    #         New y position to seed the filter with.
    #     """
    #     if hasattr(self, '_kalman_filter_x'):
    #         self._kalman_filter_x.initialize(position_x)
    #         self._kalman_filter_y.initialize(position_y)
    #     if hasattr(self, 'trail'):
    #         self.trail.clear()
            
    # def attach_ekf(self, process_noise_std: float, measurement_noise_std: float, turn_rate: float = 0.0) -> None:
    #     """
    #     Attach an Extended Kalman Filter to this aircraft.
    #     Single EKF instance tracks both axes jointly.

    #     Parameters
    #     ----------
    #     process_noise_std : float
    #         Models unexpected acceleration.
    #     measurement_noise_std : float
    #         Should match simulation noise_std.
    #     turn_rate : float
    #         Expected turn rate in radians/second.
    #         0.0 = straight flight, nonzero = coordinated turn.
    #     """
    #     self._ekf = ExtendedKalmanFilter(process_noise_std, measurement_noise_std, turn_rate)

    # def get_ekf_position(self, measured_x: float, measured_y: float, dt: float) -> tuple[float, float]:
    #     """
    #     Feed measurement into EKF and return filtered position.
    #     Falls back to raw measurement if no EKF attached.
    #     """
    #     if hasattr(self, '_ekf'):
    #         return self._ekf.update(measured_x, measured_y, dt)
    #     return measured_x, measured_y
    
    # def reset_ekf(self, position_x: float, position_y: float) -> None:
    #     """Re-initialize EKF at new position. Used for wrap-around recovery."""
    #     if hasattr(self, '_ekf'):
    #         self._ekf.reset(position_x, position_y)
    #     if hasattr(self, 'trail'):
    #         self.trail.clear()
    def attach_filter(self, filter: BaseFilter) -> None:
        """
        Attach any BaseFilter implementation to this aircraft.
        Replaces any previously attached filter.
        """
        self._filter = filter

    def get_filtered_position(self, measured_x: float, measured_y: float, dt: float) -> tuple[float, float]:
        """
        Feed measurement into attached filter and return smoothed position.
        Falls back to raw measurement if no filter attached.
        """
        if hasattr(self, '_filter'):
            return self._filter.update(measured_x, measured_y, dt)
        return measured_x, measured_y

    def reset_filter(self, x: float, y: float) -> None:
        """
        Re-initialize attached filter at new position.
        Clears trail. Used for wrap-around recovery.
        """
        if hasattr(self, '_filter'):
            self._filter.reset(x, y)
        if hasattr(self, 'trail'):
            self.trail.clear()