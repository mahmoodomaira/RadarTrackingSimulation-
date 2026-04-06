# core/base_filter.py
from abc import ABC, abstractmethod

class BaseFilter(ABC):
    """
    Abstract base class for all tracking filters.
    Filters are 2D — they consume (x, y) measurements
    and return (x, y) estimates.
    """

    @abstractmethod
    def update(self, measured_x: float, measured_y: float, dt: float) -> tuple[float, float]:
        """
        Ingest one noisy 2D measurement and return filtered position.
        First call should initialize the filter and return measurement directly.

        Parameters
        ----------
        measured_x, measured_y : float
            Noisy position observation.
        dt : float
            Seconds since last update.

        Returns
        -------
        tuple[float, float]
            (filtered_x, filtered_y)
        """
        pass

    @abstractmethod
    def reset(self, x: float, y: float) -> None:
        """
        Re-initialize filter at a new position.
        Used for wrap-around recovery and track resets.
        """
        pass

    @abstractmethod
    def is_initialized(self) -> bool:
        """Return True if filter has received at least one measurement."""
        pass

    @property
    @abstractmethod
    def position(self) -> tuple[float, float]:
        """Current (x, y) position estimate."""
        pass