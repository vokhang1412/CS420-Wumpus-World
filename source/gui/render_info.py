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
        self.to_solve_map = self.map.copy()
        tmp, self.path, self.score = new_wumpus.solve_wumpus_world(self.to_solve_map)
        self.current_pos = (0, 0)
        for i in range(len(self.path)):
            for j in range(len(self.path[i])):
                if self.map[i][j] == 'A':
                    self.current_pos = (i, j)
        self.visited[self.current_pos[0]][self.current_pos[1]] = True
        self.is_bump = False
        self.is_scream = False
        self.is_shoot = False
        self.is_collect_gold = False
        self.bump_dir = ''
        self.shoot_dir = ''
        self.font = pygame.font.SysFont('Arial', 20)


    # [(2, 1), (1, 1), 'G(1, 1)', (2, 1), (3, 1), (2, 1), (2, 0), (2, 1), (2, 2), (2, 1), (1, 1), 'Shoot the arrow up', 'Shoot the arrow left', 'W (1, 0)', (2, 1), (2, 0), (1, 0), (0, 0), 'U(0, 0)', 'L(0, 0)', (0, 1), (0, 2), (0, 1), (1, 1), (2, 1), (3, 1), (3, 0)]
    # This is an example of the path returned by the solver. It is a list of tuples and strings.
    # Tuples are coordinates, strings are actions.
    # If the room is not visited, it will be rendered as a '?' with a black background.
    # If the room is visited, it will be rendered as the content of the room with a light gray background.
    # If 'Shoot' is in the item, a note "Shoot <Dir>" will be rendered on the screen.
    # If 'W' is in the item, a note "Argghh" will be rendered on the screen.
    # If 'U, L, R, D' is in the item, a note "Wall <Dir>" will be rendered on the screen.
    # If 'G' is in the item, a note "Gold" will be rendered on the screen.
    # The position of the agent will be rendered with light green background, with the content of the room.
        
    def update_next_step(self):
        if len(self.path) == 0:
            return
        tmp = self.path.pop(0)
        if type(tmp) == tuple:
            self.current_pos = tmp
        else:
            self.current_pos = self.current_pos
            if 'Shoot' in tmp:
                self.is_shoot = True
                self.shoot_dir = tmp.split(' ')[-1]
            elif 'W' in tmp:
                self.is_scream = True
                # get the position of the wumpus
                wumpus_pos = tuple(tmp[2:-1].split(', '))
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
            elif 'G' in tmp:
                self.is_collect_gold = True
                if self.map[self.current_pos[0]][self.current_pos[1]] == 'G':
                    self.map[self.current_pos[0]][self.current_pos[1]] = '-'
                else:
                    self.map[self.current_pos[0]][self.current_pos[1]].remove('G')
                self.map = new_wumpus.update_map(self.map)
        self.visited[self.current_pos[0]][self.current_pos[1]] = True

    def draw(self, surface):
        # Draw the background of each cell
        for row in range(self.n):
            for col in range(self.n):
                color = (0, 0, 0)
                if self.visited[row][col]:
                    color = (200, 200, 200)
                pygame.draw.rect(surface, color, [(self.CELL_MARGIN + self.CELL_SIZE) * col + self.CELL_MARGIN,
                                                   (self.CELL_MARGIN + self.CELL_SIZE) * row + self.CELL_MARGIN,
                                                   self.CELL_SIZE,
                                                   self.CELL_SIZE])
        # Draw the content of each cell
        for row in range(self.n):
            for col in range(self.n):
                if self.visited[row][col]:
                    text = self.font.render(self.map[row][col], True, (0, 0, 0))
                    surface.blit(text, [(self.CELL_MARGIN + self.CELL_SIZE) * col + self.CELL_MARGIN,
                                        (self.CELL_MARGIN + self.CELL_SIZE) * row + self.CELL_MARGIN])
        # Draw the agent
        color = (0, 255, 0)
        pygame.draw.rect(surface, color, [(self.CELL_MARGIN + self.CELL_SIZE) * self.current_pos[1] + self.CELL_MARGIN,
                                           (self.CELL_MARGIN + self.CELL_SIZE) * self.current_pos[0] + self.CELL_MARGIN,
                                           self.CELL_SIZE,
                                           self.CELL_SIZE])
        # Draw the notes (if any)
        if self.is_bump:
            text = self.font.render('Wall ' + self.bump_dir, True, (0, 0, 0))
            surface.blit(text, [self.SCREEN_WIDTH - 200, 0])
            self.is_bump = False
        if self.is_scream:
            text = self.font.render('Argghh', True, (0, 0, 0))
            surface.blit(text, [self.SCREEN_WIDTH - 200, 0])
            self.is_scream = False
        if self.is_shoot:
            text = self.font.render('Shoot ' + self.shoot_dir, True, (0, 0, 0))
            surface.blit(text, [self.SCREEN_WIDTH - 200, 0])
            self.is_shoot = False
        if self.is_collect_gold:
            text = self.font.render('Gold Collected', True, (0, 0, 0))
            surface.blit(text, [self.SCREEN_WIDTH - 200, 0])
            self.is_collect_gold = False
        # Draw the cover for unvisited cells
        for row in range(self.n):
            for col in range(self.n):
                if not self.visited[row][col]:
                    color = (0, 0, 0)
                    pygame.draw.rect(surface, color, [(self.CELL_MARGIN + self.CELL_SIZE) * col + self.CELL_MARGIN,
                                                       (self.CELL_MARGIN + self.CELL_SIZE) * row + self.CELL_MARGIN,
                                                       self.CELL_SIZE,
                                                       self.CELL_SIZE])
                    text = self.font.render('?', True, (255, 255, 255))
                    surface.blit(text, [(self.CELL_MARGIN + self.CELL_SIZE) * col + self.CELL_MARGIN,
                                        (self.CELL_MARGIN + self.CELL_SIZE) * row + self.CELL_MARGIN])
                    
