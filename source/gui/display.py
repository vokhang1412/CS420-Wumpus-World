import pygame
from render_info import RenderInfo
# from win32gui import SetWindowPos

period = 0.5

class Displayer:
    def __init__(self, map_name):
        self.delta_time = 0
        self.accu_time = 0
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.render_info = RenderInfo('./map/' + map_name + '.txt')

        self.surface = pygame.Surface((self.render_info.SCREEN_WIDTH, self.render_info.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.center_x = self.render_info.SCREEN_WIDTH / 2 - self.render_info.CELL_SIZE * self.render_info.n / 2
        self.center_y = self.render_info.SCREEN_HEIGHT / 2 - self.render_info.CELL_SIZE * self.render_info.n / 2

    def run(self):
        # SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)
        while True:
            # IF KEY PRESSED
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            if self.render_info.is_done:
                pygame.time.wait(5000)
                print('Score: ' + str(self.render_info.score))
                pygame.quit()
                return
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.accu_time += self.delta_time
            if self.accu_time >= period:
                self.accu_time -= period
                self.render_info.update_next_step()
                self.surface.fill((255, 255, 255))
                self.render_info.draw(self.surface)
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.surface, (0, 0))
            pygame.display.flip()
