import pygame as pg
import time


class Player(pg.sprite.Sprite):

    def __init__(self, name, max_health, velocity, sprite_name, splashart_string, attack, heal, projectile, mana_max,
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
        self.images_rest = self.load_animation(sprite_name, 'repos')
        self.images_run = self.load_animation(sprite_name, 'course')
        self.images_punch = self.load_animation(sprite_name, 'punch')
        self.images_shoot = self.load_animation(sprite_name, 'shoot')
        self.images_jump = self.load_animation(sprite_name, 'saut')
        self.current_index = 0
        self.current_image= self.images_rest[0]
        self.rect = self.current_image.get_rect()
        self.splashart = pg.transform.scale(pg.image.load(splashart_string), (140, 140))
        self.splashart_rect = self.splashart.get_rect()
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
        self.cooldown = False
        self.previous_position =self.rect
        self.is_punching = False
        self.is_shooting = False

    def animate(self, list_plateforme, other_player):
        if self.is_stopped(list_plateforme, other_player) and not self.is_punching and not self.is_shooting:
            if self.current_index>=len(self.images_rest)-1:
                self.current_index=0
            self.current_index +=0.02
            self.current_image = self.images_rest[int(self.current_index)]
        elif self.is_punching and not self.is_shooting:
            if self.current_index >= len(self.images_punch)-1:
                self.current_index = 0
                self.is_punching = False
            self.current_index += 0.02
            self.current_image = self.images_punch[int(self.current_index)]
        elif self.is_shooting:
            if self.current_index >= len(self.images_shoot)-1:
                self.current_index = 0
                self.is_shooting = False
            self.current_index += 0.04
            self.current_image = self.images_shoot[int(self.current_index)]
        elif self.is_up(list_plateforme, other_player):
            if self.current_index >= len(self.images_jump)-1:
                self.current_index = 0
            self.current_index += 0.05
            self.current_image = self.images_jump[int(self.current_index)]
        else:
            if self.current_index >= len(self.images_run)-1:
                self.current_index = 0
            self.current_index += 0.01
            self.current_image = self.images_run[int(self.current_index)]

        if self.last_direction == 'Left':
            self.current_image = pg.transform.flip(self.current_image, True, False)
        self.maj_position_rect()

    def is_stopped(self, list_plateforme, other_player):
        if self.previous_position.x == self.rect.x and not self.is_up(list_plateforme, other_player):
            res = True
        else:
            res = False
        self.previous_position = self.rect
        return res

    def maj_position_rect(self):
        pos_x = self.rect.x
        pos_y = self.rect.y
        self.rect = self.current_image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def load_animation(self,sprite_name, action):
        images = []
        for i in range(1,9):
            image = pg.image.load(f'assets/{sprite_name}/{action}_'+str(i)+'.png')
            if image.get_width()>image.get_height():
                image = pg.transform.scale(image, (110, 90))
            else:
                image = pg.transform.scale(image, (70, 90))
            images.append(image)
        return images

    def pos_start(self):
        if self.number_play == 1:
            self.rect.x = 200
        elif self.number_play == 2:
            self.rect.x = 800
        self.rect.y = 520

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

    def try_block(self, other_player, list_plat):
        if (other_player.rect.x+20< self.rect.x + self.current_image.get_width()< other_player.rect.x+other_player.current_image.get_width()) and other_player.rect.y+other_player.current_image.get_height() +10 > self.rect.y+self.current_image.get_height()/2 > other_player.rect.y-10:
            self.blocked_direction = 'Right'
        elif other_player.rect.x <self.rect.x< other_player.rect.x + other_player.current_image.get_width()-20  and other_player.rect.y+other_player.current_image.get_height()+10 > self.rect.y+self.current_image.get_height()/2 > other_player.rect.y-10:
            self.blocked_direction = 'Left'
        elif self.rect.y == other_player.rect.y+other_player.current_image.get_height() and other_player.rect.x-10< self.rect.x+self.current_image.get_width()/2<other_player.rect.x+other_player.current_image.get_width()+10 and self.is_up(list_plat, other_player):
            self.blocked_direction = self.last_direction_up
        else:
            self.blocked_direction = None

    def distance_cac(self, other_player):
        return self.rect.colliderect(other_player.rect)

    def set_attacked(self, damage):
        self.health -= damage

    def get_healed(self):
        self.mana -= 20
        if self.health >= self.max_health - self.heal:
            self.health = self.max_health
        else:
            self.health += self.heal

    def punch(self, other_player):
        self.current_index = 0
        self.is_punching = True
        if self.distance_cac(other_player):
            other_player.set_attacked(self.attack)

    def regen_mana(self):
        if self.mana <= self.mana_max - self.mana_regen:
            self.mana += self.mana_regen
        else:
            self.mana = self.mana_max

    def is_up(self, list_plateforme, other_player):
        if self.rect.y == 520:
            res = False
        else:
            for plateforme in list_plateforme:
                if self.is_on_plateforme(plateforme):
                    res = False
                    break
                elif self.is_on_player(other_player):
                    res = False
                else:
                    res = True
        return res

    def is_on_player(self, other_player):
        return (self.rect.y + self.current_image.get_width() == other_player.rect.y) and (other_player.rect.x < self.rect.x+self.current_image.get_width()/2 < other_player.rect.x + other_player.current_image.get_width()) and self.last_direction_up=='Down'

    def is_on_plateforme(self, plateforme):
        if plateforme.rect.x - 20 < self.rect.x < plateforme.rect.x + plateforme.image.get_width() - 22 and (
                self.rect.y + self.current_image.get_height() == plateforme.rect.y or self.rect.y + self.current_image.get_height() == plateforme.rect.y + 1) and self.last_direction_up == 'Down':
            return True
        else:
            return False

    def try_fall(self, list_plateforme, other_player):
        if self.rect.y != 520:
            if not self.jump:
                self.fall = True
                # est ce quil est sur qqchose?
                for plateforme in list_plateforme:
                    if self.is_on_plateforme(plateforme):
                        self.fall = False
                        break
                if self.is_on_player(other_player):
                    self.fall = False
                    #je descend si non
                if self.fall or self.traverse_plateforme:
                    self.move_down()
                    if self.fall_direction == 'Right':
                        self.move_right()
                    if self.fall_direction == 'Left':
                        self.move_left()
                    #je retest
                    for plateforme in list_plateforme:
                        if self.is_on_plateforme(plateforme):
                            self.fall = False
                            self.traverse_plateforme = False
                    if self.is_on_player(other_player):
                        self.traverse_plateforme = False
                    if self.rect.y == 520:
                        self.fall = False
                        self.traverse_plateforme = False

    def try_jump(self):  # essaie tout le temps le saut mais le fait ssi jump est true
        # si on a deja initialisé la hauteur initiale, on le refait pas
        if not self.set_initial_height:
            self.initial_height = self.rect.y
            self.set_initial_height = True
        if self.jump:
            if self.rect.y > self.initial_height - 200 and not self.reach_top:  # s'il n'a pas atteint deja atteint le top et quil est en dessous du max, on fait monter
                self.move_up()
                if self.jump_direction == 'Right' and self.blocked_direction != 'Right':
                    self.move_right()
                if self.jump_direction == 'Left' and self.blocked_direction != 'Left':
                    self.move_left()
                if self.blocked_direction == 'Up':
                    self.reach_top = True
            else:   # sinon, on faut descendre et on dit quil a deja atteint le top
                self.reach_top = True
                self.move_down()
                if self.jump_direction == 'Right':
                    self.move_right()
                if self.jump_direction == 'Left':
                    self.move_left()

    def try_stop_jump(self, liste_plateforme, other_player):
        if self.jump:
            if not self.is_up(liste_plateforme, other_player):
                self.jump = False

    def init_jump(self):
        self.reach_top = False
        self.jump_direction = None
        self.set_initial_height = False
        self.jump = True
