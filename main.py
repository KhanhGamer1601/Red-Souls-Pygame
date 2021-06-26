from pygame import init, key, quit, display, transform, image, sprite, event
from pygame.constants import K_a, K_d, K_s, K_w, MOUSEBUTTONDOWN, QUIT
from random import*

init()

GREEN = [20, 255, 140]
GREY = [210, 210, 210]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
PURPLE = [255, 0, 255]
YELLOW = [255, 255, 0]
CYAN = [0, 255, 255]
BLUE = [100, 100, 255]
BLACK = [0, 0, 0]

game_over = 0
size = 50

App = display.set_mode([1016, 600])
display.set_caption('Red Souls')

Map = transform.scale(image.load('game_img/map.png'), [900, 500])

class World():
    def __init__(self, data):
        self.obstacle_list = []
        self.block = transform.scale(image.load('game_img/obstacle.png'), [size, size])
        row_count = 0
        for row in data:
            column_count = 0
            for obstacle in row:
                if obstacle == 1:
                    block = transform.scale(image.load('game_img/obstacle.png'), [size, size])
                    block_rect = block.get_rect()
                    block_rect.x = column_count * size
                    block_rect.y = row_count * size
                    obstacle = (block, block_rect)
                    self.obstacle_list.append(obstacle)
                column_count += 1
            row_count += 1
    
    def draw(self):
        for obstacle in self.obstacle_list:
            App.blit(obstacle[0], obstacle[1])

class Player(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = image.load('game_img/player.png')
        self.player = transform.scale(self.img, [size, size])
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn_left = transform.scale(transform.flip(self.img, True, False), [size, size])
        self.turn_state = 'ready'
        self.health = 10
        self.dx = 0
        self.dy = 0

    def move(self):
        Key = key.get_pressed()

        if Key[K_w]:
            self.dy -= 1

        if Key[K_s]:
            self.dy = 1

        if Key[K_a]:
            self.dx -= 1
            self.turn_state = 'turn_left'

        if Key[K_d]:
            self.dx = 1
            self.turn_state = 'turn_right'

        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + self.dx, self.rect.y, size, size):
                self.dx = 0

            if obstacle[1].colliderect(self.rect.x, self.rect.y + self.dy, size, size):
                self.dy = 0

        self.rect.x += self.dx
        self.rect.y += self.dy

        self.dx = 0
        self.dy = 0

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
            self.player = transform.scale(self.img, [size, size])

class Ability(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.ability = image.load('game_img/fireball.png')
        self.rect = self.ability.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.ability.get_width()
        self.height = self.ability.get_height()
        self.direction = 1
        self.dx = 0
        self.dy = 0

    def shoot(self):
        self.dx += 10 * self.direction

        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
                self.kill()

            if obstacle[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                self.dy = 0
                self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy

class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = image.load('game_img/enemy.png')
        self.enemy = transform.scale(self.img, [size, size])
        self.rect = self.enemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn_left = transform.scale(transform.flip(self.img, True, False), [size, size])
        self.run_state = 'ready'
        self.dx = 0
        self.dy = 0

    def animation(self):
        if self.run_state != 'running_left':
            self.run_state = 'running_right'

        if self.run_state == 'running_right':
            self.enemy = transform.scale(self.img, [size, size])
            self.dx = 1
            if self.rect.x >= 900:
                self.rect.x = 900
                self.run_state = 'running_left'

        if self.run_state == 'running_left':
            self.enemy = self.turn_left
            self.dx -= 1
            if self.rect.x <= 50:
                self.rect.x = 50
                self.run_state = 'running_right'

        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + self.dx, self.rect.y, size, size):
                self.dx = 0
                self.run_state = 'running_left'
                if self.rect.x == 300:
                    self.run_state = 'running_right'

            if obstacle[1].colliderect(self.rect.x, self.rect.y + self.dy, size, size):
                self.dy = 0
            
        self.rect.x += self.dx
        self.rect.y += self.dy

def Load_map(name):
    file = open(name, 'r')
    value = file.read()
    file.close()

    playmap = []
    data = value.split()

    for map in data:
        wall = []
        for i in range(len(map)):
            if i == len(map) - 2:
                wall.append(int(map[0]))

            wall.append(int(map[i]))
        playmap.append(wall)
    return playmap

world_data = Load_map('map.txt')
world = World(world_data)
Red_Souls = Player(100, 500)

Enemy_Group = sprite.Group()

Goblin_Guard_0 = Enemy(300, 250)
Goblin_Guard_1 = Enemy(203, 50)
Goblin_Guard_2 = Enemy(379, 155)
Goblin_Guard_3 = Enemy(616, 162)
Goblin_Guard_4 = Enemy(650, 300)
Goblin_Guard_5 = Enemy(81, 430)
Goblin_Guard_6 = Enemy(76, 400)
Goblin_Guard_7 = Enemy(616, 400)
Goblin_Guard_8 = Enemy(600, 150)
Enemy_Group.add(Goblin_Guard_0)
Enemy_Group.add(Goblin_Guard_1)
Enemy_Group.add(Goblin_Guard_2)
Enemy_Group.add(Goblin_Guard_3)
Enemy_Group.add(Goblin_Guard_4)
Enemy_Group.add(Goblin_Guard_5)
Enemy_Group.add(Goblin_Guard_6)
Enemy_Group.add(Goblin_Guard_7)
Enemy_Group.add(Goblin_Guard_8)

Fireball_group = sprite.Group()
running = True
while running:
    App.fill(BLACK)
    App.blit(Map, [50, 50])

    for i in event.get():
        if i.type == QUIT:
            running = False
        
        if i.type == MOUSEBUTTONDOWN:
            if i.button == 1:
                fireball = Ability(Red_Souls.rect.x, Red_Souls.rect.y)
                if Red_Souls.turn_state == 'turn_left':
                    fireball.direction = -1
                    Fireball_group.add(fireball)
                
                if Red_Souls.turn_state == 'turn_right':
                    fireball.direction = 1
                    Fireball_group.add(fireball)

    world.draw()

    for i in Fireball_group:
        i.shoot()
        App.blit(i.ability, i.rect)
        if sprite.spritecollide(i, Enemy_Group, True):
            i.kill()

    Red_Souls.move()
    App.blit(Red_Souls.player, Red_Souls.rect)

    for i in Enemy_Group:
        i.animation()
        App.blit(i.enemy, i.rect)

    display.update()

quit()