# core/ekf_filter.py
import numpy as np
from core.base_filter import BaseFilter

class ExtendedKalmanFilter(BaseFilter):
    """
    Extended Kalman Filter using a coordinated turn motion model.
    Tracks 2D position and velocity jointly.

    State vector: [x, y, vx, vy]
    Measurement: [x, y] (position only)

    Parameters
    ----------
    process_noise_std : float
        Models unexpected acceleration (sigma_a).
    measurement_noise_std : float
        Radar measurement noise (sigma_z).
    turn_rate : float
        Assumed turn rate in radians/second (omega).
        Use 0.0 for straight flight — EKF reduces to constant velocity.
        Use a nonzero value to model turning targets.
    """

    def __init__(
        self,
        process_noise_std: float,
        measurement_noise_std: float,
        turn_rate: float = 0.0
    ):
        self.process_noise_std    = process_noise_std
        self.measurement_noise_std = measurement_noise_std
        self.turn_rate            = turn_rate
        self._initialized         = False

    def initialize(self, x: float, y: float, vx: float = 0.0, vy: float = 0.0) -> None:
        """
        Seed filter state before first update.
        Initial P should express high uncertainty — np.eye(4) * 500.0.
        """
        self._x           = np.array([[x], [y], [vx], [vy]], dtype=float)
        self.P            = np.eye(4) * 500.0
        self._initialized = True

    def _predict_state(self, dt: float) -> np.ndarray:
        """
        Apply nonlinear motion model f(x) to predict next state.
        Handles omega=0 case without division by zero.
        """
        omega = self.turn_rate
        x  = float(self._x[0, 0])
        y  = float(self._x[1, 0])
        vx = float(self._x[2, 0])
        vy = float(self._x[3, 0])

        if abs(omega) >= 1e-6:
            omega_dt     = omega * dt
            sin_odt      = np.sin(omega_dt)
            cos_odt      = np.cos(omega_dt)
            inv_omega    = 1.0 / omega

            new_x  = x  + sin_odt * inv_omega * vx - (1.0 - cos_odt) * inv_omega * vy
            new_y  = y  + (1.0 - cos_odt) * inv_omega * vx + sin_odt * inv_omega * vy
            new_vx = vx * cos_odt - vy * sin_odt
            new_vy = vx * sin_odt + vy * cos_odt
        else:
            new_x  = x  + vx * dt
            new_y  = y  + vy * dt
            new_vx = vx
            new_vy = vy

        return np.array([[new_x], [new_y], [new_vx], [new_vy]], dtype=float)

    def _compute_jacobian(self, dt: float) -> np.ndarray:
        """
        Compute the 4x4 Jacobian of f(x) evaluated at current state.
        """
        omega = self.turn_rate

        if abs(omega) >= 1e-6:
            omega_dt  = omega * dt
            sin_odt   = np.sin(omega_dt)
            cos_odt   = np.cos(omega_dt)
            inv_omega = 1.0 / omega

            return np.array([
                [1.0, 0.0,  sin_odt * inv_omega,          -(1.0 - cos_odt) * inv_omega],
                [0.0, 1.0,  (1.0 - cos_odt) * inv_omega,   sin_odt * inv_omega        ],
                [0.0, 0.0,  cos_odt,                       -sin_odt                   ],
                [0.0, 0.0,  sin_odt,                        cos_odt                   ]
            ], dtype=float)
        else:
            return np.array([
                [1.0, 0.0, dt,  0.0],
                [0.0, 1.0, 0.0, dt ],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ], dtype=float)

    def _build_Q(self, dt: float) -> np.ndarray:
        """
        Build 4x4 process noise covariance matrix Q.
        Block diagonal — x axis top-left, y axis bottom-right.
        """
        s  = self.process_noise_std ** 2
        q11 = (dt ** 4 / 4.0) * s
        q12 = (dt ** 3 / 2.0) * s
        q22 = (dt ** 2)        * s

        return np.array([
            [q11, q12, 0.0, 0.0],
            [q12, q22, 0.0, 0.0],
            [0.0, 0.0, q11, q12],
            [0.0, 0.0, q12, q22]
        ], dtype=float)

    def update(self, measured_x: float, measured_y: float, dt: float) -> tuple[float, float]:
        """
        Ingest one 2D measurement and return filtered position estimate.
        First call initializes the filter and returns measurement directly.
        """
        if not self._initialized:
            self.initialize(measured_x, measured_y)
            return measured_x, measured_y

        # --- Predict ---
        x_pred = self._predict_state(dt)
        Fj     = self._compute_jacobian(dt)
        Q      = self._build_Q(dt)
        P_pred = Fj @ self.P @ Fj.T + Q

        # --- Update ---
        H = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ], dtype=float)
        R        = np.eye(2) * (self.measurement_noise_std ** 2)
        z        = np.array([[measured_x], [measured_y]], dtype=float)

        residual = z - H @ x_pred
        S        = H @ P_pred @ H.T + R
        K        = P_pred @ H.T @ np.linalg.inv(S)

        self._x  = x_pred + K @ residual
        self.P   = (np.eye(4) - K @ H) @ P_pred

        return float(self._x[0, 0]), float(self._x[1, 0])

    def reset(self, x: float, y: float) -> None:
        """
        Re-initialize filter at new position with zero velocity.
        Used for wrap-around recovery.
        """
        self.initialize(x, y, vx=0.0, vy=0.0)

    @property
    def position(self) -> tuple[float, float]:
        """Current (x, y) position estimate."""
        return float(self._x[0, 0]), float(self._x[1, 0])

    @property
    def velocity(self) -> tuple[float, float]:
        """Current (vx, vy) velocity estimate."""
        return float(self._x[2, 0]), float(self._x[3, 0])
    
    def is_initialized(self) -> bool:
        return self._initialized