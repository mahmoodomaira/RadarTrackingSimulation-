# core/alpha_beta_filter.py

class AlphaBetaFilter:
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