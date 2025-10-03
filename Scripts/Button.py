import pygame
from Scripts.config import screen, font

class Button:
    def __init__(self, text, x, y, width, height,
                 normal_color='#475F77', hover_color='#D74B4B',
                 text_color=(255, 255, 255), border_radius=40):
        self.original_y_pos = y
        self.rect = pygame.Rect(x, y, width, height)

        self.normal_color = normal_color
        self.hover_color = hover_color
        self.current_color = normal_color

        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        self.border_radius = border_radius

    def draw(self, surface=None):
        if surface is None:
            surface = screen

        self._update_hover_state()

        pygame.draw.rect(surface, self.current_color, self.rect,
                        border_radius=self.border_radius)

        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2,
                        border_radius=self.border_radius)

        surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self, mouse_pos=None):
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        return self.rect.collidepoint(mouse_pos)

    def _update_hover_state(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color