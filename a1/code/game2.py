from __future__ import annotations
from typing import Optional, List
from actors2 import *
import pygame
import random

LEVEL_MAPS = ["maze1.txt", "maze3.txt", "final_maze.txt"]


def load_map(filename: str) -> List[List[str]]:
    """
    Load the map data from the given filename and return as a list of lists.
    """

    with open(filename) as f:
        map_data = [line.split() for line in f]
    return map_data


class Game:
    """
    This class represents the main game.
    === Public Attributes ===
    screen: the screen of the game
    stage_width: width of the game
    stage_height: height of the game
    size: the resolution of the game
    player: the player in the game (an instance of the Player class)
    keys_pressed: the keys pressed to move the player
    goal_message: a string at the bottom of the game and states the rules to win
    goal_stars: the number of stars need to collect to win the game (level 0)
    monster_count: the number of squishy monsters (level 1)
    key: the number of keys (level 2)

    === Private Attributes ===
    _running: a boolean to represent if the game is running
    _actors: a list of all the elements in the game
    _level: current level that the game is in
    _max_level: max level of the game

    === Representation Invariants ===
    None
    """
    _running: bool
    _level: int
    _max_level: int
    screen: pygame.Surface
    player: Player
    keys_pressed: tuple

    _actors: list
    stage_width: int
    stage_height: int
    size: tuple
    goal_message: str

    goal_stars: int
    monster_count: int
    key: int

    def __init__(self) -> None:
        """
        Initialize a game that has a display screen and game actors.
        """

        self._running = False
        self._level = 0  # Current level that the game is in
        self._max_level = len(LEVEL_MAPS) - 1
        self.screen = None
        self.player = None
        self.keys_pressed = None

        # Attributes that get set during level setup
        self._actors = None
        self.stage_width, self.stage_height = 0, 0
        self.size = None
        self.goal_message = None

        # Attributes that are specific to certain levels
        self.goal_stars = 0  # Level 0
        self.monster_count = 0  # Level 1
        self.key = 4  # Level 2

        # Method that takes care of level setup
        self.setup_current_level()

    def get_level(self) -> int:
        """
        Return the current level the game is at.
        """

        return self._level

    def set_player(self, player: Player) -> None:
        """
        Set the game's player to be the given <player> object.
        """

        self.player = player

    def add_actor(self, actor: Actor) -> None:
        """
        Add the given <actor> to the game's list of actors.
        """

        self._actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        """
        Remove the given <actor> from the game's list of actors.
        """

        self._actors.remove(actor)

    def get_actor(self, x: int, y: int) -> Optional[Actor]:
        """
        Return the actor object that exists in the location given by
        <x> and <y>. If no actor exists in that location, return None.
        """

        for i in self._actors:
            if i.x == x and i.y == y:
                return i

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """

        pygame.init()
        self.screen = pygame.display.set_mode \
            (self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event: pygame.Event) -> None:
        """
        React to the given <event> as appropriate.
        """

        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self.player.register_event(event.key)

    def game_won(self) -> bool:
        """
        Return True iff the game has been won, according to the current level.
        """
        i = self.get_actor(self.player.x, self.player.y)
        # Task 0
        if self._level == 0:
            if self.player.get_star_count() >= self.goal_stars:
                return True
            else:
                return False
        if self._level == 1:
            if self.monster_count == 0:  # change back to == 0
                return True
            else:
                return False
        if self._level == 2:
            if self.key == 0 and isinstance(i, Door):  # change back to == 0
                return True
            else:
                return False

    def on_loop(self) -> None:
        """
        Move all actors in the game as appropriate.
        Check for win/lose conditions and stop the game if necessary.
        """

        self.keys_pressed = pygame.key.get_pressed()
        for actor in self._actors:
            actor.move(self)

        # check if it is none first
        if self.player is None:
            print("You lose! :( Better luck next time.")
            self._running = False
            return

        i = self.get_actor(self.player.x, self.player.y)

        if self.game_won() and isinstance(i, Door):
            if self._level == self._max_level:
                print("Congratulations, you won!")
                self._running = False
            else:
                self._level += 1
                self.setup_current_level()

    def on_render(self) -> None:
        """
        Render all the game's elements onto the screen.
        """

        self.screen.fill(BLACK)
        for a in self._actors:
            rect = pygame.Rect(a.x * ICON_SIZE, a.y * ICON_SIZE, ICON_SIZE, ICON_SIZE)
            self.screen.blit(a.icon, rect)

        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(self.goal_message, True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.center = (self.stage_width * ICON_SIZE // 2,
                           (self.stage_height + 0.5) * ICON_SIZE)
        self.screen.blit(text, textRect)

        pygame.display.flip()

    def on_cleanup(self) -> None:
        """
        Clean up and close the game.
        """

        pygame.quit()

    def on_execute(self) -> None:
        """
        Run the game until the game ends.
        """

        self.on_init()

        while self._running:
            pygame.time.wait(100)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def game_over(self) -> None:
        """
        Set the game as over (remove the player from the game).
        """

        self.player = None

    def setup_current_level(self):
        """
        Set up the current level of the game.
        """

        data = load_map("../data/"+LEVEL_MAPS[self._level])
        # Set the file where maze data is stored
        if self._level == 0:
            self.setup_ghost_game(data)
        elif self._level == 1:
            self.setup_squishy_monster_game(data)
        elif self._level == 2:
            self.setup_level3_game(data)

    def setup_ghost_game(self, data) -> None:
        """
        Set up a game with a ghost that chases the player, and stars to collect.
        """

        w = len(data[0])
        h = len(
            data) + 1  # We add a bit of space for the text at the bottom

        self._actors = []
        self.stage_width, self.stage_height = w, h-1
        self.size = (w * ICON_SIZE, h * ICON_SIZE)

        player, chaser = None, None

        for i in range(len(data)):
            for j in range(len(data[i])):
                key = data[i][j]
                if key == 'P':
                    player = Player("../images/boy-24.png", j, i)
                elif key == 'C':
                    chaser = GhostMonster("../images/ghost-24.png", j, i)
                elif key == 'X':
                    self.add_actor(Wall("../images/wall-24.png", j, i))
                elif key == 'D':
                    self.add_actor(Door("../images/door-24.png", j, i))

        self.set_player(player)
        self.add_actor(player)
        player.set_smooth_move(True)  # Enable smooth movement for player
        self.add_actor(chaser)
        # Set the number of stars the player must collect to win
        self.goal_stars = 5  # original is set to 5
        self.goal_message = "Objective: Collect {}".format(self.goal_stars) + \
                            " stars before the ghost gets you and head for " \
                            "the door"

        # Draw stars
        num_stars = 0
        while num_stars < 7:
            x = random.randrange(self.stage_width)
            y = random.randrange(self.stage_height)
            # Task 0
            # Make sure the stars never appear on top of another actor
            act = self.get_actor(x, y)
            while isinstance(act, Actor):
                x = random.randrange(self.stage_width)
                y = random.randrange(self.stage_height)
                act = self.get_actor(x, y)
            self.add_actor(Star("../images/star-24.png", x, y))
            num_stars += 1

    def setup_squishy_monster_game(self, data) -> None:
        """
        Set up a game with monsters that the player must squish with boxes.
        """

        w = len(data[0])
        h = len(
            data) + 1  # We add a bit of space for the text at the bottom

        self._actors = []
        self.stage_width, self.stage_height = w, h-1
        self.size = (w * ICON_SIZE, h * ICON_SIZE)
        self.goal_message = "Objective: Squish all the monsters with the "\
                            + " boxes and head for the door"

        player = None

        for i in range(len(data)):
            for j in range(len(data[i])):
                key = data[i][j]
                if key == 'P':
                    player = Player("../images/boy-24.png", j, i)
                elif key == 'M':
                    self.add_actor(SquishyMonster("../images/monster-24.png", j, i))
                    self.monster_count += 1
                elif key == 'X':
                    self.add_actor(Wall("../images/wall-24.png", j, i))
                elif key == 'D':
                    self.add_actor(Door("../images/door-24.png", j, i))

        self.set_player(player)
        self.add_actor(player)

        # Draw boxes
        num_boxes = 0
        while num_boxes < 12:
            x = random.randrange(self.stage_width)
            y = random.randrange(self.stage_height)

            # Make sure the boxes never appear on top of another actor
            act = self.get_actor(x, y)
            while isinstance(act, Actor):
                x = random.randrange(self.stage_width)
                y = random.randrange(self.stage_height)
                act = self.get_actor(x, y)
            self.add_actor(Box("../images/box-24.png", x, y))
            num_boxes += 1

    def setup_level3_game(self, data) -> None:
            """
            Set up a game with monsters, the player must collect all the keys
            to open a lock and get to the door
            """

            w = len(data[0])
            h = len(
                data) + 1  # We add a bit of space for the text at the bottom

            self._actors = []
            self.stage_width, self.stage_height = w, h-1
            self.size = (w * ICON_SIZE, h * ICON_SIZE)
            self.goal_message = "Objective: without touching devils, " \
                                "grab all keys to open lock and head " \
                                "for the door"

            player = None

            for i in range(len(data)):
                for j in range(len(data[i])):
                    key = data[i][j]
                    if key == 'P':
                        player = Player("../images/boy-24.png", j, i)
                    elif key == 'M':
                        self.add_actor(
                            Devil("../images/devil-24.png", j, i))
                    elif key == 'X':
                        self.add_actor(Wall("../images/wall-24.png", j, i))
                    elif key == 'D':
                        self.add_actor(Door("../images/door-24.png", j, i))
                    elif key == 'L':
                        self.add_actor(Lock("../images/lock-24.png", j, i))

            self.set_player(player)
            self.add_actor(player)

            num_key = 0
            while num_key < 4:
                x = random.randrange(self.stage_width)
                y = random.randrange(self.stage_height)

                # Make sure keys never appear on top of another actor
                act = self.get_actor(x, y)
                while isinstance(act, Actor):
                    x = random.randrange(self.stage_width)
                    y = random.randrange(self.stage_height)
                    act = self.get_actor(x, y)
                self.add_actor(Key("../images/key-24.png", x, y))
                num_key += 1


