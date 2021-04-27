import pygame as pg


class My_Button(pg.sprite.Sprite):
    def __init__(self, posX, posY, image_path, function):
        super().__init__()
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.function = function
