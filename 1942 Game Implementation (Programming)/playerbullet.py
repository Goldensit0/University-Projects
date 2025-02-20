from bullet import Bullet

class Playerbullet(Bullet):
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)

    def move(self):
        """
        This function makes the bullet travell through the screen at a velocity of 4 pyxels.
        """
        self.y_pos += -4

playerbulletlist = []