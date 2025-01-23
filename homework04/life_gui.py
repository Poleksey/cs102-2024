import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * 10
        self.height = self.life.rows * 10

        self.screen_size = self.width, self.height

        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        for y, row in enumerate(self.life.curr_generation):
            for x, el in enumerate(row):
                if el == 1:
                    color = pygame.Color("orange")
                else:
                    color = pygame.Color("white")
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
        pass

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        is_game_paused = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # При нажатии на пробел изменяем состояние игры
                    if event.key == pygame.K_SPACE:
                        is_game_paused = not is_game_paused
            # Отрисовка списка клеток

            if not is_game_paused:
                self.draw_grid()
                self.draw_lines()
                self.life.step()
                pygame.display.flip()
                clock.tick(self.speed)
            pause_button_rect = pygame.Rect(20, 20, 100, 50)
            pygame.draw.rect(self.screen, "black", pause_button_rect)

            if is_game_paused:
                pause_text = "Возобновить"
            else:
                pause_text = "Пауза"
            pause_button_text = pygame.font.Font(None, 36).render(pause_text, True, "white")
            self.screen.blit(pause_button_text, (pause_button_rect.x + 20, pause_button_rect.y + 10))
        pygame.quit()
        pass


game = GameOfLife((100, 100), 400)
gui = GUI(game)
gui.run()
