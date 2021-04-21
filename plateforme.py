import pygame as pg


class Plateforme(pg.sprite.Sprite):

    def __init__(self, number_plat, posX, posY, width, height, image_string):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(image_string), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY


