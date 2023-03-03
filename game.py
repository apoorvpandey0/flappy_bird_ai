import pygame
import neat
import time
import os
import random

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',f'bird{i}.png'))) for i in range(1,4)]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    MAX_VEL = 20
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height =  self.y
        self.img_count =  0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.velocity = -10.5 # we are in 4th quadrant acc to pygame
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count+=1
        
        d = self.velocity+self.tick_count + 1.5*self.tick_count**2
        
        if d>=16:
            d = d/d * 16
        
        if d<0:
            d-=2
        
        self.y = self.y + d

        if d<0 or self.y <self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt>-90:
                self.tilt-=self.ROT_VEL
    
    def draw(self,win):
        self.img_count += 1
        if self.img_count<self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count<self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt<=-80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        rotated_img = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_img,new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 300
    VEL = 5
    def __init__(self,x) -> None:    
        self.x = x
        self.height = 0
        self.gap = 200
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap
    
    def move(self):
        self.x-=self.VEL

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom ))
    
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True
        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 +self.WIDTH <0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH<0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))

def draw_window(win,bird,pipes,base):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        add_pipe = False
        base.move()
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)
            if not pipe.passed and pipe.x<bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        for r in rem:
            pipes.remove(r)
        if add_pipe:
            score+=1
            pipes.append(Pipe(600))
        
        if bird.y + bird.img.get_height()>730:
            pass
        draw_window(win,bird,pipes,base)
    pygame.quit()
    quit()
            
main()






