import pygame as pg
from Box2D import *
import Box2D as b2
import math

b2w = 100

class Ball:
    def __init__(self, world, x, y, radius, density=1, friction=0.3, restitution=0.5):
        # Set up the physical properties of the ball
        self.radius = radius
        self.density = density
        self.friction = friction
        self.restitution = restitution

        # Create the ball body
        self.body = world.CreateDynamicBody(position=(x, y))
        self.shape = b2.b2CircleShape(radius=radius)
        self.fixture = self.body.CreateFixture(shape=self.shape, density=density,
                                               friction=friction, restitution=restitution)

        self.rect = pg.Rect(x - radius, y - radius, 2*radius, 2*radius)

        self.on_ground = False

        self.speed = -1000

    def draw(self, screen, screen_height):
        # Draw the ball on the screen
        ball_position = self.body.position
        ball_screen_pos = (int(ball_position[0]), int(screen_height - ball_position[1]))
        pg.draw.circle(screen, (50, 50, 50), ball_screen_pos, self.radius)

    def update(self):
        if self.on_ground == False:
            self.body.ApplyLinearImpulse(b2Vec2(-self.speed, -10000), self.body.worldCenter, True)
            print(self.on_ground, "here 1")
        if self.on_ground == True:
            self.body.ApplyLinearImpulse(b2Vec2(-self.speed, 0), self.body.worldCenter, True)
            self.on_ground = False
            print(self.on_ground, "here 2")


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, world):
        super().__init__()

        self.x = x
        self.y = y

        self.frame_x = 0
        self.frame_y = 0

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.sheet = pg.image.load("GameMap/maleBase/maleBase/full/advnt_full.png")
        self.sheet.set_clip(pg.Rect(0, 0, 32, 64))
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.rect = self.image.get_rect()

        # set up variables for animation
        self.frame_count = 0
        self.animation_speed = 5
        self.current_frame = 0

        self.body = world.CreateDynamicBody(position=(x, y))

        self.body.userData = self

        self.fixture = self.body.CreateFixture(shape=b2PolygonShape(box=(frame_width / 2, frame_height / 2)),
                                               friction=.5,
                                               restitution=0,
                                               density=.8)

        self.is_moving = False
        self.on_ground = False
        self.direction = ""

        self.speed = 550
        self.jumpForce = -80

    def update(self, dt):
        if self.is_moving:
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0

                # update the current frame of the animation
                self.current_frame = (self.current_frame + 1) % 4
                self.frame_x = self.current_frame * self.frame_width

                # extract the current frame from the tiled sheet
                self.image = self.sheet.subsurface(
                    pg.Rect(self.frame_x, self.frame_y, self.frame_width, self.frame_height))

        if self.on_ground == True:
            self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, 0)
            if self.direction == "up":
                self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, self.jumpForce)
            elif self.direction == "left":
                self.body.ApplyLinearImpulse(b2Vec2(-self.speed, 0), self.body.worldCenter, True)
            elif self.direction == "right":
                self.body.ApplyLinearImpulse(b2Vec2(self.speed, 0), self.body.worldCenter, True)

        if self.on_ground == False:
            if self.direction == "left":
                self.body.ApplyLinearImpulse(b2Vec2(-self.speed, 0), self.body.worldCenter, True)
            elif self.direction == "right":
                self.body.ApplyLinearImpulse(b2Vec2(self.speed, 0), self.body.worldCenter, True)

        self.rect.center = self.body.position.x, self.body.position.y

    def jump(self):
        self.is_moving = True
        self.direction = "up"

    def move_left(self):
        self.is_moving = True
        self.direction = "left"

    def move_right(self):
        self.is_moving = True
        self.direction = "right"


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


