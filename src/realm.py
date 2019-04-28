import pygame, random, sys

import config as c

from grid import Grid
from text_object import TextObject

class Realm():
    def __init__(self,caption,width,height,bg_color,frame_rate):
        self.bg_color = bg_color
        self.frame_rate = frame_rate
        self.game_over = False
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.is_game_running = True
        self.grid = None
        self.help_image = pygame.image.load(c.help_image_filename)
        self.help_opened = False
        self.mouse_handlers = []
        self.create_objects()

    def reset_game(self):
        self.game_over = False
        self.grid = None
        self.menu_buttons = []
        self.mouse_handlers = []
        self.create_objects()

    def create_grid(self):
        self.grid = Grid(5, 5)
        self.mouse_handlers.append(self.grid.handler)

    def create_blocks(self):
        #setting unreachable blocks
        self.grid.add_block(1, 0, "obstacle")
        self.grid.add_block(1, 2, "obstacle")
        self.grid.add_block(1, 4, "obstacle")
        self.grid.add_block(3, 0, "obstacle")
        self.grid.add_block(3, 2, "obstacle")
        self.grid.add_block(3, 4, "obstacle")

        for i in range(15):
            block_ok = False
            if i % 3 == 0:
                block_type = "red"
            if i % 3 == 1:
                block_type = "orange"
            if i % 3 == 2:
                block_type = "yellow"
            #searching for free space for a new block
            while (not block_ok):
                x_index = random.randint(0, 4)
                if (x_index == 1) or (x_index == 3):
                    continue
                y_index = random.randint(0, 4)
                if self.grid.is_empty(x_index,y_index):
                    block_ok = True
            self.grid.add_block(x_index, y_index, block_type)

    def create_objects(self):
        self.create_grid()
        self.create_blocks()

    def update(self):
        self.game_over = self.grid.update()

    def draw_victory(self):
        victory_content = TextObject(500,30,"YOU WON! CONGRATULATIONS!", c.font_color, c.font_name, c.font_size)
        victory_content.draw(self.surface)

    def draw_help(self):
        pic_w, pic_h = self.help_image.get_width(), self.help_image.get_height()
        w, h = pygame.display.get_surface().get_size()
        self.surface.blit(self.help_image,((w - pic_w) // 2 +1, h // 2 - 3 * pic_h // 5 ))

    def draw_menu(self):
        w, h = pygame.display.get_surface().get_size()
        exit_button = TextObject(610,630,"Exit(Esc)", c.font_color, c.font_name, c.font_size)
        help_button = TextObject(380,630,"Help(H)", c.font_color, c.font_name, c.font_size)
        reset_button = TextObject(510,710,"New Game(N)", c.font_color, c.font_name, c.font_size)
        exit_button.draw(self.surface)
        help_button.draw(self.surface)
        reset_button.draw(self.surface)
        if self.help_opened:
            self.draw_help()
        if self.game_over:
            self.draw_victory()

    def draw(self):
        self.grid.draw(self.surface)
        self.draw_menu()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    if (not self.help_opened):
                        self.game_over = False
                        self.reset_game()
                elif event.key == pygame.K_h:
                    self.help_opened = not self.help_opened
            if self.game_over == False and (not self.help_opened):
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    for handler in self.mouse_handlers:
                        handler(event.type, event.pos)
    def run(self):
        while self.is_game_running:
            self.surface.fill(self.bg_color)

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)

def main():
    game = Realm('Nightmare Realm', c.screen_width, c.screen_height, c.background_color, c.frame_rate)
    game.run()

if __name__ == '__main__':
    main()
