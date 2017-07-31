import time
import sys
import pygame
from pygame.locals import *
import traceback
from AirforceWar.myplane import MyPlane
from AirforceWar.enemy import *
from AirforceWar.bullet import *
from AirforceWar.supply import *

pygame.init()
pygame.mixer.init()
bg_size = bg_width, bg_height = 480, 700
screen = pygame.display.set_mode(bg_size)
background = pygame.image.load("images/background.png").convert_alpha()
pygame.display.set_caption("AirForce_War by Wenjie Li")

pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(enemies, smallEnemies, param):
    for i in range(param):
        enemy = SmallEnemy(bg_size)
        enemies.add(enemy)
        smallEnemies.add(enemy)


def add_mid_enemies(enemies, mid, param):
    for i in range(param):
        enemy = MidEnemy(bg_size)
        enemies.add(enemy)
        mid.add(enemy)

def add_big_enemies(enemies, big, param):
    for i in range(param):
        enemy = BigEnemy(bg_size)
        enemies.add(enemy)
        big.add(enemy)

def inc_speed(target,inc):
    for each in target:
        each.speed += inc

def main():
    running = True
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    me = MyPlane(bg_size)

    switch_pic = True
    delay = 100

    bullets1 = []
    bullet1_num = 4
    bullet1_index = 0

    for i in range(bullet1_num):
        bullets1.append(Bullet1(me.rect.midtop))

    bullet2_num = 8
    bullet2_index = 0
    bullets2 = []
    for i in range(bullet2_num//2):
        bullets2.append(Bullet2((me.rect.centerx-33, me.rect.centery)))
        bullets2.append(Bullet2((me.rect.centerx+30, me.rect.centery)))

    Red = (255,0,0)
    Black = (0,0,0)
    Green = (0,255,0)
    WHITE= (255,255,255)

    enemies = pygame.sprite.Group()
    
    smallEnemies = pygame.sprite.Group()
    add_small_enemies(enemies,smallEnemies,15)

    midEnemies = pygame.sprite.Group()
    add_mid_enemies(enemies, midEnemies, 5)

    bigEnemies = pygame.sprite.Group()
    add_big_enemies(enemies, bigEnemies, 2)

    me_destroy_index = 0
    en1_destroy_index = 0
    en2_destroy_index = 0
    en3_destroy_index = 0

    pause = False
    pause_hover_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_press_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    ressume_hover_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_press_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    pause_image = pause_hover_image
    pause_rect = pause_image.get_rect()
    pause_rect.left , pause_rect.top = bg_width - pause_rect.width - 10, 10

    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)
    level = 1
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    bomb_supply = Bomb_Supply(bg_size)
    bullet_supply = Bullet_Supply(bg_size)

    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 1000 * 30)
    DOUBLE_BULLET_TIME = USEREVENT + 1
    INVINCIBLE_TIME = USEREVENT + 2

    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_num = 3
    life_rect = life_image.get_rect()

    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    record = False

    is_double_bullet = False

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    if not pause:
                        pygame.time.set_timer(SUPPLY_TIME, 1000 * 30)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()

            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = ressume_hover_image
                    else:
                        pause_image = pause_hover_image
                else:
                    if pause:
                        pause_image = resume_press_image
                    else:
                        pause_image = pause_press_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_sound.play()
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom > 0 and each.active:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                pygame.time.set_timer(DOUBLE_BULLET_TIME,0)
                is_double_bullet = False
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)


        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(enemies,smallEnemies,3)
            inc_speed(smallEnemies,1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(enemies,smallEnemies,3)
            add_mid_enemies(enemies,midEnemies,2)
            add_big_enemies(enemies,bigEnemies,1)
            inc_speed(smallEnemies,1)
            inc_speed(midEnemies,1)
        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(enemies, smallEnemies, 5)
            add_mid_enemies(enemies, midEnemies, 3)
            add_big_enemies(enemies, bigEnemies, 2)
            inc_speed(smallEnemies, 1)
            inc_speed(midEnemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(enemies, smallEnemies, 5)
            add_mid_enemies(enemies, midEnemies, 3)
            add_big_enemies(enemies, bigEnemies, 2)
            inc_speed(smallEnemies, 1)
            inc_speed(midEnemies, 1)
            inc_speed(bigEnemies,1)

        screen.blit(background,(0,0))

        if not pause and life_num:
            key_press = pygame.key.get_pressed()
            if key_press[K_w] or key_press[K_UP]:
                me.moveup()
            if key_press[K_a] or key_press[K_LEFT]:
                me.moveleft()
            if key_press[K_s] or key_press[K_DOWN]:
                me.movedown()
            if key_press[K_d] or key_press[K_RIGHT]:
                me.moveright()

            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(me,bomb_supply):
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(me,bullet_supply):
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME,18 * 1000)
                    bullet_supply.active = False

            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullets2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullets1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            for bullet in bullets:
                if bullet.active:
                    bullet.move()
                    screen.blit(bullet.image,bullet.rect)
                    enemies_over = pygame.sprite.spritecollide(bullet,enemies,False,pygame.sprite.collide_mask)
                    if enemies_over:
                        bullet.active = False
                        for each in enemies_over:
                            if each.active:
                                if each in midEnemies or each in bigEnemies:
                                    each.hit = True
                                    each.energy -= 1
                                    if each.energy == 0:
                                        each.active = False
                                else:
                                    each.active = False

            for bigEnemy in bigEnemies:
                if bigEnemy.active:
                    bigEnemy.move()
                    pygame.draw.line(screen,Black,(bigEnemy.rect.left,bigEnemy.rect.top - 5), \
                                     (bigEnemy.rect.right, bigEnemy.rect.top - 5),2)
                    remain = bigEnemy.energy / BigEnemy.energy
                    if remain > 0.2:
                        color = Green
                    else:
                        color = Red
                    pygame.draw.line(screen, color, (bigEnemy.rect.left, bigEnemy.rect.top - 5), \
                                     (bigEnemy.rect.left + bigEnemy.rect.width * remain, \
                                      bigEnemy.rect.top - 5),2)
                    if bigEnemy.hit:
                        screen.blit(bigEnemy.hit_image, bigEnemy.rect)
                        bigEnemy.hit = False

                    if switch_pic:
                        screen.blit(bigEnemy.image1,bigEnemy.rect)
                    else:
                        screen.blit(bigEnemy.image2,bigEnemy.rect)
                    if bigEnemy.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    if not (delay % 3):
                        if en3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(bigEnemy.destroy_images[en3_destroy_index],bigEnemy.rect)
                        en3_destroy_index = (en3_destroy_index + 1) % 6
                        if en3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            bigEnemy.reset()

            for midEnemy in midEnemies:
                if midEnemy.active:
                    midEnemy.move()

                    pygame.draw.line(screen, Black, (midEnemy.rect.left, midEnemy.rect.top - 5), \
                                     (midEnemy.rect.right, midEnemy.rect.top - 5), 2)
                    remain = midEnemy.energy / MidEnemy.energy
                    if remain > 0.2:
                        color = Green
                    else:
                        color = Red
                    pygame.draw.line(screen, color, (midEnemy.rect.left, midEnemy.rect.top - 5), \
                                     (midEnemy.rect.left + midEnemy.rect.width * remain, \
                                      midEnemy.rect.top - 5), 2)
                    if midEnemy.hit:
                        screen.blit(midEnemy.hit_image, midEnemy.rect)
                        midEnemy.hit = False

                    screen.blit(midEnemy.image,midEnemy.rect)
                else:
                    if not (delay % 3):
                        if en2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(midEnemy.destroy_images[en2_destroy_index],midEnemy.rect)
                        en2_destroy_index = (en2_destroy_index + 1) % 4
                        if en2_destroy_index == 0:
                            midEnemy.reset()
                            score += 6000

            for smallEnemy in smallEnemies:
                if smallEnemy.active:
                    smallEnemy.move()
                    screen.blit(smallEnemy.image,smallEnemy.rect)
                else:
                    if not (delay % 3):
                        if en1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(smallEnemy.destroy_images[en1_destroy_index],smallEnemy.rect)
                        en1_destroy_index = (en1_destroy_index + 1) % 4
                        if en1_destroy_index == 0:
                            smallEnemy.reset()
                            score += 1000

            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for each in enemies_down:
                    each.active = False

            if me.active:
                if switch_pic:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                if not (delay%3):
                    if me_destroy_index ==0:
                        me_down_sound.play()
                    screen.blit(me.me_destroy_images[me_destroy_index],me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            if not (delay % 5 == 0):
                switch_pic = not switch_pic
            delay -= 1
            if not delay:
                delay = 100

            bomb_text = bomb_font.render("× %d" % bomb_num,True,WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, bg_height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, bg_height - 5 - text_rect.height))
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,(bg_width-10-(i+1)*life_rect.width, \
                                 bg_height-10-life_rect.height))
            score_text = score_font.render("Score : %s" % str(score),True,WHITE)
            screen.blit(score_text,(10, 5))
            screen.blit(pause_image,pause_rect)

        elif 0 == life_num:
            pygame.time.set_timer(SUPPLY_TIME, 0)
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            if not record:
                record = True
                with open("record.txt", "r") as f:
                    num = f.read()
                    if not num:
                        num= "0"
                    record_score = int(num)
                    if score > record_score:
                        with open("record.txt", "w") as f:
                            f.write(str(score))
                    me.active = False

            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (bg_width - gameover_text1_rect.width) // 2, bg_height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (bg_width - gameover_text2_rect.width) // 2, \
                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (bg_width - again_rect.width) // 2, \
                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (bg_width - again_rect.width) // 2, \
                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if again_rect.left <= mouse_pos[0] <= again_rect.right and \
                        again_rect.top <= mouse_pos[1] <= again_rect.bottom :
                    main()
                elif gameover_rect.left <= mouse_pos[0] <= gameover_rect.right and \
                        gameover_rect.top <= mouse_pos[1] <= gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ =="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()