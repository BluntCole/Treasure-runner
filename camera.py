class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.rect.topleft)

    def update(self, target):
        x = -target.rect.x + int(screen.get_width() / 2)
        y = -target.rect.y + int(screen.get_height() / 2)
        self.rect = pg.Rect(x, y, self.rect.width, self.rect.height)