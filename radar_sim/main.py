# main.py
import pygame
import sys
from rendering.pygame_renderer import PygameRenderer
from core.simulation import Simulation
from core.aircraft import Aircraft
from core.noise_blip import NoiseBlip
from core.tagger import Tagger
from core.scorer import Scorer
from core.logger import Logger
from behaviors.straight_behavior import StraightBehavior
from behaviors.random_behavior import RandomBehavior

def main():
    renderer = PygameRenderer()
    renderer.initialize()

    sim    = Simulation()
    tagger = Tagger(hit_radius=15.0)
    scorer = Scorer()
    logger = Logger(output_dir="sessions")

    # Real aircraft
    sim.add_object(Aircraft("AC001", 400, 300, speed=80,  direction=45,  behavior=StraightBehavior()))
    sim.add_object(Aircraft("AC002", 200, 400, speed=60,  direction=310, behavior=StraightBehavior()))
    sim.add_object(Aircraft("AC003", 600, 200, speed=100, direction=190, behavior=StraightBehavior()))

    # Noise blips
    sim.add_object(NoiseBlip("N001", 300, 500, speed=40, behavior=RandomBehavior(drift_degrees=45)))
    sim.add_object(NoiseBlip("N002", 500, 350, speed=30, behavior=RandomBehavior(drift_degrees=60)))
    sim.add_object(NoiseBlip("N003", 450, 250, speed=50, behavior=RandomBehavior(drift_degrees=90)))

    running = True
    while running:

        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tagged = tagger.handle_click(
                    event.pos[0], event.pos[1],
                    sim.get_objects()
                )
                if tagged:
                    result = scorer.evaluate_live(tagged)
                    logger.log_click(tagged.obj_id, tagged.tag, result)
                    print(f"[TAGGED] {tagged.obj_id} → {tagged.tag} ({result})")

        # 2. Update
        delta_time = renderer.get_delta_time()
        sim.update(delta_time)

        # 3. Draw
        renderer.clear()
        renderer.draw_radar_background()

        for obj in sim.get_objects():
            x, y    = obj.get_position()
            visible = getattr(obj, "visible", True)
            renderer.draw_object(x, y, obj.get_type(), visible, obj.tag)

        renderer.present()

    # Session end
    scorer.print_summary(sim.get_objects())
    logger.save_session(scorer.get_summary(), scorer.history)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()