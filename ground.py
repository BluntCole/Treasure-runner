import pygame as pg
from Box2D import *

b2w = 100

class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, world):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2PolygonShape(box=(w, h)))
        self.image = pg.Surface((2*w*b2w, 2*h*b2w))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w