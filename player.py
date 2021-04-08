import pygame as pg
import time

# Création de la classe joueur
class Player(pg.sprite.Sprite):

    def __init__(self, number_play,nom,max_health, velocity,image, attack, heal):
        self.nom = nom
        self.health = max_health
        self.max_health = max_health
        self.velocity = velocity
        self.attack = attack
        self.heal= heal
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (140, 140))
        self.rect = self.image.get_rect()
        self.rect.y = 520

    def pos_start(self, number_play):
        if number_play == 1:
            self.rect.x = 200
        elif number_play == 2:
            self.rect.x = 800

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def distanceCac(self, OtherPlayer):
        if abs(OtherPlayer.rect.x - self.rect.x) < 100 and abs(OtherPlayer.rect.y - self.rect.y) < 60:
            return True
        else:
            return False

    def set_attacked(self,damage):
        self.health -= damage

    def set_healed(self, heal):
        self.health += heal

    def punch(self,other_player):
        if self.distanceCac(other_player):
            other_player.set_attacked(self.attack)




    """""
    def is_up(self):
        return self.rect.y == 520

    def jump(self, active, up):
        print("0")
        if active == False:
            if self.is_up() == False:
                self.rect.y -= self.velocity
                print("1")
                return True
        else:
                if up and self.rect.y > 300:
                    self.rect.y -= self.velocity
                    print("2")
                    return True
                elif up:
                    print("3")
                    return False
                elif up == False:
                    self.rect.y += self.velocity
                    print("4")
                    return False
    
    """""

