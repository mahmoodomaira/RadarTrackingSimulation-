# rendering/base_renderer.py
from abc import ABC, abstractmethod

class BaseRenderer(ABC):

    @abstractmethod
    def initialize(self):
        """Set up the rendering environment."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the screen for the next frame."""
        pass

    @abstractmethod
    def draw_radar_background(self):
        """Draw the radar circle and background."""
        pass

    @abstractmethod
    def present(self):
        """Push the finished frame to the screen."""
        pass
    
    @abstractmethod
    def draw_object(self, x: float, y: float, obj_type: str, visible: bool = True):
        """Draw a radar object at the given position."""
        pass
    
    @abstractmethod
    def get_delta_time(self) -> float:
        """Return seconds elapsed since last frame."""
        pass