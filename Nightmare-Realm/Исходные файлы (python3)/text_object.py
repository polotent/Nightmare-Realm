import pygame
import config as c

class TextObject:
    def __init__(self, x, y, text, color, font_name, font_size):
        self.pos = (x, y)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text)

    def draw(self, surface, centralized=True):
        text_surface, self.bounds = self.get_surface(self.text)
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        pygame.draw.rect(surface, c.grid_edge_color, (pos[0] - c.font_padding - c.grid_edge_width, pos[1] - c.font_padding - c.grid_edge_width, self.bounds.w + 2 * (c.font_padding + c.grid_edge_width), self.bounds.h + 2 * (c.font_padding + c.grid_edge_width)))
        pygame.draw.rect(surface, c.font_bg_color, (pos[0] - c.font_padding, pos[1] - c.font_padding, self.bounds.w + 2 * c.font_padding, self.bounds.h + 2 * c.font_padding))

        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()
