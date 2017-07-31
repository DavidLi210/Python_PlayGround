import sys,pygame
from random import *
from pygame.locals import *
import traceback
class Ball(pygame.sprite.Sprite):
    def __init__(self, gray_image,green_image, position, speed, bg_size,target):
        pygame.sprite.Sprite.__init__(self)
        self.gray_image = pygame.image.load(gray_image).convert_alpha()
        self.green_image = pygame.image.load(green_image).convert_alpha()
        self.rect = self.gray_image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = speed
        self.target = target
        self.bg_width,self.bg_height = bg_size[0],bg_size[1]
        self.radius = self.rect.width // 2
        self.control = False
        self.collide = False
        self.side = [choice([1,-1]),choice([1,-1])]

    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move([self.speed[0]*self.side[0],self.speed[1]*self.side[1]])
        if self.rect.right <= 0:
            self.rect.left = self.bg_width
        elif self.rect.left >= self.bg_width:
            self.rect.right = 0
        elif self.rect.top >= self.bg_height:
            self.rect.bottom = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.bg_height

    def check(self,motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return  False

class Glass(pygame.sprite.Sprite):
    def __init__(self,glass_image,mouse_image,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left,self.glass_rect.top = (bg_size[0]- self.glass_rect.width)//2 \
            ,(bg_size[1]- self.glass_rect.height)
        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left , self.mouse_rect.top = self.glass_rect.left, self.glass_rect.top
        pygame.mouse.set_visible(False)

def main():
    pygame.init()
    grayball_image = "gray_ball.png"
    greenball_image = "green_ball.png"
    glass_image = "glass.png"
    mouse_image = "hand.png"
    bg_image = "background.png"

    running = True
    bg_size = width,height = 1024,681
    screen = pygame.display.set_mode(bg_size)
    background = pygame.image.load(bg_image).convert_alpha()
    pygame.display.set_caption("Play The Ball")
    balls = []
    mgs = []
    pygame.mixer.music.load("bg_music.ogg")
    pygame.mixer.music.play()

    loser_sound = pygame.mixer.Sound("loser.wav")
    laugh_sound = pygame.mixer.Sound("laugh.wav")
    winner_sound = pygame.mixer.Sound("winner.wav")
    hole_sound = pygame.mixer.Sound("hole.wav")

    GAMEOVER = USEREVENT
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER,1000)

    holes = [(117, 119, 199, 201), (225, 227, 390, 392), \
            (503, 505, 320, 322), (698, 700, 192, 194), \
            (906, 908, 419, 421)]

    pygame.mixer.music.set_endevent(GAMEOVER)
    group = pygame.sprite.Group()
    for i in range(5):
        position = (randint(0,width -100),randint(0,height -100))
        speed = [randint(1,5),randint(1,5)]

        ball = Ball(grayball_image,greenball_image,position,speed,bg_size,(i+1) * 5)
        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left , ball.rect.top = (randint(0,width -100),randint(0,height -100))
        group.add(ball)
        balls.append(ball)

    pygame.key.set_repeat(100, 100)

    motion = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == GAMEOVER:
                laugh_sound.play()
                loser_sound.play()
                pygame.time.delay(4000)
                running = False
            elif event.type == MYTIMER:
                if motion:
                    for ball in group:
                        if ball.check(motion):
                            ball.speed = [0,0]
                            ball.control = True
                    motion = 0
            elif event.type == pygame.MOUSEMOTION:
                motion += 1
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    for ball in balls:
                        if ball.control:
                            print(ball.control)
                            ball.speed[1] -=1
                if event.key == K_d:
                    for ball in balls:
                        if ball.control:
                            ball.speed[0] +=1
                if event.key == K_a:
                    for ball in balls:
                        if ball.control:
                            ball.speed[0] -=1
                if event.key == K_s:
                    for ball in balls:
                        if ball.control:
                            ball.speed[1] +=1
                if event.key == K_SPACE:
                    for ball in group:
                        if ball.control:
                            for hole in holes:
                                if hole[0]-10 <= ball.rect.left <= hole[1]+10 and hole[2]-10 <= ball.rect.top <= hole[3]+10:
                                    hole_sound.play()
                                    ball.control = False
                                    ball.speed = [0,0]
                                    group.remove(ball)
                                    temp = balls.pop(balls.index(ball))
                                    balls.insert(0,temp)
                                    holes.remove(hole)

                            if not holes:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)

                                msg = pygame.image.load("win.png").convert_alpha()
                                msg_pos = (width - msg.get_width()) // 2, \
                                          (height - msg.get_height()) // 2
                                mgs.append((msg, msg_pos))
                                laugh_sound.play()


        screen.blit(background,(0,0))
        glass = Glass(glass_image,mouse_image,bg_size)
        screen.blit(glass.glass_image,glass.glass_rect)

        glass.mouse_rect.left,glass.mouse_rect.top = pygame.mouse.get_pos()
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.left > glass.glass_rect.right - glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right - glass.mouse_rect.width
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height
        screen.blit(glass.mouse_image, glass.mouse_rect)

        for ball in balls:
            ball.move()
            if ball.collide:
                ball.speed = [randint(1,5),randint(1,5)]
                ball.collide = False

            if ball.control:
                screen.blit(ball.green_image,ball.rect)
            else:
                screen.blit(ball.gray_image, ball.rect)

        # if balls collide with the other, change its direction and speed
        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False
            group.add(each)

        for msg in mgs:
            screen.blit(msg[0],msg[1])

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()