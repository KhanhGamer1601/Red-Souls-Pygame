from pygame import init, key, quit, display, transform, image, sprite, event, font, mixer
from pygame.constants import K_a, K_d, K_s, K_w, MOUSEBUTTONDOWN, QUIT
from random import*
from time import*

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
obstacle_size = 50
ball_size = 25
size = 50

win_sound = mixer.Sound('game_sound/win.mp3')
fireball_sound = mixer.Sound('game_sound/fireball.mp3')
move_sound = mixer.Sound('game_sound/move.mp3')

App = display.set_mode([1016, 600])
display.set_caption('Red Souls')

Map = transform.scale(image.load('game_img/map.png'), [900, 500])
Game_Font = font.SysFont('Times', 16)

Score = 0
Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)

class World():
    def __init__(self, data):
        self.obstacle_list = []
        self.block = transform.scale(image.load('game_img/obstacle.png'), [size, size])
        row_count = 0
        for row in data:
            column_count = 0
            for obstacle in row:
                if obstacle == 1:
                    block = transform.scale(self.block, [obstacle_size, obstacle_size])
                    block_rect = block.get_rect()
                    block_rect.x = column_count * obstacle_size
                    block_rect.y = row_count * obstacle_size
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
        self.health = 16
        self.dx = 0
        self.dy = 0

    def move(self):
        Key = key.get_pressed()

        if Key[K_w]:
            move_sound.play()
            self.dy -= 1

        if Key[K_s]:
            move_sound.play()
            self.dy = 1

        if Key[K_a]:
            move_sound.play()
            self.dx -= 1
            self.turn_state = 'turn_left'

        if Key[K_d]:
            move_sound.play()
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

    def check_health(self):
        if self.health <= 0:
            self.health = 1
            
class Ability(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.ability = transform.scale(image.load(img), [ball_size, ball_size])
        self.rect = self.ability.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1

    def shoot(self):
        self.rect.x += 10 * self.direction

        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x, self.rect.y, ball_size, ball_size):
                self.kill()

            if obstacle[1].colliderect(self.rect.x, self.rect.y, ball_size, ball_size):
                self.kill()

class Enemy(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.img = image.load(img)
        self.enemy = transform.scale(self.img, [size, size])
        self.rect = self.enemy.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.turn_left = transform.scale(transform.flip(self.img, True, False), [size, size])
        self.dx = 1

    def animation(self):
        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + self.dx, self.rect.y, size, size):
                self.dx *= -1
            
        if self.rect.x >= 900 or self.rect.x <= 50:
            self.dx *= -1
        
        if self.dx == 1:
            self.enemy = transform.scale(self.img, [size, size])

        if self.dx == -1:
            self.enemy = self.turn_left

        self.rect.x += self.dx

class Boss_Ability(sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__()
        self.ability = transform.scale(image.load('game_img/fireball.png'), [ball_size, ball_size])
        self.rect = self.ability.get_rect()
        self.rect.x = x + 58
        self.rect.y = y + 58
        self.direction_x = direction_x
        self.direction_y = direction_y

    def shoot(self):
        self.rect.x += 10 * self.direction_x
        self.rect.y += 10 * self.direction_y

        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + 10 * self.direction_x, self.rect.y, ball_size, ball_size):
                self.kill()

            if obstacle[1].colliderect(self.rect.x, self.rect.y + 10 * self.direction_y, ball_size, ball_size):
                self.kill()
                
class Boss(sprite.Sprite):
    def __init__(self, img, health):
        super().__init__()
        self.img = image.load(img)
        self.boss = transform.scale(self.img, [116, 116])
        self.rect = self.boss.get_rect()
        self.rect.x = 450
        self.rect.y = 250
        self.turn_left = transform.scale(transform.flip(self.img, True, False), [116, 116])
        self.dx = 1
        self.health = health

    def move(self):
        for obstacle in world.obstacle_list:
            if obstacle[1].colliderect(self.rect.x + self.dx, self.rect.y, 116, 116):
                self.dx *= -1
            
        if self.rect.x >= 900 or self.rect.x <= 50:
            self.dx *= -1
        
        if self.dx == 1:
            self.boss = transform.scale(self.img, [116, 116])

        if self.dx == -1:
            self.boss = self.turn_left

        self.rect.x += self.dx
            
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

Enemy_Group_1 = sprite.Group()
Enemy_Group_2 = sprite.Group()
Enemy_Group_3 = sprite.Group()

Enemy_0 = Enemy('game_img/enemy_1.png', 300, 250)
Enemy_1 = Enemy('game_img/enemy_1.png', 203, 50)
Enemy_2 = Enemy('game_img/enemy_1.png', 379, 155)
Enemy_3 = Enemy('game_img/enemy_1.png', 616, 162)
Enemy_4 = Enemy('game_img/enemy_1.png', 650, 300)
Enemy_5 = Enemy('game_img/enemy_1.png', 400, 430)
Enemy_6 = Enemy('game_img/enemy_1.png', 450, 400)
Enemy_7 = Enemy('game_img/enemy_1.png', 616, 400)
Enemy_8 = Enemy('game_img/enemy_1.png', 600, 150)
Enemy_Group_1.add(Enemy_0)
Enemy_Group_1.add(Enemy_1)
Enemy_Group_1.add(Enemy_2)
Enemy_Group_1.add(Enemy_3)
Enemy_Group_1.add(Enemy_4)
Enemy_Group_1.add(Enemy_5)
Enemy_Group_1.add(Enemy_6)
Enemy_Group_1.add(Enemy_7)
Enemy_Group_1.add(Enemy_8)

Fireball_group = sprite.Group()
Enemy_fireball_group = sprite.Group()
Player_group = sprite.Group()
Boss_group = sprite.Group()

running = True
create_boss = 0
game_match = 1
Boss_Health = 0

while running:
    for i in event.get():
        if i.type == QUIT:
            running = False
        
        if i.type == MOUSEBUTTONDOWN:
            if i.button == 1:
                fireball = Ability('game_img/fireball.png', Red_Souls.rect.x, Red_Souls.rect.y)
                fireball_sound.play()

                if Red_Souls.turn_state == 'turn_left':
                    fireball.direction = -1
                    Fireball_group.add(fireball)
                
                if Red_Souls.turn_state == 'turn_right':
                    fireball.direction = 1
                    Fireball_group.add(fireball)
       
    App.fill(BLACK)

    Health_Board = Game_Font.render('Health: {}'.format(Red_Souls.health), True, RED)
    Boss_Health_Board = Game_Font.render('Boss Health: {}'.format(Boss_Health), True, RED)
    Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)

    App.blit(Score_Board, [450, 30])
    App.blit(Health_Board, [250, 30])
    App.blit(Boss_Health_Board, [650, 30])
    App.blit(Map, [50, 50])
    
    world.draw()
          
    for i in Fireball_group:
        i.shoot()
        App.blit(i.ability, i.rect)
        if create_boss == 0:
            if sprite.spritecollide(i, Enemy_Group_1, True):
                i.kill()
                Score += 1

            if len(Enemy_Group_1) <= 0:
                create_boss += 1

        if create_boss == 3:
            if sprite.spritecollide(i, Enemy_Group_2, True):
                i.kill()
                Score += 1
                
            if len(Enemy_Group_2) <= 0:
                create_boss += 1

        if create_boss == 6:
            if sprite.spritecollide(i, Enemy_Group_3, True):
                i.kill()
                Score += 1

            if len(Enemy_Group_3) <= 0:
                create_boss += 1

        if i.rect.x >= 1016 or i.rect.x <= 0:
            i.kill()

        if create_boss == 2 or create_boss == 5 or create_boss == 8:
            if sprite.spritecollide(i, Boss_group, False):
                i.kill()
                Score += 1
                for j in Boss_group:
                    j.health -= 1
                    Boss_Health = j.health
            break

    if create_boss == 1:
        a = time()
        b = time()
        boss_1 = Boss('game_img/boss_1.png', 5)
        Boss_group.add(boss_1)
        bullet_1 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 1, 0)
        bullet_2 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, -1, 0)
        bullet_3 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 0, 1)
        bullet_4 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 0, -1)
        Enemy_fireball_group.add(bullet_1)
        Enemy_fireball_group.add(bullet_2)
        Enemy_fireball_group.add(bullet_3)
        Enemy_fireball_group.add(bullet_4)
        create_boss = 2
        Boss_Health = boss_1.health

    if create_boss == 2:
        b = time()
        boss_1.move()
        if b - a > 1:
            bullet_1 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 1, 0)
            bullet_2 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, -1, 0)
            bullet_3 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 0, 1)
            bullet_4 = Boss_Ability(boss_1.rect.x, boss_1.rect.y, 0, -1)
            Enemy_fireball_group.add(bullet_1)
            Enemy_fireball_group.add(bullet_2)
            Enemy_fireball_group.add(bullet_3)
            Enemy_fireball_group.add(bullet_4)
            a = b
        App.blit(boss_1.boss, boss_1.rect)

        for i in Enemy_fireball_group:
            i.shoot()
            App.blit(i.ability, i.rect)  

        if Boss_Health == 0:
            boss_1.kill()

            for i in Boss_group:
                i.kill()

            for i in Enemy_fireball_group:
                i.kill()

            Enemy_0 = Enemy('game_img/enemy_2.png', 300, 250)
            Enemy_1 = Enemy('game_img/enemy_2.png', 203, 50)
            Enemy_2 = Enemy('game_img/enemy_2.png', 379, 155)
            Enemy_3 = Enemy('game_img/enemy_2.png', 616, 162)
            Enemy_4 = Enemy('game_img/enemy_2.png', 650, 300)
            Enemy_5 = Enemy('game_img/enemy_2.png', 400, 430)
            Enemy_6 = Enemy('game_img/enemy_2.png', 450, 400)
            Enemy_7 = Enemy('game_img/enemy_2.png', 616, 400)
            Enemy_8 = Enemy('game_img/enemy_2.png', 600, 150)
            Enemy_Group_2.add(Enemy_0)
            Enemy_Group_2.add(Enemy_1)
            Enemy_Group_2.add(Enemy_2)
            Enemy_Group_2.add(Enemy_3)
            Enemy_Group_2.add(Enemy_4)
            Enemy_Group_2.add(Enemy_5)
            Enemy_Group_2.add(Enemy_6)
            Enemy_Group_2.add(Enemy_7)
            Enemy_Group_2.add(Enemy_8)
            create_boss += 1

    if create_boss == 4:
        a = time()
        b = time()
        boss_2 = Boss('game_img/boss_2.png', 5)
        Boss_group.add(boss_2)
        bullet_1 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 1, 0)
        bullet_2 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, -1, 0)
        bullet_3 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 0, 1)
        bullet_4 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 0, -1)
        Enemy_fireball_group.add(bullet_1)
        Enemy_fireball_group.add(bullet_2)
        Enemy_fireball_group.add(bullet_3)
        Enemy_fireball_group.add(bullet_4)
        create_boss = 5
        Boss_Health = boss_2.health

    if create_boss == 5:
        b = time()
        boss_2.move()
        if b - a > 1:
            bullet_1 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 1, 0)
            bullet_2 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, -1, 0)
            bullet_3 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 0, 1)
            bullet_4 = Boss_Ability(boss_2.rect.x, boss_2.rect.y, 0, -1)
            Enemy_fireball_group.add(bullet_1)
            Enemy_fireball_group.add(bullet_2)
            Enemy_fireball_group.add(bullet_3)
            Enemy_fireball_group.add(bullet_4)
            a = b
        App.blit(boss_2.boss, boss_2.rect)

        for i in Enemy_fireball_group:
            i.shoot()
            App.blit(i.ability, i.rect) 

        if Boss_Health == 0:
            boss_2.kill()

            for i in Boss_group:
                i.kill()

            for i in Enemy_fireball_group:
                i.kill()

            Enemy_0 = Enemy('game_img/enemy_3.png', 300, 250)
            Enemy_1 = Enemy('game_img/enemy_3.png', 203, 50)
            Enemy_2 = Enemy('game_img/enemy_3.png', 379, 155)
            Enemy_3 = Enemy('game_img/enemy_3.png', 616, 162)
            Enemy_4 = Enemy('game_img/enemy_3.png', 650, 300)
            Enemy_5 = Enemy('game_img/enemy_3.png', 400, 430)
            Enemy_6 = Enemy('game_img/enemy_3.png', 450, 400)
            Enemy_7 = Enemy('game_img/enemy_3.png', 616, 400)
            Enemy_8 = Enemy('game_img/enemy_3.png', 600, 150)
            Enemy_Group_3.add(Enemy_0)
            Enemy_Group_3.add(Enemy_1)
            Enemy_Group_3.add(Enemy_2)
            Enemy_Group_3.add(Enemy_3)
            Enemy_Group_3.add(Enemy_4)
            Enemy_Group_3.add(Enemy_5)
            Enemy_Group_3.add(Enemy_6)
            Enemy_Group_3.add(Enemy_7)
            Enemy_Group_3.add(Enemy_8)
            create_boss += 1

    if create_boss == 7:
        a = time()
        b = time()
        boss_3 = Boss('game_img/boss_3.png', 5)
        Boss_group.add(boss_3)
        bullet_1 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 1, 0)
        bullet_2 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, -1, 0)
        bullet_3 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 0, 1)
        bullet_4 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 0, -1)
        Enemy_fireball_group.add(bullet_1)
        Enemy_fireball_group.add(bullet_2)
        Enemy_fireball_group.add(bullet_3)
        Enemy_fireball_group.add(bullet_4)
        create_boss = 8
        Boss_Health = boss_3.health

    if create_boss == 8:
        b = time()
        boss_3.move()
        if b - a > 1:
            bullet_1 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 1, 0)
            bullet_2 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, -1, 0)
            bullet_3 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 0, 1)
            bullet_4 = Boss_Ability(boss_3.rect.x, boss_3.rect.y, 0, -1)
            Enemy_fireball_group.add(bullet_1)
            Enemy_fireball_group.add(bullet_2)
            Enemy_fireball_group.add(bullet_3)
            Enemy_fireball_group.add(bullet_4)
            a = b
        App.blit(boss_3.boss, boss_3.rect)

        for i in Enemy_fireball_group:
            i.shoot()
            App.blit(i.ability, i.rect) 

        if Boss_Health == 0:
            boss_3.kill()
            create_boss = 9

    if create_boss == 9:
        win_sound.play()

    Red_Souls.move()
    App.blit(Red_Souls.player,Red_Souls.rect)

    if sprite.spritecollide(Red_Souls, Enemy_Group_1, False):
        Red_Souls.health -= 1
        Red_Souls.rect.x = 100
        Red_Souls.rect.y = 500

    if sprite.spritecollide(Red_Souls, Boss_group, False):
        Red_Souls.health -= 1
        Red_Souls.rect.x = 100
        Red_Souls.rect.y = 500

    if sprite.spritecollide(Red_Souls, Enemy_fireball_group, False):
        Red_Souls.health -= 1
        Red_Souls.rect.x = 100
        Red_Souls.rect.y = 500
    
    for i in Enemy_Group_1:
        i.animation()
        App.blit(i.enemy, i.rect)

    if create_boss == 3:
        if sprite.spritecollide(Red_Souls, Enemy_Group_2, False):
            Red_Souls.health -= 1
            Red_Souls.rect.x = 100
            Red_Souls.rect.y = 500

        for i in Enemy_Group_2:
            i.animation()
            App.blit(i.enemy, i.rect)

    if create_boss == 6:
        if sprite.spritecollide(Red_Souls, Enemy_Group_3, False):
            Red_Souls.health -= 1
            Red_Souls.rect.x = 100
            Red_Souls.rect.y = 500

        for i in Enemy_Group_3:
            i.animation()
            App.blit(i.enemy, i.rect)

    display.update()
    
quit()
