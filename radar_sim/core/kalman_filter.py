# core/kalman_filter.py
import numpy as np

class KalmanFilter1D:
    """
    A one-dimensional Kalman Filter tracking position and velocity
    from noisy scalar measurements.

    State vector: [position, velocity]
    Motion model: constant velocity with process noise.

    Applied independently per axis — x and y each get their own instance,
    identical to the AlphaBetaFilter pattern.

    Parameters
    ----------
    process_noise_std : float
        Standard deviation of process noise (sigma_a).
        Models unexpected acceleration. Higher = filter adapts faster
        to maneuvers but smooths less.
    measurement_noise_std : float
        Standard deviation of measurement noise (sigma_z).
        Should match the radar's actual noise level from config.
    """

    def __init__(self, process_noise_std: float, measurement_noise_std: float):
        self.process_noise_std = process_noise_std
        self.measurement_noise_std = measurement_noise_std

        # Measurement matrix H (maps state to measurement)
        self.H = np.array([[1, 0]])  # we only measure position

        # Measurement noise covariance R
        self.R = np.array([[measurement_noise_std ** 2]])
        
        self._initialized = False

    def initialize(self, position: float, velocity: float = 0.0) -> None:
        """
        Seed the filter state before the first update.

        Parameters
        ----------
        position : float
            Initial position estimate.
        velocity : float
            Initial velocity estimate. Default 0.0.

        Notes
        -----
        Initial error covariance P should express high uncertainty —
        use a large diagonal matrix (e.g. np.eye(2) * 500.0).
        This lets the filter converge quickly from any starting point.
        """
        self.x = np.array([[position], [velocity]])
        self.P = np.eye(2) * 500.0  # reset uncertainty
        self._initialized = True

    def update(self, measurement: float, dt: float) -> float:
        """
        Ingest one noisy measurement and return the filtered position estimate.

        On the first call (not yet initialized): calls initialize(measurement)
        and returns measurement directly.

        On subsequent calls: runs the full predict → update cycle.

        Parameters
        ----------
        measurement : float
            Raw noisy observation z_k.
        dt : float
            Time since last update in seconds.

        Returns
        -------
        float
            Filtered position estimate.

        Notes
        -----
        Build F and Q inside this method using dt — they change each frame
        if dt is not perfectly constant.
        """
        if not self._initialized:
            self.initialize(measurement)
            return measurement

        # --- Predict Step ---
        F = np.array([[1, dt], [0, 1]])  # state transition matrix
        Q = np.array([[dt**4 / 4, dt**3 / 2],
                      [dt**3 / 2, dt**2]]) * self.process_noise_std ** 2

        # State prediction
        x_pred = F @ self.x
        P_pred = F @ self.P @ F.T + Q

        # --- Update Step ---
        z = np.array([[measurement]])  # measurement vector
        y = z - self.H @ x_pred       # measurement residual
        S = self.H @ P_pred @ self.H.T + self.R  # residual covariance
        K = P_pred @ self.H.T @ np.linalg.inv(S)  # Kalman gain

        self.x = x_pred + K @ y       # state update
        I = np.eye(2)
        self.P = (I - K @ self.H) @ P_pred  # error covariance update

        return float(self.x[0, 0])  # return position estimate

    @property
    def position(self) -> float:
        """Current position estimate."""
        return float(self.x[0, 0])

    @property
    def velocity(self) -> float:
        """Current velocity estimate."""
        return float(self.x[1])