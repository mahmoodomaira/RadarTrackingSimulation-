# core/alpha_beta_filter.py
from core.base_filter import BaseFilter

class AlphaBetaFilter(BaseFilter):
    """
    A two-state recursive filter estimating position and velocity
    from noisy scalar measurements.

    Applied independently per axis (x and y each get their own instance).

    Parameters
    ----------
    alpha : float
        Position smoothing gain. Range (0, 1).
        Higher = more responsive to measurements, less smoothing.
    beta : float
        Velocity smoothing gain. Range (0, 1).
        Higher = velocity adapts faster, more noise in velocity estimate.
    """

    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
        self._initialized = False

    def initialize(self, position: float, velocity: float = 0.0) -> None:
        """
        Seed the filter with a known position before the first update.
        Sets initialized flag so update() knows to skip the predict phase
        on the very first call.

        Parameters
        ----------
        position : float
            Initial position estimate (typically the first measurement).
        velocity : float
            Initial velocity estimate. Default 0.0.
        """
        self._position = position
        self._velocity = velocity
        self._initialized = True

    def update(self, measurement: float, dt: float) -> float:
        """
        Ingest one noisy measurement and return the filtered position estimate.

        On the first call (not yet initialized): calls initialize(measurement)
        and returns measurement directly — no filtering yet.

        On subsequent calls: runs predict → residual → correct and returns
        the updated position estimate.

        Parameters
        ----------
        measurement : float
            The raw noisy observation z_k.
        dt : float
            Time since last update in seconds.

        Returns
        -------
        float
            Filtered position estimate x_hat_k.
        """
        if not self._initialized:
            self.initialize(measurement)
            return measurement

        # Predict
        predicted_position = self._position + self._velocity * dt

        # Residual
        residual = measurement - predicted_position

        # Correct
        self._position = predicted_position + self.alpha * residual
        if dt > 0:
            self._velocity = self._velocity + (self.beta * residual) / dt

        return self._position

    @property
    def position(self) -> float:
        """Current position estimate."""
        return self._position

    @property
    def velocity(self) -> float:
        """Current velocity estimate."""
        return self._velocity
    
    def is_initialized(self) -> bool:
        return self._initialized


class AlphaBetaFilter2D(BaseFilter):
    """
    A 2D Alpha-Beta Filter that uses two independent AlphaBetaFilter instances
    for tracking position and velocity in x and y axes separately.

    This provides the same smoothing as the original approach but properly
    implements the BaseFilter interface.

    Parameters
    ----------
    alpha : float
        Position gain (0 < alpha <= 1). Higher values track faster but smooth less.
    beta : float
        Velocity gain (0 < beta <= 2). Higher values adapt faster to acceleration.
    """

    def __init__(self, alpha: float, beta: float):
        self._filter_x = AlphaBetaFilter(alpha, beta)
        self._filter_y = AlphaBetaFilter(alpha, beta)

    def update(self, measured_x: float, measured_y: float, dt: float) -> tuple[float, float]:
        """
        Ingest one 2D measurement and return filtered position.

        On first call: initialize both filters and return measurements directly.
        On subsequent calls: full predict → update cycle for both axes.

        Parameters
        ----------
        measured_x, measured_y : float
            Noisy position observations.
        dt : float
            Seconds since last update.

        Returns
        -------
        tuple[float, float]
            (filtered_x, filtered_y)
        """
        filtered_x = self._filter_x.update(measured_x, dt)
        filtered_y = self._filter_y.update(measured_y, dt)
        return filtered_x, filtered_y

    def reset(self, x: float, y: float) -> None:
        """
        Re-initialize filters at a new position, zero velocity.
        Used for wrap-around recovery.
        """
        self._filter_x.initialize(x)
        self._filter_y.initialize(y)

    def is_initialized(self) -> bool:
        """Return True if both axis filters are initialized."""
        return self._filter_x.is_initialized() and self._filter_y.is_initialized()

    @property
    def position(self) -> tuple[float, float]:
        """Current (x, y) position estimate."""
        return (self._filter_x.position, self._filter_y.position)

    @property
    def velocity(self) -> tuple[float, float]:
        """Current (vx, vy) velocity estimate."""
        return (self._filter_x.velocity, self._filter_y.velocity)