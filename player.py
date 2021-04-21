import pygame as pg
import time


# Création de la classe joueur


class Player(pg.sprite.Sprite):

    def __init__(self, name, max_health, velocity, image_string, splashart_string, attack, heal, projectile, mana_max,
                 mana_regen):
        super().__init__()
        self.name = name
        self.health = max_health
        self.max_health = max_health
        self.velocity = velocity
        self.attack = attack
        self.heal = heal
        self.mana = mana_max
        self.mana_max = mana_max
        self.mana_regen = mana_regen
        self.projectile = projectile
        self.image_string = image_string
        self.image = pg.image.load(self.image_string)
        self.image = pg.transform.scale(self.image, (70, 70))
        self.splashart = pg.transform.scale(pg.image.load(splashart_string), (140, 140))
        self.splashart_rect = self.splashart.get_rect()
        self.rect = self.image.get_rect()
        self.jump = False  # est ce que le joueur veut sauter
        self.reach_top = False  # est ce que le joueur a atteint en haut
        self.jump_direction = None
        self.number_play = None
        self.last_direction = None
        self.last_direction_up = None
        self.blocked_direction = None
        self.set_initial_height = False
        self.initial_height = self.rect.y
        self.fall = False
        self.fall_direction = None
        self.traverse_plateforme = False

    def pos_start(self):
        if self.number_play == 1:
            self.rect.x = 200
        elif self.number_play == 2:
            self.rect.x = 800
        self.rect.y = 535

    def move_right(self):
        self.rect.x += self.velocity
        self.last_direction = 'Right'

    def move_left(self):
        self.rect.x -= self.velocity
        self.last_direction = 'Left'

    def move_up(self):
        self.last_direction_up = 'Up'
        self.rect.y -= (self.velocity + 1)

    def move_down(self):
        self.last_direction_up = 'Down'
        self.rect.y += (self.velocity + 1)

    def try_block(self, other_player):
        if self.distance_cac(other_player):
            pass
            # if self.is_up():
            #   self.blocked_direction = self.last_direction_up
            # else:
            #   self.blocked_direction = self.last_direction
        else:
            self.blocked_direction = None

    def distance_cac(self, other_player):
        if self.rect.colliderect(other_player.rect):
            return True
        else:
            return False

    def set_attacked(self, damage):
        self.health -= damage

    def get_healed(self):
        self.mana -= 20
        if self.health >= self.max_health - self.heal:
            self.health = self.max_health
        else:
            self.health += self.heal

    def punch(self, other_player):
        if self.distance_cac(other_player):
            other_player.set_attacked(self.attack)

    def regen_mana(self):
        if self.mana <= self.mana_max - self.mana_regen:
            self.mana += self.mana_regen
        else:
            self.mana = self.mana_max

    def is_up(self, list_plateforme):
        if self.rect.y == 535:
            res = False
        else:
            for plateforme in list_plateforme:
                if self.is_on_plateforme(plateforme):
                    print("reee")
                    res = False
                    break
                else:
                    res = True
        return res

    def is_on_plateforme(self, plateforme):
        if plateforme.rect.x-20 < self.rect.x < plateforme.rect.x + plateforme.image.get_width()-22 and (
                self.rect.y + self.image.get_height() == plateforme.rect.y or self.rect.y + self.image.get_height() == plateforme.rect.y + 1) and self.last_direction_up == 'Down':
            return True
        else:
            return False

    def try_fall(self, list_plateforme):
        if self.rect.y != 535:
            if not self.jump:
                self.fall = True
                for plateforme in list_plateforme:
                    if self.is_on_plateforme(plateforme):
                        self.fall = False
                        break
                if self.fall or self.traverse_plateforme:
                    if self.fall_direction is None:
                        self.move_down()
                    if self.fall_direction == 'Right':
                        self.move_down()
                        self.move_right()
                    if self.fall_direction == 'Left':
                        self.move_down()
                        self.move_left()
                    for plateforme in list_plateforme:
                        if self.is_on_plateforme(plateforme):
                            self.fall = False
                            self.traverse_plateforme = False
                    if self.rect.y == 535:
                        self.fall = False
                        self.traverse_plateforme = False

    def try_jump(self):  # essaie tout le temps le saut mais le fait ssi jump est true
        # si on a deja initialisé la hauteur initiale, on le refait pas
        if not self.set_initial_height:
            if True:  # self.blocked_direction is None:
                self.initial_height = self.rect.y
            else:
                pass
            # self.initial_height = 535
            self.set_initial_height = True
        if self.jump:
            if self.rect.y > self.initial_height - 200 and not self.reach_top:  # s'il n'a pas atteint deja atteint le top et quil est en dessous du max, on fait monter
                if self.jump_direction is None:
                    self.move_up()
                if self.jump_direction == 'Right':
                    self.move_up()
                    self.move_right()
                if self.jump_direction == 'Left':
                    self.move_up()
                    self.move_left()
                if self.blocked_direction == 'Up':
                    self.reach_top = True
            elif self.blocked_direction != 'Down':  # sinon, on faut descendre et on dit quil a deja atteint le top
                self.reach_top = True
                if self.jump_direction is None:
                    self.move_down()
                if self.jump_direction == 'Right':
                    self.move_down()
                    self.move_right()
                if self.jump_direction == 'Left':
                    self.move_down()
                    self.move_left()

    def try_stop_jump(self, liste_plateforme):
        if self.jump:
            if not self.is_up(liste_plateforme):
                self.jump = False

    def init_jump(self):
        self.reach_top = False
        self.jump_direction = None
        self.set_initial_height = False
        self.jump = True
