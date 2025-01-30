from pygame import *
from random import randint as r
from random import random
from time import time as timer


font.init()
mixer.init()
screen = display.set_mode((700, 500))
clock = time.Clock()
bg = transform.scale(image.load('galaxy.jpg'),(700, 500))
score = 0
lost = 0
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 50)

class GameSpite(sprite.Sprite):
    def __init__(self, image_player, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(image_player),(width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSpite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 2, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSpite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = r(80, 620)
            self.rect.y = -50
            lost += 1

class Bullet(GameSpite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
player = Player('rocket.png', 310, 400, 80, 100, 10)
fire_sound = mixer.Sound('fire.ogg')

for i in range(5):
    monster = Enemy('ufo.png',r(80, 620), -50, 80, 50, r(1, 3) + random())
    monsters.add(monster)
for i in range(3):
    asteroid = Enemy('asteroid.png', r(80, 620), -50, 80, 50, r(1, 10) / 2)
    asteroids.add(asteroid)

life = 3
win = font2.render('You Win', True, (255, 215, 0))
lose = font2.render('You Lose', True, (255, 0, 0))
rel_time = False
num_fire = 0
finish = False
game = True
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

            elif e.key == K_q:
                score = 0
                lost = 0
                for monster in monsters:
                    monster.rect.y = -50
                for asteroid in asteroids:
                    asteroid.rect.y = -50
                life = 3
                finish = False


    if not finish:
        screen.blit(bg, (0, 0))

        player.reset()
        player.update()
        monsters.draw(screen)
        monsters.update()
        text_score = font1.render('Счет: '+ str(score), 1, (255, 255, 255))
        text_lost = font1.render('Пропущено: '+ str(lost), 1, (255, 255, 255))
        screen.blit(text_score, (5, 5))
        screen.blit(text_lost, (5, 33))
        bullets.draw(screen)
        bullets.update()
        asteroids.draw(screen)
        asteroids.update()
        
        if rel_time == True:
            now_time = timer()
            
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                screen.blit(reload, (260, 460))
            else:
                num_fire = 0 
                rel_time = False

        collides = sprite.groupcollide(asteroids, bullets, False, True)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png',r(80, 620), -50, 80, 50, r(2, 4))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life -= 1

        if life == 3:
            life_color = (0, 255, 0)
        elif life == 2: 
            life_color = (255, 255, 0)
        elif life == 1:
            life_color = (255, 0, 0)
        elif life == 0 or lost >= 3:
            finish = True
            screen.blit(lose, (200, 200))

        life_score = font1.render(str(life), True, life_color)
        screen.blit(life_score, (650, 10))


        if score >= 10:
            finish = True
            screen.blit(win, (200, 200))
        
    display.update()
    clock.tick(40)