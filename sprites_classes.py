import pygame
from settings import PLAYER_SIZE, EGG_SPRITE

# CLASSES

class Egg(pygame.sprite.Sprite):
    def __init__(self, rect):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(EGG_SPRITE)
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        if rect is not None:
            self.rect = rect
        else:
            self.rect = self.image.get_rect()


class Snake_part(pygame.sprite.Sprite):
    def __init__(self, image, rect=None, direction='left'):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # This could also be an image loaded from the disk.
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))

        self.rotation = direction
        if self.rotation == 'up':
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.rotation == 'down':
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.rotation == 'right':
            self.image = pygame.transform.rotate(self.image, 180)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        if rect is not None:
            self.rect = rect
        else:
            self.rect = self.image.get_rect()