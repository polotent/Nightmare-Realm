import pygame
import config as c
from pygame.rect import Rect
class Block():
    def __init__(self, x, y, offset_x, offset_y, size, type):
        self.size = size - c.grid_edge_width // 2
        self.dsize = 0
        self.type = type
        self.state = "normal"
        self.render_mode = "none"
        self.buff_type = "none"
        self.color = "none"
        if self.type == "red" :
            self.size = self.size - 5
            self.render_mode = "ellipse"
            self.color = c.block_red_color
        elif self.type == "orange" :
            self.size = self.size - 5
            self.render_mode = "ellipse"
            self.color = c.block_orange_color
        elif self.type == "yellow" :
            self.size = self.size - 5
            self.render_mode = "ellipse"
            self.color = c.block_yellow_color
        elif self.type == "obstacle" :
            self.render_mode = "rect"
            self.color = c.block_obstacle_color
        elif self.type == "empty" :
            self.size = self.size - 5
            self.dsize = -self.size
            self.render_mode = "none"
        self.x = offset_x + x * size + size // 2 + c.grid_edge_width // 2
        self.y = offset_y + y * size + size // 2 + c.grid_edge_width // 2
        self.bounds = Rect(self.x - self.size // 2 - self.dsize // 2, self.y - self.size // 2 - self.dsize // 2, self.size + self.dsize, self.size + self.dsize)
        self.bounds_touch = Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def deactivate(self):
        self.state = "normal"

    def activate(self):
        self.state = "pressed"

    def edit_type(self, type):
        self.buff_type = type
        self.state = "animated"

    def update(self):
        if self.state == "animated":
            if self.buff_type == "empty":
                if self.dsize-5 <= -self.size:
                    self.state = "normal"
                    self.type = "empty"
                    self.render_mode = "none"
                    self.buff_type = "none"
                    self.dsize = -self.size
                else:
                    self.dsize -= 5

            elif self.buff_type == "red":
                self.render_mode = "ellipse"
                self.color = c.block_red_color
                if self.dsize < 0:
                    self.dsize += 5
                else:
                    self.dsize = 0
                    self.type = "red"
                    self.buff_type = "none"
                    self.state = "normal"

            elif self.buff_type == "orange":
                self.render_mode = "ellipse"
                self.color = c.block_orange_color
                if self.dsize < 0:
                    self.dsize += 5
                else:
                    self.dsize = 0
                    self.type = "orange"
                    self.buff_type = "none"
                    self.state = "normal"

            elif self.buff_type == "yellow":
                self.render_mode = "ellipse"
                self.color = c.block_yellow_color
                if self.dsize < 0:
                    self.dsize += 5
                else:
                    self.dsize = 0
                    self.type = "yellow"
                    self.buff_type = "none"
                    self.state = "normal"


        if self.type != "empty":
            if self.state == "normal":
                if self.dsize != 0:
                    self.dsize += 1
                else:
                    pass
            elif self.state == "pressed":
                if self.dsize == -(self.size - c.block_size_small):
                    pass
                else:
                    self.dsize -= 1

        self.bounds = Rect(self.x - self.size // 2 - self.dsize // 2, self.y - self.size // 2 - self.dsize // 2, self.size + self.dsize, self.size + self.dsize)
    def draw(self, surface):
        if self.render_mode == "ellipse":
            pygame.draw.ellipse(surface, self.color, self.bounds)
        elif self.render_mode == "rect":
            pygame.draw.rect(surface, self.color, self.bounds)
