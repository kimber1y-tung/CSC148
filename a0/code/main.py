"""
This module loads, configures and runs the main game.
"""

from game import Game
from actors import *
from typing import List
import random


def load_map(filename: str) -> List[List[str]]:
    """
    Load the map data from the given filename and return as a list of lists.
    """

    with open(filename) as f:
        map_data = [line.split() for line in f]
    return map_data


if __name__ == "__main__":

    data = load_map("../data/maze0.txt")  # Set the filename where maze data is

    width = len(data[0])
    height = len(data)

    game = Game(width, height)
    player, chaser = None, None

    # Task 0
    # according to the map created, creates the characters of the game (the
    # player, chaser, and wall)
    for i in range(len(data)):
        for j in range(len(data[i])):
            key = data[i][j]
            if key == 'P':
                player = Player("../images/boy-24.png", j, i)
            elif key == 'C':
                chaser = Chaser("../images/ghost-24.png", j, i)
            elif key == 'X':
                game.add_actor(Wall("../images/wall-24.png", j, i))

    game.set_player(player)
    game.add_actor(player)
    game.add_actor(chaser)
    # Set the number of stars the player must collect to win
    game.goal_stars = 5

    # Task 0
    # random creates 8 stars in the game
    # first while loop creates a star in the width and the height of the game
    # second while loop checks if the star created is on top of the actor, then
    # it creates another one

    # Task 3
    num_stars = 0
    while num_stars < 8:
        x = random.randrange(game.stage_width)
        y = random.randrange(game.stage_height)
        act = game.get_actor(x, y)
        while isinstance(act, Actor):
            x = random.randrange(game.stage_width)
            y = random.randrange(game.stage_height)
            act = game.get_actor(x, y)
        game.add_actor(Star("../images/star-24.png", x, y))
        num_stars += 1

    game.on_execute()
