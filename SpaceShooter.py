from time import time as timer

import pygame
from pygame import *
from random import randint, choice

pygame.init()

clock = time.Clock()
FPS = 60

reload = False

lost_monsters = 0
killed_monsters = 0
lives = 3
color_g = (0, 255, 0)
color_y = (255, 255, 0)
color_r = (255, 0, 0)
color_w = (255, 255, 255)
fired = 0

info = display.Info()
w = info.current_w
h = info.current_h
w = 430
h = 932

if w > h:
    koef = randint(10, 20)
    head_dict = {
        "ast_sizew": int(w / koef),
        "ast_sizeh": int(h / koef),
        "rocket_sizew": int(w / 20),
        "rocket_sizeh": int(h / 10),
        "monster_sizew": int(w / koef),
        "monster_sizeh": int(h / koef),
        "speed_r": 15,
        "speed_m": 8,
        "speed_a": 10,
        "font_size": 10,
        "koef_b": 4
    }
else:
    koef = randint(8, 10)
    head_dict = {
        "ast_sizew": int(w / koef),
        "ast_sizeh": int(h / koef),
        "rocket_sizew": int(w / 8),
        "rocket_sizeh": int(h / 10),
        "monster_sizew": int(w / 5),
        "monster_sizeh": int(h / 10),
        "speed_r": 15,
        "speed_m": 5,
        "speed_a": 5,
        "font_size": 5,
        "koef_b": 2
    }

window = display.set_mode((w, h))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (w, h))

mixer.init()
mixer.music.load("ambient.ogg")
fire_sound = mixer.Sound("bullet_sound.ogg")
mixer.music.set_volume(0.3)
# mixer.music.play()

font.init()
font1 = font.Font(None, 30)
font2 = font.Font(None, 70)
font3 = font.Font(None, 30)
font4 = font.Font(None, 30)
font5 = font.Font(None, 30)

font_w = font2.render("YOU WIN", True, (0, 255, 0))
font_l = font2.render("YOU LOSE", True, (255, 0, 0))


def button_paint(height, width, color, text, posx, posy, window):
    button = Rect(posx, posy, width, height)
    draw.rect(window, color, button, 2)
    draw.rect(window, color, button, 2)
    fontb = font.Font(None, 30)
    fonts = fontb.render(text, 1, (255, 255, 255))
    font_c = fonts.get_rect(center=button.center)
    window.blit(fonts, font_c)
    return button


class GameSprites(sprite.Sprite):
    def __init__(self, player_img, player_speed, sprite_x, sprite_y, width, heigth):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.width = width
        self.heigth = heigth
        self.image = transform.scale(image.load(player_img), (self.width, self.heigth))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprites):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < w - size_player_w:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_w] and self.rect.y >= h / 1.5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y <= h - size_player_h:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet("bullet.png",
                        7, self.rect.x,
                        self.rect.y, 10,
                        20)
        bullets.add(bullet)
        mixer.music.set_volume(0.3)
        # fire_sound.play()


class Enemy(GameSprites):
    def automove(self):
        global size_monster_w
        global lost_monsters
        self.rect.y += self.speed
        if self.rect.y >= h:
            lost_monsters += 1
            self.rect.y = 0
            location = []
            for i in range(20, w, size_monster_w + 10):
                location.append(i)
            self.rect.x = choice(location)


class Bullet(GameSprites):
    global bullets
    global asteroids

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0 or sprite.groupcollide(bullets,
                                                   asteroids,
                                                   True,
                                                   False):
            self.kill()


class Asteroid(GameSprites):
    def automove(self):
        self.rect.y += self.speed
        if self.rect.y >= h:
            self.rect.y = 0
            self.rect.x = randint(50, w - 50)


monsters = sprite.Group()
for i in range(1, 6):
    koef = randint(3, 10)
    size_monster_w = int(w / koef)
    size_monster_h = int(h / koef)
    monster = Enemy("ufo.png", randint(3, head_dict["speed_m"]), randint(50, w - 50), 20, head_dict["monster_sizew"],
                    head_dict["monster_sizeh"])
    monsters.add(monster)

bullets = sprite.Group()

size_player_w = int(w / 20)
size_player_h = int(h / 10)
player = Player("rocket.png", head_dict["speed_r"], (w / 2), h - head_dict["rocket_sizeh"], head_dict["rocket_sizew"],
                head_dict["rocket_sizeh"])

asteroids = sprite.Group()
asteroid = Asteroid("asteroid.png", head_dict["speed_a"], randint(50, w - 50), 20, head_dict["ast_sizew"],
                    head_dict["ast_sizeh"])
asteroids.add(asteroid)


def show_settings():
    while True:
        window.blit(background, (0, 0))
        text_sound = font5.render("Гучність:", 1, (255, 255, 255))
        window.blit(text_sound, (int(w / 2.2), int(h / 2 - 50)))
        button_exit = button_paint(50, 180, color_w, "ВИХІД", int(w / 2.4), int(h / 2 + 55), window)

        for i in event.get():
            if i.type == QUIT:
                return False
            if i.type == MOUSEBUTTONUP:
                mouse_p = mouse.get_pos()
                if button_exit.collidepoint(mouse_p):
                    return
        display.update()


def show_menu():
    while True:

        window.blit(background, (0, 0))
        text_logo = font5.render("SpaceShooter", 1, (255, 255, 255))
        window.blit(text_logo, (int(w / 2.8), int(h / 2 - 90)))
        button_start = button_paint(30 * head_dict["koef_b"], 90 * head_dict["koef_b"], color_w, "ПОЧАТИ",
                                    int((w - (90 * head_dict["koef_b"])) / 2), int(h / 2 - 31 * head_dict["koef_b"]),
                                    window)
        button_settings = button_paint(30 * head_dict["koef_b"], 90 * head_dict["koef_b"], color_w, "НАЛАШТУВАННЯ",
                                       int((w - (90 * head_dict["koef_b"])) / 2), int(h / 2), window)
        button_exit = button_paint(30 * head_dict["koef_b"], 90 * head_dict["koef_b"], color_w, "ВИХІД",
                                   int((w - (90 * head_dict["koef_b"])) / 2), int(h / 2 + 31 * head_dict["koef_b"]),
                                   window)

        for i in event.get():
            if i.type == QUIT:
                return False
            if i.type == MOUSEBUTTONUP:
                mouse_p = mouse.get_pos()
                if button_start.collidepoint(mouse_p):
                    game = True
                    return game
                if button_exit.collidepoint(mouse_p):
                    game = False
                    return game
                if button_settings.collidepoint(mouse_p):
                    show_settings()

        display.update()


game = show_menu()

finish = False
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if reload == False and fired < 10:
                    player.fire()
                    fired += 1
                if fired >= 10:
                    reload = True
                    reload_timer1 = timer()
            if i.key == K_ESCAPE:
                game = False

    if not finish:
        koef = randint(4, 10)
        size_monster_w = int(w / koef)
        size_monster_h = int(h / koef)
        window.blit(background, (0, 0))
        player.show()
        player.update()
        bullets.draw(window)
        monsters.draw(window)
        for monster in monsters:
            monster.automove()
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            killed_monsters += 1
            monster = Enemy("ufo.png", randint(3, head_dict["speed_m"]), randint(50, w - 50), 20,
                            head_dict["monster_sizew"], head_dict["monster_sizeh"])
            monsters.add(monster)
        text_killed = font1.render("ЗНИЩЕНІ: " + str(killed_monsters), 1, (0, 255, 0))
        text_lost = font1.render("ПРОПУЩЕНІ: " + str(lost_monsters), 1, (0, 255, 0))
        window.blit(text_killed, (20, 20))
        window.blit(text_lost, (20, 50))

        if lives == 3:
            text_lives = font3.render("ЖИТТЯ", 1, (color_g))
        if lives == 2:
            text_lives = font3.render("ЖИТТЯ", 1, (color_y))
        if lives == 1:
            text_lives = font3.render("ЖИТТЯ", 1, (color_r))
        window.blit(text_lives, (w - 100, 20))

        if sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, monsters, True)
            lives -= 1

        if reload == True:
            reload_timer2 = timer()
            if (reload_timer2 - reload_timer1) < 1.5:
                font_r = font4.render("ПЕРЕЗАРЯДКА", 1, (color_r))
                window.blit(font_r, (int(w / 2.2), h - size_player_h))
            else:
                reload = False
                fired = 0

        if killed_monsters >= 2:
            asteroid.show()
            asteroid.automove()

        if killed_monsters >= 10:
            window.blit(font_w, (int(w / 2.4), int(h / 2)))
            finish = True

        if lost_monsters >= 10 or sprite.spritecollide(player, asteroids, False) or lives <= 0:
            window.blit(font_l, (int(w / 2.4), int(h / 2)))
            finish = True

    clock.tick(FPS)
    display.update()
