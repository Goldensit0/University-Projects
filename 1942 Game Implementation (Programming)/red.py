import constants
import math
import pyxel
import random
from plane import Plane
import HUD

class Red(Plane):
    """
    This class will contain all the attributes for a red enemy and it's functions
    """
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        # We import these parameters from the constant file
        self.x_pos_infile = constants.red_xpos
        self.y_pos_infile = constants.red_ypos
        self.x_size = constants.red_xsize
        self.y_size = constants.red_ysize
        # This attribute will tell if the red plane is doing a loop or not
        self.looping = False
        # This attributes will store the center of the loop at the start
        self.center = 0

    # looping property and setter
    @property
    def looping(self):
        return self.__looping

    @looping.setter
    def looping(self, value):
        if type(value) != bool:
            raise TypeError("looping must be a boolean")
        else:
            self.__looping = value

    # center property and setter
    @property
    def center(self):
        return self.__center
    @center.setter
    def center(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("center must be a number")
        else:
            self.__center = value




    def move(self):
        """
        This function will update the position of a red enemy. It will be divided into normal parts and loop parts.
        x pos will always vary, while y pos will only vary when looping
        """

        if self.looping:
            # for circular trajectory, the x and y positions depend on this formula
            # x/y = center_of_the_circle + cos/sen(angular_velocity + initial_angular_position) * radius_of_the_circle
            self.x_pos = self.center + math.cos((HUD.hud.realframecount-self.framecount)/ 16 + math.pi *3/2)* 40
            self.y_pos = 70 + math.sin((HUD.hud.realframecount-self.framecount)/ 16 + math.pi *3/2)* 40
            # red enemies only fire when looking down, when cos tends to 1
            if math.cos((HUD.hud.realframecount-self.framecount)/ 16 + math.pi *3/2) >= 0.99:
                # chance of fire will be defined as a 10%
                if random.randint(0,100) <= 10:
                    self.fire(self.x_pos,self.y_pos)
            # sprite will face up when sin tends to 1
            if math.sin((HUD.hud.realframecount - self.framecount) / 16 + math.pi * 3 / 2) >= 0.99:
                self.x_pos_infile = 0
            # sprite will face right when cos tends to -1
            if math.cos((HUD.hud.realframecount - self.framecount) / 16 + math.pi * 3 / 2) <= -0.99:
                self.x_pos_infile = 16
            # the loop will end then the value of cos is negative and value of sin tends to -1
            if math.cos((HUD.hud.realframecount-self.framecount)/ 16 + math.pi *3/2) < 0 and math.sin((HUD.hud.realframecount-self.framecount)/ 16 + math.pi *3/2) <= -0.99:
                self.looping = False
                self.x_pos = self.center+1
                self.y_pos = 30
        # the loops will be performed at x=60 and x=139
        elif self.x_pos == 60 or self.x_pos == 139:
            self.looping = True
            self.center = self.x_pos
            self.framecount = HUD.hud.realframecount
            # Sprite now facing down
            self.x_pos_infile = 32
        # the red enemies will stop when they go out of the screen
        elif self.x_pos >= constants.WIDTH+2:
            self.x_pos = constants.WIDTH+2
        # the "normal" behaviour is going forward
        else:
            self.x_pos += 2

    def draw(self):
        """
        This function will be used for the draw function of pyxel.run
        """
        pyxel.blt(self.x_pos, self.y_pos, 0, self.x_pos_infile, self.y_pos_infile, self.x_size, self.y_size, colkey=0)



def createred():
    """
    This function creates a list of 5 red enemies and returns it.
    """

    redlist = []

    for i in range(5):
        # Each enemy is separated by 30 pyxels
        x = -16 -30*i
        redlist.append(Red(x ,30))

    return redlist

redlist = createred()