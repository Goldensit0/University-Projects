from plane import Plane
import constants
import random
import pyxel

class Super(Plane):
    """
    This class will contain all the attributes for a superbomber enemy and it's functions
    """
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        # We import these parameters from the constant file
        self.x_pos_infile = constants.superb_xpos
        self.y_pos_infile = constants.superb_ypos
        self.x_size = constants.superb_xsize
        self.y_size = constants.superb_ysize
        # We define hp at 15
        self.hp = 40
        # We start with an initial direction of -1
        self.xdir = -1

    # x dir property and setter
    @property
    def xdir(self):
        return self.__xdir
    @xdir.setter
    def xdir(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Position must be a number")
        else:
            self.__xdir = value

    def move(self):
        # When it's killed, it goes to HEIGHT+100 and stays there
        if self.y_pos == constants.HEIGHT+100:
            pass
        # Superb goes up until the half of the screen
        elif self.y_pos > constants.HEIGHT/2:
            self.y_pos += -1
        elif self.y_pos >= -constants.superb_ysize:
            # Then it starts going left
            # Goes right when reaching left part of the screen
            if self.x_pos == 0:
                self.xdir = +1
            # Goes left when reaching right part of the screen
            if self.x_pos == constants.WIDTH-constants.superb_xsize:
                self.xdir = -1
            # Then it goes up when it reaches half of the screen again
            if self.x_pos == constants.WIDTH/2-constants.superb_xsize+1 and self.xdir == -1:
                self.xdir = 0
            # Goes up until out of the screen
            if self.xdir == 0:
                self.y_pos +=-0.8
            self.x_pos += self.xdir
            # Always slightly going upwards:
            self.y_pos += -0.2
            # random fire
            if random.randint(0,100) >= 99:
                self.fire(self.x_pos,self.y_pos)
        else:
            self.y_pos = constants.HEIGHT+100

    def draw(self):
        """
        This function will be used for the draw function of pyxel.run
        """
        pyxel.blt(self.x_pos, self.y_pos, 1, self.x_pos_infile, self.y_pos_infile, self.x_size, self.y_size, colkey=0)


superb = Super(constants.WIDTH//2-constants.superb_xsize, constants.HEIGHT+constants.superb_ysize)