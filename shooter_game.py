#imports
from pygame import *
import random


#window settings
window_im = "galaxy.jpg"
w = 1700
h = 900
window = display.set_mode((w, h))
display.set_caption("----------------------------------------------------------------Arcade: Mission Vacuum----------------------------------------------------------------")
background = transform.scale(image.load(window_im), (w, h))

clock = time.Clock()
FPS = 60



#music settings
mixer.init()
bg_music = "space.ogg"
fire_s = "fire.ogg"
#mixer.music.load(bg_music)
#mixer.music.play()

fire_se = mixer.Sound(fire_s)


#text
font.init()

font = font.SysFont(None, 30)
you_failed_text = font.render('MISSION FAILED', True, (250, 20, 0))



#character appearance

asteroid_im = "asteroid.png"
spaceship = "rocket.png"
ufo_im = "ufo.png"
bullet_im = "bullet.png"

#classes
'''main classes'''
class GameSprite(sprite.Sprite):
    def __init__(self, p_x, p_y, p_speed, p_image, hp):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
        self.speed = p_speed
        self.hp = hp

    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


'''sprites groups'''
bullets = sprite.Group()   
hostiles = sprite.Group()   


'''usual ones'''
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1595:
            self.rect.x += self.speed
        
    
    def fire(self):
        bullet = Bullet(plr.rect.centerx - 30, plr.rect.top, 20, bullet_im, 5)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 995:
            self.rect.y += self.speed
        if self.rect.y > 995:
            self.rect.y = 0
            self.rect.x = random.randint(10, 1590)
        
 

class Bullet(GameSprite):
    def update(self):
        
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()


#heroes settings
plr = Player(50, 800, 12, spaceship, 9)




for i in range(0, 5):
    ufo = Enemy(random.randint(10, 1590), 0, 2, ufo_im, 7)
    hostiles.add(ufo)
    
    
#game cycle
game = True
end = False

while game:
    for e in event.get():
        
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                plr.fire()
                #fire_se.play()
        
    
    if end != True:
        window.blit(background, (0, 0))
        plr.reset()
        plr.update()
        hostiles.draw(window)
        hostiles.update()
        bullets.draw(window)
        bullets.update()
        display.update()
    
    collide_setup = sprite.groupcollide(bullets, hostiles, True, True)
    for c in collide_setup:
        ufo = Enemy(random.randint(10, 1590), 0, 2, ufo_im, 2)
        hostiles.add(ufo)
        
    if sprite.spritecollide(plr, hostiles, True):
        plr.hp -= ufo.hp
        print(plr.hp)
        if plr.hp < 0:
            window.blit(you_failed_text, (700, 700))

    
    if sprite.groupcollide(bullets, hostiles, True, True):

        bullets.remove(bullet)
    
