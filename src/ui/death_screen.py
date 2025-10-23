"""
Death screen overlay menu with retry/quit options
"""

import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class DeathScreen:
    """Transparent overlay menu shown when player dies"""

    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        # Menu state
        self.selected_option = 0  # 0 = Retry, 1 = Quit
        self.options = ["Retry", "Quit"]
        self.button_rects = []  # Store button rectangles for click detection

        # Colors
        self.overlay_color = (0, 0, 0, 128)  # Semi-transparent black
        self.text_color = WHITE
        self.selected_color = (255, 255, 0)  # Yellow for selected option
        self.hover_color = (200, 200, 200)  # Light grey for hover

    def handle_input(self, event):
        """Handle keyboard and mouse input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.options[self.selected_option].lower()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        return self.options[i].lower()

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i
                    break

        return None

    def draw(self):
        """Draw the death screen overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw "YOU DIED" text
        death_text = self.font_large.render("YOU DIED", True, (220, 20, 20))
        death_rect = death_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        )
        self.screen.blit(death_text, death_rect)

        # Clear button rects for new frame
        self.button_rects = []

        # Draw menu options with clickable areas
        for i, option in enumerate(self.options):
            color = (
                self.selected_color if i == self.selected_option else self.text_color
            )
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)
            )

            # Create clickable area (larger than text for easier clicking)
            button_rect = pygame.Rect(
                option_rect.centerx - 100, option_rect.centery - 30, 200, 60
            )
            self.button_rects.append(button_rect)

            # Draw button background if selected/hovered
            if i == self.selected_option:
                pygame.draw.rect(self.screen, (50, 50, 50), button_rect, 2)

            self.screen.blit(option_text, option_rect)
