import solvers.new_wumpus as new_wumpus
import pygame

CELL_MARGIN = 5
CELL_SIZE = 50

class RenderInfo:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    CELL_SIZE = CELL_SIZE
    CELL_MARGIN = CELL_MARGIN

    def __init__(self, map_path):
        self.map = new_wumpus.read_map(map_path)
        self.n = len(self.map)
        self.map = new_wumpus.update_map(self.map)
        self.visited = []
        for i in range(len(self.map)):
            self.visited.append([False] * len(self.map[i]))
        self.to_solve_map = new_wumpus.read_map(map_path)
        self.to_solve_map = new_wumpus.update_map(self.to_solve_map)
        tmp, self.path, self.score = new_wumpus.solve_wumpus_world(self.to_solve_map)
        self.score = 0
        self.current_pos = (0, 0)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j].find('A') != -1:
                    self.current_pos = (i, j)
                    if self.map[i][j] == 'A':
                        self.map[i][j] = '-'
                    else:
                        self.map[i][j] = self.map[i][j].replace('A', '')
        self.visited[self.current_pos[0]][self.current_pos[1]] = True
        self.is_bump = False
        self.is_scream = False
        self.is_shoot = False
        self.is_collect_gold = False
        self.bump_dir = ''
        self.shoot_dir = ''
        self.font = pygame.font.SysFont('Arial', 20)
        self.is_done = False
        self.center_x = self.SCREEN_WIDTH / 2 - self.CELL_SIZE * self.n / 2
        self.center_y = self.SCREEN_HEIGHT / 2 - self.CELL_SIZE * self.n / 2
        self.is_begin = True
        self.agent_map = []


    # [(2, 1), [['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x']], (1, 1), [['x', 'x', 'x', 'x'], ['x', 'x', 'x', 'x'], ['x', '-', 'x', 'x'], ['x', 'x', 'x', 'x']], 'G(1, 1)', (2, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['x', '-', 'x', 'x'], ['x', 'x', 'x', 'x']], (3, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['x', '-', 'x', 'x'], ['x', 'x', 'x', 'x']], (2, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['x', '-', 'x', 'x'], ['x', 'B', 'x', 'x']], (2, 0), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['x', '-', 'x', 'x'], ['x', 'B', 'x', 'x']], (2, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['S', '-', 'x', 'x'], ['x', 'B', 'x', 'x']], (2, 2), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['S', '-', 'x', 'x'], ['x', 'B', 'x', 'x']], (2, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (1, 1), [['x', 'x', 'x', 'x'], ['x', 'SB', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], 'Shoot the arrow up', 'Shoot the arrow left', 'W (1,0)', (2, 1), [['x', 'x', 'x', 'x'], ['x', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (1, 1), [['x', 'x', 'x', 'x'], ['x', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (1, 0), [['x', 'x', 'x', 'x'], ['x', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (0, 0), [['x', 'x', 'x', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], 'U(0, 0)', 'L(0, 0)', (0, 1), [['-', 'x', 'x', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (0, 2), [['-', '-', 'x', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (0, 1), [['-', '-', 'B', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (1, 1), [['-', '-', 'B', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (2, 1), [['-', '-', 'B', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (2, 0), [['-', '-', 'B', 'x'], ['-', 'B', 'x', 'x'], ['S', '-', 'B', 'x'], ['x', 'B', 'x', 'x']], (3, 0), [['-', '-', 'B', 'x'], ['-', 'B', 'x', 'x'], ['-', '-', 'B', 'x'], ['x', 'B', 'x', 'x']]]
    # The path has changed
    # Now, after each (int, int) is the currrent map from the agent's perspective.
    # The action remains the same
    # We have to render the map from the agent's perspective
        
    def update_next_step(self):
        if len(self.path) == 0:
            self.is_done = True
            return
        tmp = self.path.pop(0)
        if type(tmp) == tuple:
            self.current_pos = tmp
            self.agent_map = self.path.pop(0)
            if self.map[self.current_pos[0]][self.current_pos[1]].find('G') != -1:
                self.agent_map[self.current_pos[0]][self.current_pos[1]] = self.agent_map[self.current_pos[0]][self.current_pos[1]] + 'G'
            if self.is_begin:
                self.is_begin = False
            else:
                self.score -= 10
        else:
            self.current_pos = self.current_pos
            if 'Shoot' in tmp:
                self.is_shoot = True
                self.shoot_dir = tmp.split(' ')[-1]
                self.score -= 100
            elif 'W' in tmp:
                self.is_scream = True
                wumpus_pos = tmp.split(' ')[-1]
                wumpus_pos = wumpus_pos.replace('(', '').replace(')', '').split(',')
                # get the wumpus position
                wumpus_pos = (int(wumpus_pos[0]), int(wumpus_pos[1]))
                # update wumpus dead
                self.map[int(wumpus_pos[0])][int(wumpus_pos[1])] = '-'
                # update the map
                self.map = new_wumpus.update_map(self.map)
            elif 'U' in tmp or 'L' in tmp or 'R' in tmp or 'D' in tmp:
                self.is_bump = True
                if 'U' in tmp:
                    self.bump_dir = 'up'
                elif 'L' in tmp:
                    self.bump_dir = 'left'
                elif 'R' in tmp:
                    self.bump_dir = 'right'
                elif 'D' in tmp:
                    self.bump_dir = 'down'
                self.agent_map = self.path.pop(0)
            elif 'G' in tmp:
                self.is_collect_gold = True
                self.score += 1000
                if self.agent_map[self.current_pos[0]][self.current_pos[1]] == 'G':
                    self.agent_map[self.current_pos[0]][self.current_pos[1]] = '-'
                    self.map[self.current_pos[0]][self.current_pos[1]] = '-'
                else:
                    self.agent_map[self.current_pos[0]][self.current_pos[1]] = self.agent_map[self.current_pos[0]][self.current_pos[1]].replace('G', '')
                    self.map[self.current_pos[0]][self.current_pos[1]] = self.map[self.current_pos[0]][self.current_pos[1]].replace('G', '')
        self.visited[self.current_pos[0]][self.current_pos[1]] = True

    def draw(self, surface):
        # Draw the border for notification area
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.SCREEN_WIDTH, 50))
        # Draw the border for the map (below the notification area)
        pygame.draw.rect(surface, (0, 0, 0), (0, 50, self.SCREEN_WIDTH, self.SCREEN_HEIGHT - 50))
        # Draw the base map
        for i in range(self.n):
            for j in range(self.n):
                pygame.draw.rect(surface, (255, 255, 255), (self.center_x + j * self.CELL_SIZE, self.center_y + i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 1)
        # Draw the visited cells
        for i in range(self.n):
            for j in range(self.n):
                if self.visited[i][j]:
                    pygame.draw.rect(surface, (200, 200, 200), (self.center_x + j * self.CELL_SIZE + self.CELL_MARGIN, self.center_y + i * self.CELL_SIZE + self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN))
                    text = self.font.render(self.agent_map[i][j], True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (self.center_x + j * self.CELL_SIZE + self.CELL_SIZE / 2, self.center_y + i * self.CELL_SIZE + self.CELL_SIZE / 2)
                    surface.blit(text, text_rect)
                else:
                    pygame.draw.rect(surface, (0, 0, 0), (self.center_x + j * self.CELL_SIZE + self.CELL_MARGIN, self.center_y + i * self.CELL_SIZE + self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN))
                    text = self.font.render('?', True, (255, 255, 255))
                    text_rect = text.get_rect()
                    text_rect.center = (self.center_x + j * self.CELL_SIZE + self.CELL_SIZE / 2, self.center_y + i * self.CELL_SIZE + self.CELL_SIZE / 2)
                    surface.blit(text, text_rect)
        # Draw the current position of the agent (reveal the content of the room)
        pygame.draw.rect(surface, (0, 255, 0), (self.center_x + self.current_pos[1] * self.CELL_SIZE + self.CELL_MARGIN, self.center_y + self.current_pos[0] * self.CELL_SIZE + self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN, self.CELL_SIZE - 2 * self.CELL_MARGIN))
        text = self.font.render(self.agent_map[self.current_pos[0]][self.current_pos[1]], True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.center_x + self.current_pos[1] * self.CELL_SIZE + self.CELL_SIZE / 2, self.center_y + self.current_pos[0] * self.CELL_SIZE + self.CELL_SIZE / 2)
        surface.blit(text, text_rect)
        # Draw the notification (if any)
        if self.is_bump:
            text = self.font.render('Bump ' + self.bump_dir, True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.SCREEN_WIDTH / 2, 25)
            surface.blit(text, text_rect)
            self.is_bump = False
        if self.is_scream:
            text = self.font.render('Argghh', True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.SCREEN_WIDTH / 2, 25)
            surface.blit(text, text_rect)
            self.is_scream = False
        if self.is_shoot:
            text = self.font.render('Shoot ' + self.shoot_dir, True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.SCREEN_WIDTH / 2, 25)
            surface.blit(text, text_rect)
            self.is_shoot = False
        if self.is_collect_gold:
            text = self.font.render('Gold', True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.SCREEN_WIDTH / 2, 25)
            surface.blit(text, text_rect)
            self.is_collect_gold = False
        # Draw the score
        text = self.font.render('Score: ' + str(self.score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.SCREEN_WIDTH - 100, 25)
        surface.blit(text, text_rect)
