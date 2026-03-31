# rendering/pygame_renderer.py
import pygame
from rendering.base_renderer import BaseRenderer
import config

class PygameRenderer(BaseRenderer):

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Radar Simulation")
        self.clock = pygame.time.Clock()

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
        self.clock.tick(config.FPS)