# rendering/menu_renderer.py
import pygame
import config
from core.difficulty import DifficultyPreset, ALL_PRESETS

class MenuRenderer:
    """
    Draws the pre-game difficulty selection screen.
    Returns the selected preset when a button is clicked.
    """

    BUTTON_WIDTH  = 200
    BUTTON_HEIGHT = 60
    BUTTON_GAP    = 30

    COLORS = {
        "background":  (0,   0,   0),
        "title":       (0,   255, 100),
        "subtitle":    (150, 150, 150),
        "easy":        (50,  200, 50),
        "medium":      (220, 180, 0),
        "hard":        (220, 60,  60),
        "button_text": (0,   0,   0),
        "hover":       (255, 255, 255),
    }

    PRESET_COLORS = ["easy", "medium", "hard"]

    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.buttons = self._build_buttons()
        pygame.font.init()
        self.font_title    = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_subtitle = pygame.font.SysFont("consolas", 18)
        self.font_button   = pygame.font.SysFont("consolas", 22, bold=True)
        self.font_detail   = pygame.font.SysFont("consolas", 14)

    def _build_buttons(self) -> list[dict]:
        """Calculate button positions centered on screen."""
        buttons   = []
        cx        = config.WINDOW_WIDTH  // 2
        total_h   = len(ALL_PRESETS) * self.BUTTON_HEIGHT + \
                    (len(ALL_PRESETS) - 1) * self.BUTTON_GAP
        start_y   = config.WINDOW_HEIGHT // 2 - total_h // 2 + 40

        for i, preset in enumerate(ALL_PRESETS):
            rect = pygame.Rect(
                cx - self.BUTTON_WIDTH // 2,
                start_y + i * (self.BUTTON_HEIGHT + self.BUTTON_GAP),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT
            )
            buttons.append({"rect": rect, "preset": preset, "color_key": self.PRESET_COLORS[i]})

        return buttons

    def draw(self, mouse_pos: tuple):
        self.screen.fill(self.COLORS["background"])
        self._draw_title()
        for button in self.buttons:
            self._draw_button(button, mouse_pos)

    def _draw_title(self):
        cx = config.WINDOW_WIDTH // 2

        title = self.font_title.render("RADAR SIMULATION", True, self.COLORS["title"])
        self.screen.blit(title, title.get_rect(center=(cx, 160)))

        sub = self.font_subtitle.render("Select difficulty to begin session", True, self.COLORS["subtitle"])
        self.screen.blit(sub, sub.get_rect(center=(cx, 215)))

    def _draw_button(self, button: dict, mouse_pos: tuple):
        rect      = button["rect"]
        preset    = button["preset"]
        color_key = button["color_key"]
        hovered   = rect.collidepoint(mouse_pos)

        # Button fill
        color = self.COLORS["hover"] if hovered else self.COLORS[color_key]
        pygame.draw.rect(self.screen, color, rect, border_radius=8)

        # Button label
        label = self.font_button.render(preset.name, True, self.COLORS["button_text"])
        self.screen.blit(label, label.get_rect(center=rect.center))

        # Detail line below button
        detail_text = (
            f"aircraft: {preset.aircraft_count}  "
            f"noise: {preset.noise_count}  "
            f"speed: {int(preset.aircraft_speed)}"
        )
        detail = self.font_detail.render(detail_text, True, self.COLORS[color_key])
        self.screen.blit(detail, detail.get_rect(
            center=(rect.centerx, rect.bottom + 12)
        ))

    def handle_click(self, mouse_pos: tuple) -> DifficultyPreset | None:
        """Return the preset if a button was clicked, else None."""
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                return button["preset"]
        return None