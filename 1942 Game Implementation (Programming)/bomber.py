import constants
from plane import Plane
import random
import pyxel

class Bomber(Plane):
    """
    This class will contain all the attributes for a bomber enemy and it's functions
    """
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        # We import these parameters from the constant file
        self.x_pos_infile = constants.bombardier_xpos
        self.y_pos_infile = constants.bombardier_ypos
        self.x_size = constants.bombardier_xsize
        self.y_size = constants.bombardier_ysize
        self.hp = 20

    def move(self):
        """
        This function defines the movement of the bomber.
        """
        if constants.HEIGHT*3/4 >= self.y_pos >= constants.HEIGHT/2:
            self.x_pos += 1
            self.y_pos += 0.5
            # The sprite faces right
            self.x_pos_infile = 104
            self.y_pos_infile = 32
            if random.randint(0,100) >= 99:
                self.fire(self.x_pos+16,self.y_pos+16) # enhancing correction
        elif constants.HEIGHT/2 >= self.y_pos >= constants.HEIGHT*1/4:
            self.x_pos += -1
            self.y_pos += 0.5
            #The sprite faces left
            self.x_pos_infile = 160
            self.y_pos_infile = 0
            if random.randint(0,100) >= 99:
                self.fire(self.x_pos-8,self.y_pos+8) # enhancing correction
        elif self.y_pos <= constants.HEIGHT+self.y_size:
            self.y_pos += 1
            # The sprite faces down (normal state)
            self.x_pos_infile = constants.bombardier_xpos
            self.y_pos_infile = constants.bombardier_ypos

    def draw(self):
        """
        This function will be used for the draw function of pyxel.run
        """
        pyxel.blt(self.x_pos, self.y_pos, 1, self.x_pos_infile, self.y_pos_infile, self.x_size, self.y_size, colkey=0)

bomber1 = Bomber(200, -constants.bombardier_ysize)
bomber2 = Bomber(200, -constants.bombardier_ysize)

