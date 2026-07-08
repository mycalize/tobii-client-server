import pygame


class GazePoint:
    def __init__(self, pos, inner_radius, outer_radius, color):
        self.pos = pos
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

        self.inner_color = pygame.Color(color)
        self.outer_color = pygame.Color(color)
        self.outer_color.a = 150

    def draw(self, screen):
        pygame.draw.circle(screen, self.outer_color.premul_alpha(), self.pos, self.outer_radius)
        pygame.draw.circle(screen, self.inner_color, self.pos, self.inner_radius)
