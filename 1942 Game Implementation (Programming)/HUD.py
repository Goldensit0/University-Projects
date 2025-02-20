import pyxel


class HUD:
    """
    This class will store all the game values such as score, lifes or other relevant parameters.
    """
    def __init__(self):
        self.lifes = 3
        self.score = 0

        self.start = False
        self.framecount = 0
        self.deathframe = 0

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

    # deathframe property and setter
    @property
    def deathframe(self):
        return self.__deathframe

    @deathframe.setter
    def deathframe(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("framecount must be a number")
        else:
            self.__deathframe = value

    # Calculates the real frame_count
    @property
    def realframecount(self):
        """
        This property calculates the real framecount of the program
        """
        realframecount = pyxel.frame_count-self.framecount
        return realframecount

    # lifes property and setter
    @property
    def lifes(self):
        return self.__lifes

    @lifes.setter
    def lifes(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Lifes must be a number")
        else:
            self.__lifes = value

    # score property and setter
    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if type(value) != int and type(value) != float:
            raise TypeError("Score must be a number")
        else:
            self.__score = value


    # start property and setter
    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        if type(value) != bool:
            raise TypeError("Start must be a bool")
        else:
            self.__start = value


hud = HUD()