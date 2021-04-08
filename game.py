import pygame as pg
from player import Player
from projectile import Projectile


# Création de la classe Game
class Game:

    def __init__(self):

        self.P1 = Player(1,'Marc', 150, 3, 'assets/004-evil.png', 10,5)
        self.P1.pos_start(1)
        self.P2 = Player(2, 'Yoann', 110, 3, 'assets/002-angel.png', 7,2)
        self.P2.pos_start(2)
        self.proj = Projectile('balle de fusil',10,'assets/bullet.png')

        self.pressed = {}


