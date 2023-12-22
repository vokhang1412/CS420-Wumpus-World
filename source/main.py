import sys
sys.path.insert(0, './gui')
sys.path.insert(0, './solvers')
sys.path.insert(0, './map')

from gui import game

if __name__ == '__main__':
    game.Game().run()