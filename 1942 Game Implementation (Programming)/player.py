import constants
import explosion
from explosion import Explosion
import playerbullet
import pyxel
from playerbullet import Playerbullet
import HUD


class Player:
    """
    DISCLAIMER: this class is not a subclass of plane due to a circular import error related to bullets.
    Since the fire function is different and others are new, the decision was thought to be even recommended.
    """
    def __init__(self, xpos, ypos):
        # Both positions on board have to be updated
        self.x_pos = xpos
        self.y_pos = ypos
        # We import these parameters from the constant file
        self.x_pos_infile = constants.player_xpos
        self.y_pos_infile = constants.player_ypos
        self.x_size = constants.player_xsize
        self.y_size = constants.player_ysize
        # Health has to be updated
        self.hp = 1
        # Rolls have to ve updated
        self.rolls = 3
        # This attribute will store the framecount at the start of the loop
        self.framecount = 0
        self.not_rolling = True

    # not_rolling property and setter
    @property
    def not_rolling(self):
        return self.__not_rolling

    @not_rolling.setter
    def not_rolling(self, value):
        if type(value) != bool:
            raise TypeError("Start must be a bool")
        else:
            self.__not_rolling = value

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

    # rolls property and setter #
    @property
    def rolls(self):
        return self.__rolls

    @rolls.setter
    def rolls(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__rolls = value

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
        This function damages the plane when asked, lowering health by one
        """
        self.hp += -1
        explosion.explosions.append(Explosion(self.x_pos-self.x_size//2, self.y_pos-self.y_size//2, 0))


    def fire(self, xpos, ypos):
        """
        This function creates a bullet on the playerbulletlist
        """
        playerbullet.playerbulletlist.append(Playerbullet(xpos, ypos))
        pyxel.play(3,1)


    def move(self):
        '''
        This function checks if the arrows of the keyboard are pressed and updates the x and y accordingly.
        It also avoids the plane going out of the screen using booleans that allow the movement in each direction if
        the position has not surpassed a certain value.
        '''
        rightcollider = True
        leftcollider = True
        upcollider = True
        downcollider = True
        if self.x_pos >= constants.WIDTH - 16:
            rightcollider = False
        if self.y_pos >= constants.HEIGHT - 48:
            downcollider = False
        if self.x_pos <= 0:
            leftcollider = False
        if self.y_pos <= constants.HEIGHT // 4:
            upcollider = False
        if pyxel.btn(pyxel.KEY_RIGHT) and rightcollider:
            self.x_pos += 2
        if pyxel.btn(pyxel.KEY_LEFT) and leftcollider:
            self.x_pos += -2
        if pyxel.btn(pyxel.KEY_UP) and upcollider:
            self.y_pos += -3
        if pyxel.btn(pyxel.KEY_DOWN) and downcollider:
            self.y_pos += 3
        if pyxel.btnp(pyxel.KEY_X):
            self.fire(self.x_pos, self.y_pos)


x = constants.WIDTH//2 - constants.player_xsize
y = constants.HEIGHT-50
player_one = Player(x, y)