import pygame
import config as c
from block import Block
from pygame.rect import Rect
from math import sqrt, pow

class Grid:
    def __init__(self, w, h):
        self.table = []
        self.block_width = w
        self.block_height = h
        self.width = w * c.block_size
        self.height = h * c.block_size
        self.s_height = (c.screen_height - self.height) // 2
        self.e_height = (c.screen_height + self.height) // 2
        self.s_width = (c.screen_width - self.width) // 2
        self.e_width = (c.screen_width + self.width) // 2

        self.pressed_block = [-1, -1]
        for i in range(h):
            arr = []
            for j in range(w):
                empty_block = Block(j, i, self.s_width, self.s_height, c.block_size, "empty")
                arr.append(empty_block)
            self.table.append(arr)

    def is_empty(self, x, y):
        buff_obj = self.table[y][x]
        if buff_obj.type == "empty":
            return True
        else:
            return False
    def add_block(self, x, y, type):
        new_block = Block(x, y, self.s_width, self.s_height, c.block_size, type)
        self.table[y][x] = new_block

    def is_done(self):
        done_bool = True
        order_lst = ["yellow","orange","red"]
        for el in order_lst:
            lst_pos = order_lst.index(el)
            pos = order_lst.index(el) * 2
            for j in range(self.block_height):
                if order_lst[lst_pos] != self.table[j][pos].type:
                    done_bool = False
        return done_bool
    #movement mechanics
    def handle_mouse_down(self, pos):
        for j in range(self.block_height):
            for i in range(self.block_width):
                if self.table[j][i].type != "obstacle" and self.table[j][i].bounds_touch.collidepoint(pos):
                    if (self.pressed_block[0] == j) and (self.pressed_block[1] == i):
                        pass
                    else:
                        if self.table[j][i].type != "empty":
                            if self.pressed_block != [-1, -1]:
                                self.table[self.pressed_block[0]][self.pressed_block[1]].deactivate()
                            self.pressed_block = [j, i]
                            self.table[j][i].activate()
                        else:
                            if self.pressed_block != [-1, -1]:
                                if sqrt(pow(self.pressed_block[0] - j, 2) + pow(self.pressed_block[1] - i, 2)) == 1:
                                    self.table[j][i].edit_type(self.table[self.pressed_block[0]][self.pressed_block[1]].type)
                                    self.table[self.pressed_block[0]][self.pressed_block[1]].edit_type("empty")
                                    self.pressed_block = [-1, -1]

    def handler(self, type, pos):
        if type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)

    def update(self):
        if self.is_done():
            return True
        else :
            return False

    def draw(self, surface):
        #drawing header grid
        pygame.draw.rect(surface, c.grid_bg_color, (self.s_width, self.s_height - 2 * c.block_size, self.width, c.block_size))
        pygame.draw.line(surface, c.grid_edge_color, (self.s_width, self.s_height - 2 * c.block_size), (self.e_width, self.s_height - 2 * c.block_size), c.grid_edge_width)
        pygame.draw.line(surface, c.grid_edge_color, (self.s_width, self.s_height - c.block_size), (self.e_width, self.s_height - c.block_size), c.grid_edge_width)
        for i in range(self.block_width + 1):
            pygame.draw.line(surface, c.grid_edge_color, (self.s_width + i * c.block_size, self.s_height - c.block_size), (self.s_width + i * c.block_size, self.s_height - 2 * c.block_size), c.grid_edge_width)
        #drawing color order
        pygame.draw.ellipse(surface, c.block_yellow_color, (self.s_width + 5, self.s_height - 2 * c.block_size + 5, c.block_size - 5, c.block_size - 5))
        pygame.draw.ellipse(surface, c.block_orange_color, (self.s_width + 2 * c.block_size + 5, self.s_height - 2 * c.block_size + 5, c.block_size - 5, c.block_size - 5))
        pygame.draw.ellipse(surface, c.block_red_color, (self.s_width + 4 * c.block_size + 5, self.s_height - 2 * c.block_size + 5, c.block_size - 5, c.block_size - 5))
        #drawing grid
        pygame.draw.rect(surface, c.grid_bg_color, (self.s_width, self.s_height, self.width, self.height))
        for j in range(self.block_height + 1):
            pygame.draw.line(surface, c.grid_edge_color, (self.s_width, self.s_height + j * c.block_size), (self.e_width, self.s_height + j * c.block_size), c.grid_edge_width)
        for i in range(self.block_width + 1):
            pygame.draw.line(surface, c.grid_edge_color, (self.s_width + i * c.block_size, self.s_height), (self.s_width + i * c.block_size, self.e_height), c.grid_edge_width)
        #drawing blocks
        for j in range(self.block_height):
            for i in range(self.block_width):
                self.table[j][i].draw(surface)
                self.table[j][i].update()
