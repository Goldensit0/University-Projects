import random
import constants
from plane import Plane
import pyxel

class Regular(Plane):
    """
    This class will contain all the attributes for a regular enemy and it's functions
    """
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        # We import these parameters from the constant file
        self.x_pos_infile = constants.regular_xpos
        self.y_pos_infile = constants.regular_ypos
        self.x_size = constants.regular_xsize
        self.y_size = constants.regular_ysize
        # x velocity. This parameter will only be set at the creation of the object
        # if the object is at the left part of the screen, the velocity will be positive, otherwise, negative.
        if self.x_pos < (constants.WIDTH//2 + self.x_size):
            self.x_velocity = 0.3
        else:
            self.x_velocity = -0.3
        # goingback will control if the plane has turned or not
        self.goingback = False

    # goingback property and setter
    @property
    def goingback(self):
        return self.__goingback
    @goingback.setter
    def goingback(self, value):
        if type(value) != bool:
            raise TypeError("goingback must be a boolean")
        else:
            self.__goingback = value

    def move(self):
        """
        This function will update the position of a regular enemy. x velocity will be constant
        while y velocity will vary. It also defines fire when turning.
        """
        # x velocity is constant, although it will only move when the plane enters the screen
        if -16 <= self.y_pos <= constants.HEIGHT+self.y_size:
            self.x_pos += self.x_velocity
        # y velocity depends on y_pos
        # If the plane is already going back, the velocity will be negative
        if self.goingback:
            # If the plane has already gone out of the screen from above, it should stop moving, so we move it down the screen.
            # We also turn False "turningback" so the plane stops going upwards
            if self.y_pos < -self.y_size:
                self.y_pos = constants.HEIGHT+1
                self.goingback = False
            else: self.y_pos += -2
        # If not, it must continue going further until it reaches the half of the screen
        elif self.y_pos < constants.HEIGHT // 2:
                self.y_pos += 2
        elif self.y_pos < constants.HEIGHT:
            # We define the chances of firing and turning in a 15%
            if random.randint(1, 100) < 5:
                self.fire(self.x_pos,self.y_pos)
                self.goingback = True
                # updates the sprite
                self.x_pos_infile = 0
            # If not, it must continue going further
            else:
                self.y_pos += 2
        # If the enemy has gone out of the screen, it should not move anymore
        else:
            self.y_pos = self.y_pos

    def draw(self):
        """
        This function will be used for the draw function of pyxel.run
        """
        pyxel.blt(self.x_pos, self.y_pos, 0, self.x_pos_infile, self.y_pos_infile, self.x_size, self.y_size, colkey=0)


def createregular(x, y):
    """
    This function creates a list of x waves of y enemies regular enemies for each and returns it.
    """

    regularlist = []

    for i in range(x):
        checker = []
        for j in range(y):
            # The x pos is defined as a random position that does not overlap with the previous ones in the wave
            # For that, we use a list checker
            x_pos = constants.WIDTH // 10 * random.randint(0, 9)
            while x_pos in checker:
                x_pos = constants.WIDTH // 10 * random.randint(0, 9)
            checker.append(x_pos)
            # The y pos will be all the same for the wave, above the screen and each wave divided by 600 pyxels
            y_pos = -300 -500*i

            regularlist.append(Regular(x_pos, y_pos))

    return regularlist

# We create a regular enemy list made of 5 waves of 4 enemies for each
regularenemylist = createregular(5, 4)

