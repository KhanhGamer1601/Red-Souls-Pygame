from pygame import sprite, image, key
from pygame.constants import K_a, K_d, K_s, K_w

class Player(sprite.Sprite):
    def __init__(self, img_right, x, y, img_left):
        super().__init__()
        self.player = image.load(img_right)
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn_left = image.load(img_left)
        self.img = img_right
        self.turn_state = 'ready'

    def move(self):
        Key = key.get_pressed()

        if Key[K_w]:
            self.rect.y -= 1
            if self.rect.y < 10:
                self.rect.y = 10

        if Key[K_s]:
            self.rect.y += 1
            if self.rect.y > 450:
                self.rect.y = 450

        if Key[K_a]:
            self.rect.x -= 1
            if self.rect.x < 10:
                self.rect.x = 10
            self.turn_state = 'turn_left'

        if Key[K_d]:
            self.rect.x += 1
            if self.rect.x > 850:
                self.rect.x = 850
            self.turn_state = 'turn_right'

        if self.turn_state == 'turn_left':
            self.player = self.turn_left

        if self.turn_state == 'turn_right':
            self.player = image.load(self.img)

class Ability(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.ability = image.load(img)
        self.rect = self.ability.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot_right(self):
        self.rect.x += 16

    def shoot_left(self):
        self.rect.x -= 16
