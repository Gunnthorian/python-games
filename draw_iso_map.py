#!/usr/bin/env python
import profile
import pygame, sys, os, math
import spritesheet
from pygame.locals import *

pygame.init()
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((256, 256), flags)

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)

icon = pygame.display.set_icon(pygame.image.load(os.path.join(current_path, 'images/logo.png')).convert_alpha())

ground_img = pygame.image.load(os.path.join(current_path, "images/ground.png")).convert_alpha()
water_img = pygame.image.load(os.path.join(current_path, "images/water.png")).convert_alpha()
rock_img = pygame.image.load(os.path.join(current_path, "images/rock.png")).convert_alpha()
fence_x_img = pygame.image.load(os.path.join(current_path, "images/fence_x.png")).convert_alpha()
fence_y_img = pygame.image.load(os.path.join(current_path, "images/fence_y.png")).convert_alpha()

character_ss = spritesheet.spritesheet('images/character_ss.png')
character_test = character_ss.images_at(((0*64, 8*64, 64, 64),
                              (0*64, 9*64, 64, 64),
                              (0*64, 10*64, 64, 64),
                              (0*64, 11*64, 64, 64)), colorkey = -1)
#character_aa = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))
RUNNING = True

save = [
[{"id":1, "cc":{"id":2}},{"id":1},{"id":0},{"id":0},{"id":0}],
[{"id":1},{"id":1},{"id":1},{"id":0},{"id":0}],
[{"id":1},{"id":1},{"id":1},{"id":1},{"id":1}],
[{"id":1, "cy":{"id":3}, "cx":{"id":3}},{"id":1},{"id":1},{"id":1},{"id":1}],
[{"id":1, "cx":{"id":3}},{"id":1},{"id":1},{"id":1},{"id":1}]]

def str_to_class(str):
    return reduce(getattr, str.split("."), sys.modules[__name__])

class GroundTile:
    def __init__(self, y_, x_, img_, GO=None):
        self.x = x_
        self.y = y_
        self.img = img_
        self.cc = None
        self.cx = None
        self.cy = None
        if GO:
            self.createChild(GO)

    def createChild(self,GO):
        try:
            if GO['cc']:
                self.cc = createGameObject(self.y,self.x,GO['cc'],relationship='cc')
        except:
            pass
        try:
            if GO['cx']:
                self.cx = createGameObject(self.y,self.x,GO['cx'],relationship='cx')
        except:
            pass
        try:
            if GO['cy']:
                self.cy = createGameObject(self.y,self.x,GO['cy'],relationship='cy')
        except:
            pass

    def render(self):
        screen.blit(self.img, (screen_x_mid() + self.x*32 - self.y*32, screen_y_mid() + self.y*16 + self.x*16))
        if self.cc:
            self.cc.render()
        if self.cx:
            self.cx.render()
        if self.cy:
            self.cy.render()

class WorldObject:
    def __init__(self, y_, x_, img_, GO=None):
        self.x = x_
        self.y = y_
        self.img = img_
        self.c = None
        if GO:
            self.createChild(GO)

    def createChild(self,GO):
        try:
            if GO['c']:
                self.c = createGameObject(self.y,self.x,GO['c'],relationship='c')
        except:
            pass

    def render(self):
        screen.blit(self.img, (screen_x_mid() + self.x*32 - self.y*32, screen_y_mid() + self.y*16 + self.x*16))
        if self.c:
            self.c.render()


map = [[None for x in range(len(save[0]))] for y in range(len(save))]

def openSaveMap(map_):
    for i in range(len(map_)):
        for j in range(len(map_)):
            map[i][j] = createGameObject(i,j,map_[i][j])

def createGameObject(i_,j_,GO_,relationship=None):
    if GO_['id'] == 0:
        return GroundTile(i_,j_,water_img,GO=GO_)
    elif GO_['id'] == 1:
        return GroundTile(i_,j_,ground_img,GO=GO_)
    elif GO_['id'] == 2:
        return WorldObject(i_,j_,rock_img,GO=GO_)
    elif GO_['id'] == 3:
        if relationship == 'cx':
            return WorldObject(i_,j_,fence_x_img,GO=GO_)
        elif relationship == 'cy':
            return WorldObject(i_,j_,fence_y_img,GO=GO_)

openSaveMap(save)

class player():

    def update(self):
        self.updatePlayerMovement()
        self.x += self.moving*0.04*math.cos(self.angle - math.pi/4)
        self.y += self.moving*0.04*math.sin(self.angle - math.pi/4)

    def x_vel(self):
        if self.a and self.d:
            return 0
        elif self.a:
            return -0.03
        elif self.d:
            return 0.03
        else:
            return 0
    def y_vel(self):
        if self.a and self.d:
            return 0
        elif self.w:
            return -0.03
        elif self.s:
            return 0.03
        else:
            return 0

    def updatePlayerMovement(self):
        x_comp = 0
        if self.a and self.d:
            x_comp = 0
        elif self.a:
            x_comp = -1
        elif self.d:
            x_comp = 1
        else:
            x_comp = 0
        y_comp = 0
        if self.a and self.d:
            y_comp = 0
        elif self.w:
            y_comp = -1
        elif self.s:
            y_comp = 1
        else:
            y_comp = 0

        if x_comp or y_comp != 0:
            self.moving = 1
        else:
            self.moving = 0

        self.angle = math.atan2(y_comp,x_comp)
        return self.angle


    angle = 0
    moving = 0

    w = False
    a = False
    s = False
    d = False

    x = 1
    y = 1

player = player()

screen_w = 256
screen_h = 256

def screen_x_mid():
    return screen_w/2 - 32
def screen_y_mid():
    return (screen_h/2 - len(map)*32) + 32

def numToTileImg(num):
    if num == 0:
        return water_img
    elif num == 1:
        return ground_img

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            screen_w = event.w
            screen_h = event.h
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.w = True
            if event.key == pygame.K_a:
                player.a = True
            if event.key == pygame.K_s:
                player.s = True
            if event.key == pygame.K_d:
                player.d = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.w = False
            if event.key == pygame.K_a:
                player.a = False
            if event.key == pygame.K_s:
                player.s = False
            if event.key == pygame.K_d:
                player.d = False

    player.update()

    # screen.fill((255,255,255))
    for i in range(len(map)):
        for j in range(len(map[i])):
            map[i][j].render()
            # screen.blit(map[i][j].img, (screen_x_mid() + j*32 - i*32, screen_y_mid() + i*16 + j*16))
    screen.blit(character_test[0], (screen_w/2-32 + player.x*32 - player.y*32, screen_h/2-48 + player.x*16 + player.y*16))
    # screen.blit(ground_img, (0, 0))
    # pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
