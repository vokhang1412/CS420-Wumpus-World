from display import Displayer

class Game:
    def __init__(self):
        self.displayer = None
        self.map_name = ''

    def run(self):
        self.map_name = input('Enter map name: ')
        self.displayer = Displayer(self.map_name)
        self.displayer.run()