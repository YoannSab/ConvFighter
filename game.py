import pygame as pg
from player import Player
from projectile import Projectile


# Création de la classe Game
class Game:

    def __init__(self):

        self.proj1 = Projectile('balle de fusil',10,'assets/bullet.png')
        self.proj2 = Projectile('balle de fusil2', 10, 'assets/bullet2.png')
        self.P1 = Player(1,'Marc', 150, 1, 'assets/004-evil.png', 10, 5, self.proj1)
        self.P1.pos_start(1)
        self.P2 = Player(2, 'Yoann', 110, 1, 'assets/002-angel.png', 7,2, self.proj2)
        self.P2.pos_start(2)
        self.pressed = {}
        self.projs1 = []
        self.projs2 = []

    def create_proj(self, player):
        if player.number_play==1:
            self.projs1.append(Projectile(player.projectile.name, player.projectile.damage, player.projectile.image_string))
        else:
            self.projs2.append(Projectile(player.projectile.name, player.projectile.damage, player.projectile.image_string))