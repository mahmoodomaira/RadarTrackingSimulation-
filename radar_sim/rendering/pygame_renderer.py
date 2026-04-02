# rendering/pygame_renderer.py
import pygame
from rendering.base_renderer import BaseRenderer
import config

class PygameRenderer(BaseRenderer):
    OBJECT_COLORS = {
        "aircraft": (0, 255, 100),
        "noise":    (255, 80,  80),
        "unknown":  (200, 200, 200),
    }
    TAG_COLORS = {
        "real":  (0,   200, 255),  # cyan ring  — user says real
        "noise": (255, 165, 0),    # orange ring — user says noise
    }
    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Radar Simulation")
        self.clock = pygame.time.Clock()
        self._delta_time = 0.0
    def clear(self):
        self.screen.fill(config.BLACK)

    def draw_radar_background(self):
        pygame.draw.circle(
            self.screen, config.DARK_GREEN,
            config.CENTER, config.RADAR_RADIUS
        )
        pygame.draw.circle(
            self.screen, config.GREEN,
            config.CENTER, config.RADAR_RADIUS, 2
        )
        pygame.draw.circle(
            self.screen, config.GREEN,
            config.CENTER, 4
        )

    def present(self):
        pygame.display.flip()
        self._delta_time = self.clock.tick(config.FPS) / 1000.0
        
    def draw_object(
        self,
        x: float,
        y: float,
        obj_type: str,
        visible: bool = True,
        tag: str = None
    ):
        if not visible:
            return

        ix, iy = int(x), int(y)

        # Draw tag ring first (behind the dot)
        if tag and tag in self.TAG_COLORS:
            pygame.draw.circle(
                self.screen,
                self.TAG_COLORS[tag],
                (ix, iy),
                12, 2          # radius 12, thickness 2
            )

        # Draw the dot on top
        color = self.OBJECT_COLORS.get(obj_type, (255, 255, 255))
        pygame.draw.circle(self.screen, color, (ix, iy), 5)
        
    def get_delta_time(self) -> float:
        return self._delta_time  