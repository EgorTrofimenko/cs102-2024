"""Game of life"""

import pygame
from pygame import QUIT

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Class of the gamewindow"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.cell_width = self.life.cols
        self.cell_height = self.life.rows
        self.width = self.cell_size * self.cell_width
        self.height = self.cell_size * self.cell_height
        self.screen_size = self.width + 120, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

        self.pause_button = pygame.Rect(self.width + 10, 10, 100, 30)
        self.restart_button = pygame.Rect(self.width + 10, self.pause_button.y + 40, 100, 30)

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.status = False

    def draw_lines(self) -> None:
        """Drawing lines"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """Drawing grid"""
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x, y = j * self.cell_size + 1, i * self.cell_size + 1
                rect_coord = (x, y, self.cell_size - 1, self.cell_size - 1)
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect_coord)
                if self.life.curr_generation[i][j] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect_coord)

    def draw_buttons(self) -> None:
        """Отрисовать кнопку паузы"""
        pygame.draw.rect(self.screen, pygame.Color("grey"), self.pause_button)
        pygame.draw.rect(self.screen, pygame.Color("grey"), self.restart_button)
        font = pygame.font.SysFont(None, 24)
        text_pause = font.render("Pause", True, pygame.Color("black"))
        text_restart = font.render("Restart", True, pygame.Color("black"))
        self.screen.blit(text_pause, (self.pause_button.x + 25, self.pause_button.y + 8))
        self.screen.blit(text_restart, (self.restart_button.x + 20, self.restart_button.y + 8))

    def run(self) -> None:
        """Game of life"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.pause_button.collidepoint(mouse_pos):
                        paused = not paused
                    elif self.restart_button.collidepoint(event.pos):
                        self.life.curr_generation = self.life.create_grid(randomize=True)
                        self.life.generations = 0
                        self.draw_grid()
                        self.draw_lines()
                    elif paused:
                        x, y = mouse_pos
                        cell_x = x // self.cell_size
                        cell_y = y // self.cell_size
                        if 0 <= cell_x < self.life.cols and 0 <= cell_y < self.life.rows:
                            self.life.curr_generation[cell_y][cell_x] = not self.life.curr_generation[cell_y][cell_x]
                            self.draw_grid()
                            self.draw_lines()

            self.draw_grid()
            self.draw_lines()
            self.draw_buttons()
            if paused is False:
                self.life.step()

            if self.life.is_max_generations_exceeded:
                running = False
            if not self.life.is_changing:
                running = False

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


life = GameOfLife((30, 40), max_generations=500)
ui = GUI(life)
ui.run()
