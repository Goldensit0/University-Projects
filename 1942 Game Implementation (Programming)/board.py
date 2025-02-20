import bomber
import constants
import enemybullet
import explosion
import player
import regular
import red
import pyxel # made with pyxel 1.9.6
import playerbullet
import superbomber
import collisions
import HUD
import time

def update():
    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()
    # This input will only be available in start screen
    if not HUD.hud.start:
        if pyxel.btnp(pyxel.KEY_RETURN):
            HUD.hud.start = True
            HUD.hud.framecount = pyxel.frame_count
    else:
        # In-game updates
        if player.player_one.hp > 0:
            # The duration of the level is of 55 seconds maximum
            if HUD.hud.realframecount//60 < 55:
                # Player (control toggles off ending the game, when superb killed or out of screen)
                if HUD.hud.realframecount//60 <= 55 and superbomber.superb.y_pos != constants.HEIGHT+100:
                    player.player_one.move()
                # Regular enemies
                for obj in regular.regularenemylist:
                    obj.move()
                # The red enemies appear on screen at second 28
                if HUD.hud.realframecount // 60 >= 28:
                    for obj in red.redlist:
                        obj.move()
                # First bomber appears on screen at second 22
                if HUD.hud.realframecount // 60 >= 22:
                    bomber.bomber1.move()
                # Second bomber appears on screen at second 32
                if HUD.hud.realframecount // 60 >= 32:
                    bomber.bomber2.move()
                # Super bomber appears on screen at second 40
                if HUD.hud.realframecount // 60 >= 40:
                    superbomber.superb.move()
                # Player bullets
                for obj in playerbullet.playerbulletlist:
                    obj.move()
                # Enemy bullets
                for obj in enemybullet.enemybulletlist:
                    obj.move()

                # ROLL ALGORITHM (only when rolls available)
                if player.player_one.rolls > 0:
                    # If Z is pressed and the roll is not already happening
                    if pyxel.btnp(pyxel.KEY_Z) or not player.player_one.not_rolling:
                        # First frame of the roll
                        if player.player_one.framecount == 0:
                            # We set not_rolling=False and we register the time of the start of the roll
                            player.player_one.not_rolling = False
                            player.player_one.framecount = HUD.hud.realframecount
                        # First part of the animation until frame 15
                        elif (HUD.hud.realframecount - player.player_one.framecount) <= 15:
                            player.player_one.x_pos_infile = 16
                        # Second part of the animation until frame 30
                        elif (HUD.hud.realframecount - player.player_one.framecount) <= 30:
                            player.player_one.x_pos_infile = 32
                        # First part of the animation until frame 45
                        elif (HUD.hud.realframecount - player.player_one.framecount) <= 45:
                            player.player_one.x_pos_infile = 48
                        else:
                            # We reset the sprite to the standard sprite
                            player.player_one.x_pos_infile = 0
                            # We reset the framecount
                            player.player_one.framecount = 0
                            # We reset the not_rolling boolean
                            player.player_one.not_rolling = True
                            # We substract one roll of the total
                            player.player_one.rolls += -1

        # If the player is hit/killed:
        else:
            # We register the death moment
            if HUD.hud.deathframe == 0:
                HUD.hud.deathframe = pyxel.frame_count
            # We take the player out of the screen
            player.player_one.x_pos = 500
            # After 5 seconds after death
            if (pyxel.frame_count - HUD.hud.deathframe)//60 >= 5:
                # We reset the health
                player.player_one.hp = 1
                # We substract one life of the total
                HUD.hud.lifes += -1
                # We reset the framecount
                HUD.hud.framecount = pyxel.frame_count
                # We reposition the player in the screen
                player.player_one.x_pos = constants.WIDTH//2 - player.player_one.x_size
                player.player_one.y_pos = constants.HEIGHT-50
                # We clear the deathframe parameter (reset to 0)
                HUD.hud.deathframe = 0




def draw():

    if HUD.hud.start:
        # While lifes are not 0
        if HUD.hud.lifes > 0:
            # We set all the values to default at the start of the game (frame 0)
            if HUD.hud.realframecount == 0:
                pyxel.playm(0, loop=True)
                HUD.hud.deathframe = 0
                regular.regularenemylist = regular.createregular(5, 4)
                red.redlist = red.createred()
                bomber.bomber1 = bomber.Bomber(200, -constants.bombardier_ysize)
                bomber.bomber2 = bomber.Bomber(200, -constants.bombardier_ysize)
                superbomber.superb = superbomber.Super(constants.WIDTH//2-constants.superb_xsize, constants.HEIGHT+constants.superb_ysize)
                explosion.explosions.clear()
                enemybullet.enemybulletlist.clear()
                playerbullet.playerbulletlist.clear()
                HUD.hud.score = 0
                player.player_one.x_pos_infile = 0
                player.player_one.framecount = 0
                player.player_one.not_rolling = True
                player.player_one.rolls = 3
                player.player_one.x_pos = constants.WIDTH//2 - constants.player_xsize
                player.player_one.y_pos = constants.HEIGHT-50


                                    ### DRAWS ###

            # Background animation (more divisions = more fluid animation). Updates every 10 frames.
            # The animation is a basic y_displacement
            if HUD.hud.realframecount % 160 > 140:
                pyxel.bltm(0,0,0,0,0,constants.WIDTH,constants.HEIGHT)
            if HUD.hud.realframecount % 160 > 120:
                pyxel.bltm(0,0,0,0,2,constants.WIDTH,constants.HEIGHT)
            elif HUD.hud.realframecount % 160 > 100:
                pyxel.bltm(0,0,0,0,4,constants.WIDTH,constants.HEIGHT)
            elif HUD.hud.realframecount % 160 > 80:
                pyxel.bltm(0, 0, 0, 0, 6, constants.WIDTH, constants.HEIGHT)
            elif HUD.hud.realframecount % 160 > 60:
                pyxel.bltm(0, 0, 0, 0, 8, constants.WIDTH, constants.HEIGHT)
            elif HUD.hud.realframecount % 160 > 40:
                pyxel.bltm(0, 0, 0, 0, 10, constants.WIDTH, constants.HEIGHT)
            elif HUD.hud.realframecount % 160 > 20:
                pyxel.bltm(0, 0, 0, 0, 12, constants.WIDTH, constants.HEIGHT)
            else:
                pyxel.bltm(0, 0, 0, 0, 14, constants.WIDTH, constants.HEIGHT)

            # Player draw
            pyxel.blt(player.player_one.x_pos, player.player_one.y_pos, 0, player.player_one.x_pos_infile,
                      player.player_one.y_pos_infile, player.player_one.x_size, player.player_one.y_size, colkey=0)

            # All enemy draw
            # Regular enemies
            for obj in regular.regularenemylist:
                obj.draw()
            # First bomber
            bomber.bomber1.draw()
            # Red enemies
            for obj in red.redlist:
                obj.draw()
            # Second bomber
            bomber.bomber2.draw()
            # Superbomber
            superbomber.superb.draw()

            # Player bullets draw
            for obj in playerbullet.playerbulletlist:
                pyxel.blt(obj.x_pos,obj.y_pos,0,36,50,8,8, colkey=0)

            # Enemy bullets draw
            for obj in enemybullet.enemybulletlist:
                pyxel.blt(obj.x_pos,obj.y_pos,0,20,52,8,8, colkey=0)


            # Player collisions (only when not rolling)
            if player.player_one.not_rolling:
                collisions.collision_player()

            # Playerbullet collisions
            collisions.collision_playerbullet()

            # Drawing explosions (after collisions)
            for obj in explosion.explosions:
                obj.draw()


                                    ### DELETIONS ###

            # Out of screen bullet deleter for both enemy and player bullets
            collisions.oos_delet(playerbullet.playerbulletlist)
            collisions.oos_delet(enemybullet.enemybulletlist)

            # Regular enemies deletion and score points:
            deleterlist = []
            for i in range(len(regular.regularenemylist)):
                if regular.regularenemylist[i].hp <= 0:
                    deleterlist.append(i)
            deleterlist.sort(reverse=True)
            for index in deleterlist:
                # Regular enemies give 50 point
                HUD.hud.score += 50
                regular.regularenemylist.pop(index)

            # Red enemies deletion and score points:
            deleterlist = []
            for i in range(len(red.redlist)):
                if red.redlist[i].hp <= 0:
                    deleterlist.append(i)
            deleterlist.sort(reverse=True)
            for index in deleterlist:
                # Red enemies give 100 points
                HUD.hud.score += 100
                red.redlist.pop(index)

            # Bombers deletion and score points:
            if bomber.bomber1.hp <= 0:
                # Bombers give 200 points
                HUD.hud.score += 200
                # We take it out and reset health
                bomber.bomber1.y_pos = constants.HEIGHT+50
                bomber.bomber1.hp = 1
            if bomber.bomber2.hp <= 0:
                # Bombers give 200 points
                HUD.hud.score += 200
                # We take it out and reset health
                bomber.bomber2.y_pos = constants.HEIGHT+50
                bomber.bomber2.hp = 1

            # Superbomber deletion and score points:
            if superbomber.superb.hp <= 0:
                # Superbomber gives 500 points
                HUD.hud.score += 500
                # We take it out and reset health
                superbomber.superb.y_pos = constants.HEIGHT+100
                superbomber.superb.hp = 1


            # Score draw on screen:
            pyxel.text(6, 6, str("Score: " + str(HUD.hud.score)), 0) # Background text for fancier look in black
            pyxel.text(5, 5, str("Score: " + str(HUD.hud.score)), 10) # Actual score on yellow

            # Rolls left draw:
            # First R
            if player.player_one.rolls >= 3:
                pyxel.blt(constants.WIDTH-8*3, constants.HEIGHT-8, 0, 240, 8, 8, 8, colkey= 0)
            # Second R
            if player.player_one.rolls >= 2:
                pyxel.blt(constants.WIDTH-8*2, constants.HEIGHT-8, 0, 240, 8, 8, 8, colkey= 0)
            # Third R
            if player.player_one.rolls >= 1:
                pyxel.blt(constants.WIDTH-8, constants.HEIGHT-8, 0, 240, 8, 8, 8, colkey= 0)

            # Lifes left draw:
            # First Life
            if HUD.hud.lifes >= 3:
                pyxel.blt(constants.WIDTH-12*3, 3, 0, 211, 0, 10, 9, colkey= 0)
            # Second Life
            if HUD.hud.lifes >= 2:
                pyxel.blt(constants.WIDTH-12*2, 3, 0, 211, 0, 10, 9, colkey= 0)
            # Third Life
            if HUD.hud.lifes >= 1:
                pyxel.blt(constants.WIDTH-12, 3, 0, 211, 0, 10, 9, colkey= 0)


            # Winning screen - Activates when timer ends (superB has gone away) or when superB is killed (taken to HEIGHT+100)
            # Only for when player still alive
            if superbomber.superb.y_pos == constants.HEIGHT+100 and player.player_one.hp == 1:
                # Clear bullets for avoiding player getting killed when it can't move after killing the superb
                for object in enemybullet.enemybulletlist:
                    object.y_pos = 500
                if HUD.hud.deathframe == 0:
                    HUD.hud.deathframe = pyxel.frame_count
                # Player goes automatically up
                player.player_one.y_pos += -2
                # Text display
                pyxel.text(81, 161, "YOU WIN!", 0)
                pyxel.text(80, 160, "YOU WIN!", 7)
                pyxel.text(81, 171, str("Score: " + str(HUD.hud.score)), 0)
                pyxel.text(80, 170, str("Score: " + str(HUD.hud.score)), 7)
                # Reset of lifes and start over
                if (pyxel.frame_count - HUD.hud.deathframe) // 60 >= 4:
                    HUD.hud.lifes = 3
                    HUD.hud.start = False


        else:
            # Losing screen

            if HUD.hud.deathframe == 0:
                HUD.hud.deathframe = pyxel.frame_count
            # Text
            pyxel.text(81, 161, "GAME OVER", 0)
            pyxel.text(80, 160, "GAME OVER", 7)
            if (pyxel.frame_count - HUD.hud.deathframe)//60 >= 4:
                HUD.hud.lifes = 3
                HUD.hud.start = False

    else:
        pyxel.stop()
        # Title screen
        pyxel.cls(0)
        # Big title
        pyxel.blt(constants.WIDTH//2-58, constants.HEIGHT//2-27, 0, 88, 88, 120, 48, colkey=0)
        pyxel.blt(constants.WIDTH//2-60, constants.HEIGHT//2-25, 0, 88, 32, 120, 48, colkey=0)
        # Enter to play text. Blinks slightly.
        if HUD.hud.realframecount % 120 <= 90:
            pyxel.text(98,192, "Press Enter to play", 7)




