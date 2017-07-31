import sys,pygame
class MyPlane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.bg_width , self.bg_height = bg_size[0],bg_size[1]
        self.rect.left , self.rect.top = (self.bg_width - self.rect.width)//2 , self.bg_height - self.rect.height - 60
        self.speed = 10
        self.active = True
        self.invincible = False
        self.me_destroy_images = []
        self.me_destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_4.png").convert_alpha() \
            ])
        self.mask = pygame.mask.from_surface(self.image1)

    def moveup(self):
        if self.rect.top >0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveleft(self):
        if self.rect.left >0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def movedown(self):
        if self.rect.bottom < self.bg_height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.bg_height - 60

    def moveright(self):
        if self.rect.right < self.bg_width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.bg_width

    def reset(self):
        self.rect.left, self.rect.top = (self.bg_width - self.rect.width) // 2, self.bg_height - self.rect.height - 60
        self.active = True
        self.invincible = True
