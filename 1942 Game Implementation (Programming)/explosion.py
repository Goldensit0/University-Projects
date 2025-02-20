import pyxel
import HUD

class Explosion:
    def __init__(self, xpos, ypos, size):
        self.x_pos = xpos
        self.y_pos = ypos

        # Explosions for enemies:
        if size != 0:
            self.adjust = 0
            self.special = False
            # Explosion for bombardiers
            if size == 32:
                self.xsize = 32
                self.ysize = 32
                self.xpos_infile = 64
                self.xpos_infile2 = 134
                self.ypos_infile = 0
            # Explosion for red and regular
            elif size ==16:
                self.xsize = 16
                self.ysize = 16
                self.xpos_infile = 216
                self.xpos_infile2 = 237
                self.ypos_infile = 4
            # Explosion for superbombardiers
            elif size == 48:
                self.xsize = 32
                self.ysize = 32
                self.xpos_infile = 64
                self.xpos_infile2 = 134
                self.ypos_infile = 4
                # Since the plane is bigger, we have to adjust the explosion
                self.adjust = 16

        # Explosion for player
        else:
            self.special = True
            self.xsize = 32
            self.ysize = 32
            self.xpos_infile = 64
            self.xpos_infile2 = 134
            self.ypos_infile = 0

        # We register the moment of the inition of the explosion
        self.framecount = HUD.hud.realframecount

    def draw(self):
        # For enemies
        if not self.special:
            # Sound effects
            if HUD.hud.realframecount-self.framecount == 0:
                # For big enemies
                if self.xsize == 32:
                    pyxel.play(3,4)
                # For small enemies
                else:
                    pyxel.play(3,0)
            # 10 frames of first half of animation
            if HUD.hud.realframecount-self.framecount < 10:
                pyxel.blt(self.x_pos+self.adjust, self.y_pos+self.adjust, 2, self.xpos_infile, self.ypos_infile, self.xsize, self.ysize, colkey=0)
            # 10 frames of second half of animation
            elif HUD.hud.realframecount-self.framecount < 20:
                pyxel.blt(self.x_pos+self.adjust, self.y_pos+self.adjust, 2, self.xpos_infile2, self.ypos_infile, self.xsize, self.ysize, colkey=0)
        # For player
        else:
            # 60 frames of first half of animation (1 sec)
            if HUD.hud.realframecount-self.framecount == 0:
                # Stops the music
                pyxel.stop()
                # Explosion sound
                pyxel.play(3, 4)
            elif HUD.hud.realframecount-self.framecount == 59:
                # Explosion sound
                pyxel.play(3, 4)
            elif HUD.hud.realframecount-self.framecount == 119:
                # Explosion sound
                pyxel.play(3, 4)
            if HUD.hud.realframecount-self.framecount < 60:
                pyxel.blt(self.x_pos, self.y_pos, 2, self.xpos_infile, self.ypos_infile, self.xsize, self.ysize, colkey=0)
            # 60 frames of second half of animation (1 sec)
            elif HUD.hud.realframecount-self.framecount < 120:
                pyxel.blt(self.x_pos, self.y_pos, 2, self.xpos_infile2, self.ypos_infile, self.xsize, self.ysize, colkey=0)


explosions = []