import pygame

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image, x, y):
        if image in loaded:
            self.image = loaded[image]
        else:
            self.image = pygame.image.load(image)
            loaded[image] = self.image
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        sprites.append(self)

    def delete(self):
        sprites.remove(self)

    def draw(self, screen, camera):
        self.rect.topleft = (self.x, self.y)
        # Draw relative to camera
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))