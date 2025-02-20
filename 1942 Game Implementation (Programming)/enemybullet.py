import math
from bullet import Bullet
import player

class Enemybullet(Bullet):
    """
    This class defines an enemy bullet.
    """
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        # x and y are the coordinates of the displacement vector from the initial position to the player.
        # this direction will only be calculated at the creation of the bullet, therefore, we don't need any properties.
        x = player.player_one.x_pos-self.x_pos
        y = player.player_one.y_pos-self.y_pos
        # we calculate the module in order to calculate the unitary vector
        module = math.sqrt(x**2+y**2)
        # we multiply the vectors by 2 in order to give the bullet more velocity
        self.xdir = x/module *2
        self.ydir = y/module *2

    def move(self):
        """
        This function increments the position using the vectors previously calculated
        """
        self.x_pos += self.xdir
        self.y_pos += self.ydir

enemybulletlist = []

