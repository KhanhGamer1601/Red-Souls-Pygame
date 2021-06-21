from pygame import display, init, event, quit, image, draw, font, mouse
from pygame.constants import MOUSEBUTTONDOWN, QUIT
from sprite import*

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GRAY = [100, 100, 100]

init()
App = display.set_mode([1016, 600])
display.set_caption('Red Souls !')
shoot_state = 'ready'

Map = World('game_img/map.png')

Red_Souls = Player('game_img/player.png', 50, 500)
fireball_group_right = sprite.Group()
fireball_group_left = sprite.Group()

Enemy_Group = sprite.Group()

Game_Font = font.SysFont('Times', 16)
Score = 0
Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)

Health_Text = Game_Font.render('Player Health: {}'.format(Red_Souls.health), True, RED)
Heart = image.load('game_img/heart.png')

Obstacle_list = []

file = open('map.txt', 'r')
value = file.read()
file.close()

wall = value.split()
map_game = []

for i in wall:
    map_game.append(i.split(','))

for i in range(len(map_game)):
    for j in range(len(map_game[i])):
        if map_game[i][j] == '1':
            Stone = Obstacle('game_img/obstacle.png', 100 + (j * 50), 100 + (i * 50))
            Obstacle_0 = (Stone.obstacle, Stone.rect)
            Obstacle_list.append(Obstacle_0)

Goblin_Guard_0 = Enemy('game_img/enemy.png', 201, 185)
Goblin_Guard_1 = Enemy('game_img/enemy.png', 203, 50)
Goblin_Guard_2 = Enemy('game_img/enemy.png', 379, 155)
Goblin_Guard_3 = Enemy('game_img/enemy.png', 616, 162)
Goblin_Guard_4 = Enemy('game_img/enemy.png', 650, 300)
Goblin_Guard_5 = Enemy('game_img/enemy.png', 81, 430)
Goblin_Guard_6 = Enemy('game_img/enemy.png', 76, 400)
Goblin_Guard_7 = Enemy('game_img/enemy.png', 792, 256)
Goblin_Guard_8 = Enemy('game_img/enemy.png', 600, 150)
Goblin_Guard_9 = Enemy('game_img/enemy.png', 275, 250)
Enemy_Group.add(Goblin_Guard_0)
Enemy_Group.add(Goblin_Guard_1)
Enemy_Group.add(Goblin_Guard_2)
Enemy_Group.add(Goblin_Guard_3)
Enemy_Group.add(Goblin_Guard_4)
Enemy_Group.add(Goblin_Guard_5)
Enemy_Group.add(Goblin_Guard_6)
Enemy_Group.add(Goblin_Guard_7)
Enemy_Group.add(Goblin_Guard_8)
Enemy_Group.add(Goblin_Guard_9)

running = True
while running:
    App.fill(BLACK)
    Red_Souls.move()
    App.blit(Score_Board, [250, 30])
    App.blit(Health_Text, [450, 30])
    App.blit(Heart, [560, 25])
    App.blit(Map.background, Map.rect)

    for i in event.get():
        if i.type == QUIT:
            running = False
        if i.type == MOUSEBUTTONDOWN:
            if i.button == 1:
                fireball = Ability('game_img/fireball.png', Red_Souls.rect.x, Red_Souls.rect.y)
                fireball_group_right.add(fireball)
                fireball_group_left.add(fireball)
                if Red_Souls.player != Red_Souls.turn_left:
                    shoot_state = 'shooting_right'
                if Red_Souls.player == Red_Souls.turn_left:
                    shoot_state = 'shooting_left'

    if shoot_state == 'shooting_right':
        for i in fireball_group_right:
            i.shoot_right()
            App.blit(i.ability, i.rect)
            if i.rect.x >= 1016:
                i.kill()
            if sprite.spritecollide(i, Enemy_Group, True):
                Score += 1
                Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)
                i.kill()

    if shoot_state == 'shooting_left':
        for i in fireball_group_left:
            i.shoot_left()
            App.blit(i.ability, i.rect)
            if i.rect.x <= 0:
                i.kill()
            if sprite.spritecollide(i, Enemy_Group, True):
                Score += 1
                Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)
                i.kill()

    if sprite.spritecollide(Red_Souls, Enemy_Group, False):
        Red_Souls.health -= 1
        Health_Text = Game_Font.render('Player Health: {}'.format(Red_Souls.health), True, RED)
        Red_Souls.rect.x = 50
        Red_Souls.rect.y = 50

        if Red_Souls.health <= 0:
            Red_Souls.rect.x = -160
            Red_Souls.rect.y = -160
            for i in Enemy_Group:
                i.kill()
            Death_Text = Game_Font.render('You Died', True, RED)
            App.blit(Death_Text, [450, 250])

    for i in Obstacle_list:
        if i[1].colliderect(Red_Souls.rect.x + Red_Souls.dx, Red_Souls.rect.y, 50, 50):
            Red_Souls.dx = 0
        if i[1].colliderect(Red_Souls.rect.x, Red_Souls.rect.y + Red_Souls.dy, 50, 50):
            Red_Souls.dy = 0

        for e in Enemy_Group:
            if i[1].colliderect(e.rect.x + e.dx, e.rect.y, 50, 50):
                e.dx = 0
            if i[1].colliderect(e.rect.x, e.rect.y + e.dy, 50, 50):
                e.dy = 0

        for b_1 in fireball_group_right:
            if i[1].colliderect(b_1.rect.x + b_1.dx, b_1.rect.y, 50, 50):
                b_1.dx = 0
                b_1.kill()
            if i[1].colliderect(b_1.rect.x, b_1.rect.y + b_1.dy, 50, 50):
                b_1.dy = 0
                b_1.kill()

        for b_2 in fireball_group_left:
            if i[1].colliderect(b_2.rect.x + b_2.dx, b_2.rect.y, 50, 50):
                b_2.dx = 0
                b_2.kill()
            if i[1].colliderect(b_2.rect.x, b_2.rect.y + b_2.dy, 50, 50):
                b_2.dy = 0
                b_2.kill()

    for i in Obstacle_list:
        Red_Souls.collision()

        for e in Enemy_Group:
            e.collision()

        for b_1 in fireball_group_right:
            b_1.collision()

        for b_2 in fireball_group_left:
            b_2.collision()

        App.blit(i[0], i[1])
        
    for i in Enemy_Group:
        i.animation()
        App.blit(i.enemy, i.rect)

    App.blit(Red_Souls.player, Red_Souls.rect)

    display.update()

quit()
