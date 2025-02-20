import board
import pyxel
import constants


                                  ### 1942 ###
                    ### BY SALVADOR AYALA AND ANTONIO VAZQUEZ ###
                            ### CREATED ON DEC 2022 ###
                              ### WITH PYXEL 1.9.6 ###
                                  ### UC3M ###


pyxel.init(constants.WIDTH, constants.HEIGHT, title=constants.CAPTION, fps=constants.FPS, display_scale=constants.SCALE)
pyxel.load("my_resource.pyxres")

pyxel.run(board.update, board.draw)
