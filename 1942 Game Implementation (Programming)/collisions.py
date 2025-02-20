import math

import constants
import playerbullet
import enemybullet

import regular
import red
import bomber
import superbomber

import player


def oos_delet(list):
    """
    This function will check if the bullet is still on screen, if not it will be deleted.
    """
    counter = 0
    bulletdeleter = []
    # We locate all the bullets out of the screen
    for bullet in list:
        if bullet.y_pos < 0 or bullet.y_pos > constants.HEIGHT or bullet.x_pos < 0 or bullet.x_pos > constants.WIDTH:
            bulletdeleter.append(counter)
        counter += 1

    # We sort the list from the back
    bulletdeleter.sort(reverse=True)

    # We delete out of screen bullets
    for number in bulletdeleter:
        list.pop(number)

def distance_calculator(obj1, obj2):
    """
    This function calculates de distance between 2 objects. Will be used to determine collisions
    """
    # We define the center of the two objects
    center1 = obj1.x_pos+obj1.x_size//2 , obj1.y_pos+obj1.y_size//2
    center2 = obj2.x_pos+obj2.x_size//2 , obj2.y_pos+obj2.y_size//2

    # We calculate the distance using the module of the displacement vector from center1 to center2
    distance = math.sqrt((center2[0]-center1[0])**2+(center2[1]-center1[1])**2)

    return distance


def collision_player():
    """
    This function checks the collisions of the player with the enemy bullets and planes
    """
    # For bullets
    for bullet in enemybullet.enemybulletlist:
        # Calculating distance
        distance = distance_calculator(bullet, player.player_one)
        # If one over another, both take damage
        if distance < (bullet.x_size//2+player.player_one.x_size//2):
            player.player_one.damage()
            bullet.damage()
    # For regular enemies
    for enemy in regular.regularenemylist:
        # Calculating distance
        distance = distance_calculator(enemy, player.player_one)
        # If one over another, both take damage
        if distance < (enemy.x_size//2+player.player_one.x_size//2):
            player.player_one.damage()
            enemy.damage()
    # For red enemies
    for enemy in red.redlist:
        # Calculating distance
        distance = distance_calculator(enemy, player.player_one)
        # If one over another, both take damage
        if distance < (enemy.x_size // 2 + player.player_one.x_size // 2):
            player.player_one.damage()
            enemy.damage()
    # For bombers
    # Calculating distance
    distance = distance_calculator(bomber.bomber1, player.player_one)
    # If one over another, both take damage
    if distance < (bomber.bomber1.x_size // 2 + player.player_one.x_size // 2):
        player.player_one.damage()
        bomber.bomber1.damage()
    # Calculating distance
    distance = distance_calculator(bomber.bomber2, player.player_one)
    # If one over another, both take damage
    if distance < (bomber.bomber2.x_size // 2 + player.player_one.x_size // 2):
        player.player_one.damage()
        bomber.bomber2.damage()
    # For superbomber
    # Calculating distance
    distance = distance_calculator(superbomber.superb, player.player_one)
    # If one over another, both take damage
    if distance < (superbomber.superb.x_size // 2 + player.player_one.x_size // 2):
        player.player_one.damage()
        superbomber.superb.damage()

def collision_playerbullet():
    """
    This function checks the collisions of the player bullets with the enemy planes
    """
    for bullet in playerbullet.playerbulletlist:
        # For regular enemies
        for enemy in regular.regularenemylist:
            distance = distance_calculator(enemy, bullet)
            # If one over another, both take damage
            if distance < (enemy.x_size//2+bullet.x_size//2):
                bullet.damage()
                enemy.damage()
        # For red enemies
        for enemy in red.redlist:
            distance = distance_calculator(enemy, bullet)
            # If one over another, both take damage
            if distance < (enemy.x_size // 2 + bullet.x_size // 2):
                bullet.damage()
                enemy.damage()
        # For bombers
        distance = distance_calculator(bomber.bomber1, bullet)
        # If one over another, both take damage
        if distance < (bomber.bomber1.x_size // 2 + bullet.x_size // 2):
            bullet.damage()
            bomber.bomber1.damage()
        distance = distance_calculator(bomber.bomber2, bullet)
        # If one over another, both take damage
        if distance < (bomber.bomber2.x_size // 2 + bullet.x_size // 2):
            bullet.damage()
            bomber.bomber2.damage()
        # For superbomber
        distance = distance_calculator(superbomber.superb, bullet)
        # If one over another, both take damage
        if distance < (superbomber.superb.x_size // 2 + bullet.x_size // 2):
            bullet.damage()
            superbomber.superb.damage()


