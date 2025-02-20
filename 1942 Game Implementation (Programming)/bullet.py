class Bullet:
    """
    This class contains the basic positions and their properties and setters
    """
    def __init__(self, xpos, ypos):
        self.x_size = 8
        self.y_size = 8
        # pos has to be updated
        self.x_pos = xpos + self.x_size//2
        self.y_pos = ypos
        # Health has to be updated
        self.hp = 1


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
        This function damages the bullet when asked, deleting it by taking it out of screen
        """
        self.x_pos = 500