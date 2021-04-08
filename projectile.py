import pygame as pg


class Projectile(pg.sprite.Sprite):

    def __init__(self, name, damage, image):
        self.name = name
        self.damage = damage
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (140, 140))
        self.rect = self.image.get_rect()
        self.rect.y = 520

    # test si un projectile entre dans un joueur
    def entered(self, player):
        if player.rect.x - 70 < self.rect.x < player.rect.x + 70:
            return True
        else:
            return False

    def proj_damage(self, player):
        if self.entered(player):
            player.set_attacked(self.damage)


#heheheh