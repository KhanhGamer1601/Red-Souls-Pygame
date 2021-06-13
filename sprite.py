from pygame import sprite, image, key, transform
from pygame.constants import K_a, K_d, K_s, K_w
from random import randint

class Player(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.player = transform.scale(image.load(img), (50, 50))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn_left = transform.scale(transform.flip(image.load(img), True, False), (50, 50))
        self.img = img
        self.turn_state = 'ready'
        self.health = 10
        self.dx = 0
        self.dy = 0
        self.obstacle_collision = False
        self.condition = None

    def move(self):
        Key = key.get_pressed()

        dx = self.dx
        dy = self.dy

        if self.obstacle_collision == False:
            if Key[K_w]:
                dy -= 1

            if Key[K_s]:
                dy = 1

            if Key[K_a]:
                dx -= 1
                self.turn_state = 'turn_left'

            if Key[K_d]:
                dx = 1
                self.turn_state = 'turn_right'

        if self.obstacle_collision == True:
            if self.condition == 1:
                if Key[K_w]:
                    dy -= 1

                if Key[K_s]:
                    dy = 1

                if Key[K_a]:
                    dx -= 1
                    self.turn_state = 'turn_left'

            if self.condition == 2:
                if Key[K_w]:
                    dy -= 1

                if Key[K_s]:
                    dy = 1

                if Key[K_d]:
                    dx = 1
                    self.turn_state = 'turn_right'

            if self.condition == 3:
                if Key[K_w]:
                    dy -= 1

                if Key[K_a]:
                    dx -= 1
                    self.turn_state = 'turn_left'

                if Key[K_d]:
                    dx = 1
                    self.turn_state = 'turn_right'

            if self.condition == 4:
                if Key[K_a]:
                    dx -= 1
                    self.turn_state = 'turn_left'

                if Key[K_s]:
                    dy = 1

                if Key[K_d]:
                    dx = 1
                    self.turn_state = 'turn_right'

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.y < 10:
            self.rect.y = 10

        if self.rect.y > 500:
            self.rect.y = 500

        if self.rect.x < 50:
            self.rect.x = 50

        if self.rect.x > 900:
            self.rect.x = 900

        if self.turn_state == 'turn_left':
            self.player = self.turn_left

        if self.turn_state == 'turn_right':
            self.player = transform.scale(image.load(self.img), (50, 50))

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

class Enemy(sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.enemy = transform.scale(image.load(img), (50, 50))
        self.rect = self.enemy.get_rect()
        self.rect.x = randint(50, 850)
        self.rect.y = randint(50, 450)
        self.turn_left = transform.scale(transform.flip(image.load(img), True, False), (50, 50))
        self.img = img
        self.run_state = 'ready'

    def animation(self):
        if self.run_state != 'running_left':
            self.run_state = 'running_right'
        
        if self.run_state == 'running_right':
            self.enemy = transform.scale(image.load(self.img), (50, 50))
            self.rect.x += 1
            if self.rect.x >= 850:
                self.run_state = 'running_left'

        if self.run_state == 'running_left':
            self.enemy = self.turn_left
            self.rect.x -= 1
            if self.rect.x <= 50:
                self.run_state = 'running_right'

class Obstacle(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.obstacle = transform.scale(image.load(img), (50, 50))
        self.rect = self.obstacle.get_rect()
        self.rect.x = x
        self.rect.y = y
