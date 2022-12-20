from __future__ import annotations
import pygame
from settings import *


class Actor:
    """
    A class to represent all the game's actors. This class includes any
    attributes/methods that every actor in the game must have.

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    x:
        x coordinate of this actor's location on the stage
    y:
        y coordinate of this actor's location on the stage
    icon:
        the image representing this actor
    """
    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, icon_file, x, y):
        """Initialize an actor with the given image <icon_file> and the
        given <x> and <y> position on the game's stage.
        """

        self.x, self.y = x, y
        self.icon = pygame.image.load(icon_file)

    def move(self, game: 'Game') -> None:
        """Move this actor by taking one step of its animation."""

        raise NotImplementedError


class Player(Actor):
    """
    A class to represent a Player in the game.
    """
    # === Private Attributes ===
    # _stars_collected:
    #       the number of stars the player has collected so far
    x: int
    y: int
    icon: pygame.Surface
    _stars_collected: int

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initalize a Player with the given image <icon_file> at the position
        <x> and <y> on the stage."""

        super().__init__(icon_file, x, y)
        self._stars_collected = 0

    def move(self, game: 'Game') -> None:
        """
        Move the player on the <game>'s stage based on keypresses.
        """

        new_x, new_y = self.x, self.y

        # Task 1
        if game.keys_pressed[pygame.K_LEFT] or game.keys_pressed[pygame.K_a]:
            new_x -= 1
        if game.keys_pressed[pygame.K_RIGHT] or game.keys_pressed[pygame.K_d]:
            new_x += 1
        if game.keys_pressed[pygame.K_DOWN] or game.keys_pressed[pygame.K_s]:
            new_y += 1
        if game.keys_pressed[pygame.K_UP] or game.keys_pressed[pygame.K_w]:
            new_y -= 1

        # i is the actor at point x, y
        i = game.get_actor(new_x, new_y)

        # Task 2
        # check if the player moves to a wall or not
        if isinstance(i, Wall):
            return

        # Task 4
        # check if the player touches a star
        if isinstance(i, Star):
            self._stars_collected += 1
            game.remove_actor(i)  # removes the star once the player touches it

        self.x, self.y = new_x, new_y

    def has_won(self, game: 'Game') -> bool:
        """Return True iff the game has been won."""

        # Task 5
        if self._stars_collected == game.goal_stars:
            return True


class Chaser(Actor):
    """
    A class to represent a Chaser in the game who chases the Player.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        Move the chaster on the <game>'s stage based on the player's location.
        """

        if game.player.x > self.x:
            self.x += 0.5
        elif game.player.x < self.x:
            self.x -= 0.5
        elif game.player.y > self.y:
            self.y += 0.5
        elif game.player.y < self.y:
            self.y -= 0.5

        # Task 6
        # check if the Chaser has touched the Player and if so, make it
        # [game over] using the appropriate method from the game object
        if game.player.x == self.x and game.player.y == self.y:
            game.game_over()


class Star(Actor):
    """
    A class to represent a Star in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Star cannot move, so do nothing.
        """

        pass


class Wall(Actor):
    """
    A class to represent a Wall in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Wall cannot move, so do nothing.
        """

        pass


