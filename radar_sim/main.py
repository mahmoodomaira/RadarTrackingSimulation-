# main.py
import pygame
import sys
from rendering.pygame_renderer import PygameRenderer
from core.aircraft import Aircraft
from behaviors.straight_behavior import StraightBehavior

def main():
    renderer = PygameRenderer()
    renderer.initialize()

    # Create one aircraft to test
    aircraft = Aircraft(
        obj_id="AC001",
        x=400, y=300,
        speed=80,        # pixels per second
        direction=45,    # degrees
        behavior=StraightBehavior()
    )

    clock_ref = pygame.time.Clock()
    running = True

    while running:

        delta_time = clock_ref.tick(60) / 1000.0  # seconds

        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Update
        aircraft.update(delta_time)

        # 3. Draw
        renderer.clear()
        renderer.draw_radar_background()

        # Draw the aircraft as a small dot
        pos = aircraft.get_position()
        pygame.draw.circle(
            renderer.screen,
            (0, 255, 100),
            (int(pos[0]), int(pos[1])),
            5
        )

        renderer.present()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()