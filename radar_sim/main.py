# main.py
import pygame
import sys
from rendering.pygame_renderer import PygameRenderer
from rendering.menu_renderer import MenuRenderer
from core.simulation import Simulation
from core.scene_builder import SceneBuilder
from core.tagger import Tagger
from core.scorer import Scorer
from core.logger import Logger

def main():
    renderer = PygameRenderer()
    renderer.initialize()

    menu     = MenuRenderer(renderer.screen)
    builder  = SceneBuilder()
    tagger   = Tagger(hit_radius=15.0)
    scorer   = Scorer()
    logger   = Logger(output_dir="sessions")

    sim      = None
    state    = "menu"         # "menu" | "simulation"

    running  = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if state == "menu":
                    preset = menu.handle_click(mouse_pos)
                    if preset:
                        sim   = builder.build(preset)
                        state = "simulation"
                        print(f"\n[SESSION] Difficulty: {preset.name}")
                        print(f"[SESSION] Aircraft: {preset.aircraft_count}  "
                              f"Noise: {preset.noise_count}\n")

                elif state == "simulation":

                    tagged = tagger.handle_click(
                        mouse_pos[0], mouse_pos[1],
                        sim.get_cached_render_positions()
                    )
                    if tagged:
                        result = scorer.evaluate_live(tagged)
                        logger.log_click(tagged.obj_id, tagged.tag, result)
                        print(f"[TAGGED] {tagged.obj_id} → {tagged.tag} ({result})")

        # 2. Update
        if state == "simulation":
            delta_time = renderer.get_delta_time()
            sim.update(delta_time)
            sim.update_render_positions(delta_time)   # cache render positions once per frame
        else:
            renderer.get_delta_time()

        # 3. Draw
        if state == "menu":
            menu.draw(mouse_pos)
            pygame.display.flip()

        elif state == "simulation":
            renderer.clear()
            renderer.draw_radar_background()
            for snap in sim.get_cached_render_positions():
                visible = getattr(snap.obj, "visible", True)
                if snap.trail:
                    renderer.draw_trail(snap.trail)
                if snap.raw_x is not None:
                    renderer.draw_raw_blip(snap.raw_x, snap.raw_y)
                renderer.draw_object(snap.rx, snap.ry, snap.obj.get_type(), visible, snap.obj.tag)
            renderer.present()

    # Session end
    if sim is not None:
        scorer.print_summary(sim.get_objects())
        logger.save_session(scorer.get_summary(), scorer.history)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()