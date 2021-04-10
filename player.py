import pygame as pg
import time

# Création de la classe joueur
class Player(pg.sprite.Sprite):

    def __init__(self, number_play,name,max_health, velocity,image, attack, heal, projectile):
        super().__init__()
        self.name = name
        self.number_play = number_play
        self.health = max_health
        self.max_health = max_health
        self.velocity = velocity
        self.attack = attack
        self.heal = heal
        self.projectile = projectile
        self.image_string = image
        self.image = pg.image.load(self.image_string)
        self.image = pg.transform.scale(self.image, (140, 140))
        self.rect = self.image.get_rect()
        self.rect.y = 520
        if self.number_play==1:
            self.last_direction = 'Right'   #met en mémoire la dernière direction
        if self.number_play ==2:
            self.last_direction = 'Left'
        self.jump = False #est ce que le joueur veut sauter
        self.reach_top = False #est ce que le joueur a atteint en haut
        self.jump_direction = None

    def pos_start(self, number_play):
        if number_play == 1:
            self.rect.x = 200
        elif number_play == 2:
            self.rect.x = 800

    def move_right(self):
        self.rect.x += self.velocity
        self.last_direction = 'Right'

    def move_left(self):
        self.rect.x -= self.velocity
        self.last_direction = 'Left'

    def move_up(self):
        self.rect.y -= (self.velocity+2)

    def move_down(self):
        self.rect.y += (self.velocity+2)

    def distance_cac(self, other_player):
        if abs(other_player.rect.x - self.rect.x) < 100 and abs(other_player.rect.y - self.rect.y) < 60:
            return True
        else:
            return False

    def set_attacked(self, damage):
        self.health -= damage

    def set_healed(self, heal):
        self.health += heal

    def punch(self, other_player):
        if self.distance_cac(other_player):
            other_player.set_attacked(self.attack)

    def is_up(self):
        return self.rect.y != 520

    def try_jump(self): #essaie tout le temps le saut mais le fait ssi jump est true
        if self.jump:
            if self.rect.y>300 and not self.reach_top: #s'il n'a pas atteint deja atteint le top et quil est en dessous du max, on fait monter
                if self.jump_direction ==None:
                    self.move_up()
                if self.jump_direction== 'Right':
                    self.move_up()
                    self.move_right()
                if self.jump_direction== 'Left':
                    self.move_up()
                    self.move_left()
            else:
                self.reach_top = True
                if self.jump_direction==None:
                    self.move_down()  #sinon, on faut descendre et on dit quil a deja atteint le top
                if self.jump_direction == 'Right':
                    self.move_down()
                    self.move_right()
                if self.jump_direction =='Left':
                    self.move_down()
                    self.move_left()
                if not self.is_up(): #s'il est de nouveau a terre, jump devient false
                    self.jump = False

    def init_jump(self):
        self.reach_top = False
        self.jump_direction = None
        self.jump = True

