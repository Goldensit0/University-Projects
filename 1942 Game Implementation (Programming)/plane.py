import explosion
import pyxel
from explosion import Explosion
import enemybullet
from enemybullet import Enemybullet
class Plane:
    """
    This class will contain all the common attributes of all the enemy planes and player plane.
    """
    def __init__(self, xpos, ypos):
        # Both positions on board have to be updated
        self.x_pos = xpos
        self.y_pos = ypos
        # Size won't change
        self.x_size = 16
        self.y_size = 16
        # Position on file will change when movement change
        self.x_pos_infile = 0
        self.y_pos_infile = 0
        # Health has to be updated
        self.hp = 1
        # This attribute will store the framecount at the start of the loop
        self.framecount = 0

    # framecount property and setter
    @property
    def framecount(self):
        return self.__framecount
    @framecount.setter
    def framecount(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("framecount must be a number")
        else:
            self.__framecount = value

    # x pos property and setter #
    @property
    def x_pos(self):
        return self.__x_pos
    @x_pos.setter
    def x_pos(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__x_pos = value

    # y pos property and setter #
    @property
    def y_pos(self):
        return self.__y_pos
    @y_pos.setter
    def y_pos(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__y_pos = value

    # x pos_infile property and setter #
    @property
    def x_pos_infile(self):
        return self.__x_pos_infile

    @x_pos_infile.setter
    def x_pos_infile(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__x_pos_infile = value

    # y pos_infile property and setter #
    @property
    def y_pos_infile(self):
        return self.__y_pos_infile

    @y_pos_infile.setter
    def y_pos_infile(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__y_pos_infile = value
    # hp property and setter
    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Health must be a number")
        else:
            self.__hp = value

    def damage(self):
        """
        This function damages the plane when asked, lowering health by one and creating an explosion
        """
        self.hp += -1
        if self.hp <= 0:
            explosion.explosions.append(Explosion(self.x_pos, self.y_pos, self.x_size))


    def fire(self, xpos, ypos):
        """
        This function creates a bullet on the enemybulletlist
        """
        enemybullet.enemybulletlist.append(Enemybullet(xpos,ypos))

