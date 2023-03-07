import pygame as pg
from Box2D import *

class Box2DUpdater:
    def __init__(self, world, timeStep=1.0/60, vel_iters=6, pos_iters=2):
        self.world = world
        self.timeStep = timeStep
        self.vel_iters = vel_iters
        self.pos_iters = pos_iters

    def update(self):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)

