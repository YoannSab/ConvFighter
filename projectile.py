import pygame as pg
import time


class Projectile(pg.sprite.Sprite):

    def __init__(self, name, damage, image, mana_cost):
        super(Projectile, self).__init__()
        self.name = name
        self.damage = damage
        self.image_string = image
        self.image = pg.image.load(self.image_string)
        self.image = pg.transform.scale(self.image, (70, 30))
        self.rect = self.image.get_rect()
        self.mana_cost = mana_cost
        self.shot = False
        self.direction = None
        self.shoot_initiated = False

    # test si un projectile entre dans un joueur

    def touched(self, to_player):
        if self.rect.colliderect(to_player.rect):
            return True
        else:
            return False

    def try_damage(self, to_player):
        if self.touched(to_player):
            to_player.set_attacked(self.damage)
            self.shot = False

    def move_right(self):
        self.rect.x += 2

    def move_left(self):
        self.rect.x -= 2

    def coord_update(self):
        if self.rect.x <= 0 or self.rect.x >= 1050:
            self.shot = False
        if self.shot:
            if self.direction == 'Right':
                self.move_right()
            else:
                self.move_left()

    def init_shoot(self, from_player):
        from_player.mana -= self.mana_cost
        self.direction = from_player.last_direction
        if self.direction == 'Right':
            self.rect.x = from_player.rect.x+from_player.current_image.get_width()/2-10
            self.rect.y = from_player.rect.y+from_player.current_image.get_height()/2-20
        else:
            self.rect.x = from_player.rect.x - from_player.current_image.get_width() / 2-10
            self.rect.y = from_player.rect.y + from_player.current_image.get_height() / 2-20
            self.image = pg.transform.flip(self.image, True, False)
        self.shoot_initiated = True


