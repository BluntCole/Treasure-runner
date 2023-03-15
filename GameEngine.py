import pygame as pg
from Box2D import *
import pytmx
import os
from Bodies import Player
from Bodies import Tile

class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        x = -target.rect.x + int(screen.get_width() / 2)
        y = -target.rect.y + int(screen.get_height() / 2)
        self.rect = pg.Rect(x, y, self.rect.width, self.rect.height)

pg.init()

b2w = 100

screen = pg.display.set_mode((1024, 768))

script_dir = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(script_dir, "GameMap", "GameMap.tmx")
tiled_map = pytmx.util_pygame.load_pygame(map_path)


world = b2World(gravity = (0,100), doSleep=True)
player = Player(50,150,32,64, world)

gamer = pg.sprite.Group()
gamer.add(player)

tile_group = pg.sprite.Group()
non_pys_group = pg.sprite.Group()
win_group = pg.sprite.Group()
lose_group = pg.sprite.Group()


for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('Physical for player and ball', 'physical for player'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=tile_group)

for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('stairs', 'decorate', 'wall'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=non_pys_group)

for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('lose'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=lose_group)

for layer in tiled_map.layers:
    # if layer.name in ('player'):
    if layer.name in ('win'):
        for x, y, surf in layer.tiles():
            pos = (x * tiled_map.tilewidth, y * tiled_map.tileheight)
            Tile(pos=pos, surf=surf, groups=win_group)

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

    camera_x = player.rect.x - screen.get_width() / 2
    camera_y = player.rect.y - screen.get_height() / 2

    # Ensure the camera does not go off the edges of the map
    camera_x = max(camera_x, 0)
    camera_x = min(camera_x, tiled_map.width * tiled_map.tilewidth - screen.get_width())
    camera_y = max(camera_y, 0)
    camera_y = min(camera_y, tiled_map.height * tiled_map.tileheight - screen.get_height())

    for tile in tile_group:
        if tile.image != 0:
            if player.rect.colliderect(tile.rect):
                player.on_ground = True
                break
    else:
        player.on_ground = False

    for tile in win_group:
        if tile.image != 0:
            if player.rect.colliderect(tile.rect):
                print("you win")
                pg.quit()

    for tile in lose_group:
        if tile.image != 0:
            if player.rect.colliderect(tile.rect):
                print("you lose")
                pg.quit()

    dt = clock.tick(60) / 1000.0
    world.Step(dt, 6, 2)

    # screen.fill((0, 0, 0))
    gamer.update(dt)
    for tile in lose_group:
        if tile.image != 0:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))
    for tile in non_pys_group:
        if tile.image != 0:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))
    for tile in tile_group:
        if tile.image != 0:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))
    for tile in win_group:
        if tile.image != 0:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))
    for tile in lose_group:
        if tile.image != 0:
            screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))

    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))


    pg.display.update()
    pg.display.flip()

pg.quit()

