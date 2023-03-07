import pygame as pg
from Box2D import *
import math

b2w = 100

class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, world):
        super().__init__()
        self.body = world.CreateStaticBody(position=(x, y))
        self.image = pg.Surface((2*w*b2w, 2*h*b2w))
        self.image.fill((0, 255, 0,))
        self.rect = self.image.get_rect()
        self.rect.center = self.body.position.x * b2w, 768 - self.body.position.y * b2w
        self.fixture = self.body.CreateFixture(shape=b2PolygonShape(box=(w, h)),
                                               friction=0,
                                               restitution=.9,
                                               density=100)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, frame_width, frame_height, world):
        super().__init__()

        self.x = x
        self.y = y

        self.frame_x = 0
        self.frame_y = 0

        self.frame_width = frame_width
        self.frame_height = frame_height

        self.sheet = pg.image.load("maleBase/maleBase/full/advnt_full.png")
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
                                               friction=0,
                                               restitution=.5,
                                               density=1)

        self.is_moving = False
        self.on_ground = False
        self.direction = ""

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
                self.body.linearVelocity = b2Vec2(self.body.linearVelocity.x, -200)
            elif self.direction == "left":
                self.body.ApplyLinearImpulse(b2Vec2(-1000, 0), self.body.worldCenter, True)
            elif self.direction == "right":
                self.body.ApplyLinearImpulse(b2Vec2(1000, 0), self.body.worldCenter, True)

        if self.on_ground == False:
            if self.direction == "left":
                self.body.ApplyLinearImpulse(b2Vec2(-1000, 0), self.body.worldCenter, True)
            elif self.direction == "right":
                self.body.ApplyLinearImpulse(b2Vec2(1000, 0), self.body.worldCenter, True)


        self.rect.center = self.body.position.x, self.body.position.y

    def jump(self):
        # if self.on_ground:
            # self.body.ApplyLinearImpulseToCenter((0, 200), True)
        # self.on_ground = False
        self.direction = "up"

    def move_left(self):
        # self.body.ApplyLinearImpulse(b2Vec2(-2, 0), self.body.worldCenter, True)
        self.is_moving = True
        print(self.on_ground)
        self.direction = "left"

    def move_right(self):
        # self.body.ApplyLinearImpulse(b2Vec2(2, 0), self.body.worldCenter, True)
        self.is_moving = True
        self.direction = "right"

class ContactListener(b2ContactListener):
    def __init__(self, player, world):
        super().__init__()
        self.player = player
        self.impulse = None
        self.world = world
        self.contacts = []

    # def BeginContact(self, contact):
    #     print("Contact detected")
    #     fixture_a = contact.fixtureA
    #     print(fixture_a, "a")
    #     fixture_b = contact.fixtureB
    #     print(fixture_b, "a")
    #     # Check if the player has collided with the ground
    #     if self.player in [fixture_a.body.userData, fixture_b.body.userData]:
    #         self.player.on_ground = True
    #         self.contacts.append(contact)
    #
    #         # Get the normal vector of the collision
    #         normal = contact.normal
    #
    #         # Calculate the impulse required to stop the player from falling through the ground
    #         self.impulse = self.player.body.mass * -self.world.gravity.y * normal / (normal.dot(normal) + 0.1)
    #
    #         # Add a small y offset to player position to prevent sticking to the ground
    #         y_offset = 0.01
    #         if contact.fixtureA.body.userData == self.player:
    #             self.player.body.position.y += y_offset
    #         else:
    #             self.player.body.position.y -= y_offset
    #
    # def EndContact(self, contact):
    #     fixture_a = contact.fixtureA
    #     fixture_b = contact.fixtureB
    #     # Check if the player has left the ground
    #     if self.player in [fixture_a.body.userData, fixture_b.body.userData]:
    #         self.player.on_ground = False
    #         self.contacts.remove(contact)
    #         self.impulse = None
    #
    # def update(self):
    #     for contact in self.contacts:
    #         print("here 1")
    #         # handle collision between player and ground
    #         if contact.fixtureA.body.userData == self.player or contact.fixtureB.body.userData == self.player:
    #             self.BeginContact(contact)
    #
    # # def has_contact(self, body1, body2):
    # #     for contact in self.contacts:
    # #         fixture_a = contact.fixtureA
    # #         fixture_b = contact.fixtureB
    # #         if (fixture_a.body.userData == body1 and fixture_b.body.userData == body2) or (
    # #                 fixture_a.body.userData == body2 and fixture_b.body.userData == body1):
    # #             return True
    # #     return False