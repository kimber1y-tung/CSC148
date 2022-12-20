from __future__ import annotations
import pygame
from typing import Optional
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
        self.lock = Lock

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
    # _last_event:
    #       keep track of the last key the user pushed down
    # _smooth_move:
    #       represent on/off status for smooth player movement

    x: int
    y: int
    icon: pygame.Surface
    _stars_collected: int
    _last_event: Optional[int]
    _smooth_move: bool

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initialize a Player with the given image <icon_file> at the position
        <x> and <y> on the stage."""

        super().__init__(icon_file, x, y)
        self._stars_collected = 0
        self._last_event = None  # This is used for precise movement
        self._smooth_move = False  # Turn this on for smooth movement

    def set_smooth_move(self, status: bool) -> None:
        """
        Set the <status> of whether or not the player will move smoothly.
        """

        self._smooth_move = status

    def get_star_count(self) -> int:
        """
        Return the number of stars collected.
        """

        return self._stars_collected

    def register_event(self, event: int) -> None:
        """
        Keep track of the last key <event> the user made.
        """

        self._last_event = event

    def move(self, game: 'Game') -> None:
        """
        Move the player on the <game>'s stage based on keypresses.
        """

        evt = self._last_event

        if self._last_event:
            dx, dy = 0, 0
            if self._smooth_move:  # Smooth movement used by the ghost level
                # Task 0
                if game.keys_pressed[pygame.K_LEFT] or \
                        game.keys_pressed[pygame.K_a]:
                    dx -= 1
                if game.keys_pressed[pygame.K_RIGHT] or \
                        game.keys_pressed[pygame.K_d]:
                    dx += 1
                if game.keys_pressed[pygame.K_DOWN] or \
                        game.keys_pressed[pygame.K_s]:
                    dy += 1
                if game.keys_pressed[pygame.K_UP] or \
                        game.keys_pressed[pygame.K_w]:
                    dy -= 1

            else:  # Precise movement used by the squishy monster level
                if evt == pygame.K_LEFT or evt == pygame.K_a:
                    dx -= 1
                if evt == pygame.K_RIGHT or evt == pygame.K_d:
                    dx += 1
                if evt == pygame.K_UP or evt == pygame.K_w:
                    dy -= 1
                if evt == pygame.K_DOWN or evt == pygame.K_s:
                    dy += 1
                self._last_event = None

            new_x, new_y = self.x + dx, self.y + dy

            # i is the actor at point x, y
            i = game.get_actor(new_x, new_y)

            # check if the player moves to a wall or not
            if isinstance(i, Wall):
                return

            # level 1 check
            if isinstance(i, Door) and game.get_level() == 0:
                if game.player.get_star_count() < game.goal_stars:
                    print("Door won't open unless you collect enough stars")
                    return

            # level 2 check
            if isinstance(i, Door) and game.get_level() == 1:
                if game.monster_count != 0:
                    print("Door won't open unless all the monsters are dead")
                    return

            # level 3 check
            if isinstance(i, Key):
                game.key -= 1
                game.remove_actor(i)
            if isinstance(i, Lock):
                if game.key == 0:
                    game.remove_actor(i)
                else:
                    print("Lock won't open unless all keys are collected")
                return

            # checks if the player touches a star
            if isinstance(i, Star):
                self._stars_collected += 1
                game.remove_actor(i)
                # removes the star once the player touches it

            self.x, self.y = new_x, new_y

            if isinstance(i, Box):
                if i.be_pushed(game, dx, dy):
                    return
                else:
                    self.x, self.y = self.x - dx, self.y - dy
                    # player wont go through boxes
                    return


# === Classes for immobile objects === #
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


class Door(Actor):
    """
    A class to represent a Door in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Door cannot move, so do nothing.
        """
        pass


class Key(Actor):
    """
    A class to represent a Key in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Key cannot move, so do nothing.
        """
        pass


class Lock(Actor):
    """
    A class to represent a Lock in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Lock cannot move, so do nothing.
        """
        pass


# === Classes for movable objects === #
class Box(Actor):

    def be_pushed(self, game: 'Game', dx: int, dy: int) -> bool:
        """Move the box in the direction that it is being pushed,
        represented by <dx> and <dy> if the way is not blocked by a wall.
        If there is another box in the way, move both boxes at once.
        If there is a monster in the way, squish the monster.
        Return True if a move was possible, and False otherwise."""

        i = game.get_actor(self.x + dx, self.y + dy)  # gets the actor at x,y
        if isinstance(i, Wall):
            return False  # wont run into walls

        if isinstance(i, Box) or isinstance(i, SquishyMonster):
            # if box
            if isinstance(i, Box):
                j = i.be_pushed(game, dx, dy)
                if j:
                    new_x = dx + self.x
                    new_y = dy + self.y
                    self.x, self.y = new_x, new_y
                return j
            else:  # if monster, kill it
                new_x = dx + self.x
                new_y = dy + self.y
                self.x, self.y = new_x, new_y
                i.die(game)
            return True

        else:  # pushing box at normal
            new_x = dx + self.x
            new_y = dy + self.y
            self.x, self.y = new_x, new_y
            return True

    def move(self, game: 'Game'):
        pass


# === Classes for monsters === #
class Monster(Actor):
    """
    A class to represent monsters that kill the player upon contact.
    """
    # === Private attributes ===
    # _dx:
    #   the horizontal distance this monster will move during each step
    # _dy:
    #   the vertical distance this monster will move during each step
    # _delay:
    #   the speed the monster moves at
    # _delay_count:
    #   used to keep track of the monster's delay in speed
    x: int
    y: int
    icon: pygame.Surface
    _dx: float
    _dy: float
    _delay: int
    _delay_count: int

    def __init__(self, icon_file: str, x: int, y: int, dx: float, dy: float) -> None:
        """Initalize a monster with the given <icon_file> as its image,
        <x> and <y> as its position, and <dx> and <dy> being how much
        it moves by during each animation in the game. The monster also
        has a delay which could optionally be used to slow it down."""

        super().__init__(icon_file, x, y)
        self._dx = dx
        self._dy = dy
        self._delay = 5
        self._delay_count = 1

    def move(self, game: 'Game') -> None:
        """Move the monster by taking one step in its animation."""

        raise NotImplementedError

    def check_player_death(self, game: 'Game') -> None:
        """Make the game over if this monster has hit the player."""

        if game.player is None:
            return
        i = (game.player.x, game.player.y)
        j = (self.x, self.y)
        if i == j:
            game.game_over()


class GhostMonster(Monster):
    """
    A class to represent a ghost in the game who chases the Player.
    """
    x: int
    y: int
    icon: pygame.Surface
    _dx: float
    _dy: float
    _delay: int
    _delay_count: int

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initialize a ghost with the given <icon_file> and <x> and <y>
        as its position."""

        # Set movement with each animation to be 0.5
        super().__init__(icon_file, x, y, 0.5, 0.5)  # uses Monster.__init__

    def move(self, game: 'Game') -> None:
        """
        Move the ghost on the <game>'s screen based on the player's location.
        Check if the ghost has caught the player after each move.
        """

        if game.player.x > self.x:
            self.x += self._dx
        elif game.player.x < self.x:
            self.x -= self._dx
        elif game.player.y > self.y:
            self.y += self._dy
        elif game.player.y < self.y:
            self.y -= self._dy

        self.check_player_death(game)


class SquishyMonster(Monster):
    """
    A class to represent a monster in the game that can kill the player, or
    get squished by a box.
    """
    x: int
    y: int
    icon: pygame.Surface
    _dx: float
    _dy: float
    _delay: int
    _delay_count: int

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initalize a monster with the given <icon_file> and <x> and <y>
        as its position."""

        # Set movement with each animation to be 1 step
        super().__init__(icon_file, x, y, 1, 1)  # uses Monster.__init__

    def move(self, game: 'Game') -> None:
        """
        Move one step, if possible. If the way is blocked, bounce back in
        the opposite direction. After each move, check if the player has been
        hit.
        """

        if self._delay_count == 0:  # delay the monster's movement
            i = game.get_actor(self.x + self._dx, self.y + self._dy)
            if isinstance(i, Wall) or isinstance(i, Box):
                self._dx = -1 * self._dx
                self._dy = -1 * self._dy
            else:
                self.x += self._dx
                self.y += self._dy

        self._delay_count = (self._delay_count + 1) % self._delay
        self.check_player_death(game)

    def die(self, game: 'Game') -> None:
        """Remove this monster from the <game>."""

        i = game.get_actor(self.x, self.y)
        if isinstance(i, SquishyMonster):
            game.remove_actor(i)
            game.monster_count -= 1


class Devil(Monster):
    x: int
    y: int
    icon: pygame.Surface
    _dx: float
    _dy: float
    _delay: int
    _delay_count: int

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initalize a monster with the given <icon_file> and <x> and <y>
        as its position."""

        # Set movement with each animation to be 1 step
        super().__init__(icon_file, x, y, 1, 1) # uses Monster.__init__

    def move(self, game: 'Game') -> None:
        """
        Move one step, if possible. If the way is blocked, bounce back in
        the opposite direction. After each move, check if the player has been
        hit.
        """

        if self._delay_count == 0:  # delay the monster's movement
            i = game.get_actor(self.x + self._dx, self.y + self._dy)
            if isinstance(i, Wall) or isinstance(i, Box) or \
                    isinstance(i, Devil):
                self._dx = -1 * self._dx
                self._dy = -1 * self._dy
            else:
                self.x += self._dx
                self.y += self._dy

        self._delay_count = (self._delay_count + 1) % self._delay
        self.check_player_death(game)

    def die(self, game: 'Game') -> None:
        """Remove this Devil from the <game>."""

        i = game.get_actor(self.x, self.y)
        if isinstance(i, Devil):
            game.remove_actor(i)
            game.monster_count -= 1

