from pygame import display, init, event, quit, image, draw, time, font
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

Red_Souls = Player('game_img/player.png', 300, 100, 'game_img/player_turn_left.png')
fireball_group_right = sprite.Group()
fireball_group_left = sprite.Group()

Goblin_Guard_0 = Enemy('game_img/enemy.png', 'game_img/enemy.png')

Enemy_Group = sprite.Group()
Enemy_Group.add(Goblin_Guard_0)

Game_Font = font.SysFont('Times', 16)
Score = 0
Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)

running = True
while running:
    App.fill(BLACK)
    Red_Souls.move()
    App.blit(Score_Board, [450, 30])

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

    draw.rect(App, GRAY, [50, 50, 900, 500])

    if shoot_state == 'shooting_right':
        for i in fireball_group_right:
            i.shoot_right()
            App.blit(i.ability, i.rect)
            if i.rect.x >= 1016:
                i.kill()
            if sprite.spritecollide(i, Enemy_Group, False):
                Score += 1
                Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)
                i.kill()

    if shoot_state == 'shooting_left':
        for i in fireball_group_left:
            i.shoot_left()
            App.blit(i.ability, i.rect)
            if i.rect.x <= 0:
                i.kill()
            if sprite.spritecollide(i, Enemy_Group, False):
                Score += 1
                Score_Board = Game_Font.render('Score: {}'.format(Score), True, RED)
                i.kill()

    App.blit(Red_Souls.player, Red_Souls.rect)
    App.blit(Goblin_Guard_0.enemy, Goblin_Guard_0.rect)

    display.update()

quit()
