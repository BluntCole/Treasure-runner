import pygame as pg
from Box2D import *
from Bodies import Player
from Bodies import Ground
from Bodies import ContactListener

pg.init()

b2w = 100

screen = pg.display.set_mode((1024, 768))

world = b2World(gravity = (0,100), doSleep=True)
ground = Ground(1,1,25,.5, world)
player = Player(100,500,32,64, world)

contact_listener = ContactListener(player, world)
world.contactListener = contact_listener

groundGroup = pg.sprite.Group()
groundGroup.add(ground)

gamer = pg.sprite.Group()
gamer.add(player)

collided = pg.sprite.spritecollide(player, groundGroup, False)
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                player.move_left()
            elif event.key == pg.K_d:
                player.move_right()
            elif event.key == pg.K_SPACE:
                player.jump()
        # elif event.type == pg.KEYUP:
        #     player.is_moving = False

    if player.rect.colliderect(ground.rect):
        player.on_ground = True

    if not player.rect.colliderect(ground.rect):
        player.on_ground = False



        # difference = ground.rect.top - player.rect.bottom

        # # Check if the player is intersecting with the ground
        # if difference >= 0:
        #     # Move the player's sprite up by the difference amount plus a small offset value
        #     offset = 2
        #     player.rect.move_ip(0, difference + offset)
        #
        #     # Update the player's Box2D body position to match the new sprite position
        #     player.body.position = (player.rect.centerx / b2w, player.rect.centery / b2w)

    # if contact_listener.has_contact("player", "ground"):d
    #     print("Player collided with ground")
        # normal = contact_listener.normal
        # impulse = player.body.mass * -world.gravity.y * normal / (normal.dot(normal) + 0.1)
        # player.body.ApplyLinearImpulse(impulse, player.body.worldCenter, True)
        # player.on_ground = True

    dt = clock.tick(60) / 1000.0
    world.Step(dt, 6, 2)

    # contact_listener.update()

    # for contact in contact_listener.contacts:
    #     print("here 2")
    #     if ground in [contact.fixtureA.body.userData, contact.fixtureB.body.userData]:
    #         player.on_ground = True
    #         print("here 1")
    #
    #         # Get the normal vector of the collision
    #         normal = contact.normal
    #
    #         # Calculate the impulse required to stop the player from falling through the ground
    #         impulse = player.body.mass * -world.gravity.y * normal / (normal.dot(normal) + 0.1)
    #
    #         # Apply the impulse to the player's body
    #         player.body.ApplyLinearImpulse(impulse, player.body.worldCenter, True)

    screen.fill((0, 0, 0))
    screen.blit(ground.image, ground.rect)
    gamer.update(dt)
    # ground.update(dt)
    # groundGroup.draw(screen)
    # gamer.draw(screen)

    # screen.blit(ground.image, ground.rect)
    screen.blit(player.image, player.rect)


    pg.display.update()
    pg.display.flip()

pg.quit()