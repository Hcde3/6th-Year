import pygame
import sys
import math
import random
from pygame.locals import *

def window_blit(self):
    if self.absC[0]*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz) -(self.surf.get_width()*(window/window_sz))< window_sz and self.absC[0]*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz) + (self.surf.get_width()*2*(window/window_sz)) > 0 and self.absC[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz) - (self.surf.get_width()*(window/window_sz)) < window_sz and self.absC[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz) + (self.surf.get_width()*2*(window/window_sz))> 0:
        new_surface = pygame.transform.scale(self.surf, (self.surf.get_width()*(window/window_sz), self.surf.get_height()*(window/window_sz)))
        new_surface = new_surface.convert_alpha()
        screen.blit(new_surface,(self.absC[0]*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz),self.absC[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz)))

def dis(point1,point2):
    dis = math.sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2)
    return dis

def abswin_convert(point,original,xory):
    if original == "abs":
        if xory == "x":
            new_point = point*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz)
        else:
            new_point = point*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz)
    elif original == "win":
        if xory == "x":
            new_point = (point - center_xdis*(window/window_sz) - (window_sz-window)/2)/(window/window_sz)
        else:
            new_point = (point - center_ydis*(window/window_sz) - (window_sz-window)/2)/(window/window_sz)
    return new_point

def vectorcomponent(angle, magnitude, XorY):
    if XorY == "y":
        angle -= 90
        if angle < 0:
            angle += 360
    dis = math.cos(math.radians(angle)) * magnitude
    return dis

def angle(point1,point2):
    xdis = point1[0] - point2[0]
    ydis = point1[1] - point2[1]
    if not xdis:
        if ydis >= 0:
            Angle = 270
        else:
            Angle = 90
    else:
        Angle = math.degrees(math.atan(ydis/xdis))
    if xdis <= 0 and ydis <= 0:
        Angle = 0 + Angle
        #print("UpLeft")
    elif xdis <= 0 and ydis >= 0:
        Angle = 360 + Angle
        #print("DownLeft")
    elif xdis >= 0 and ydis >= 0:
        Angle = 180 + Angle
        #print("DownRight")
    elif xdis >= 0 and ydis <= 0:
        Angle = 180 + Angle
        #print("UpRight")
    return Angle

class Particle:
    def __init__(self,charge,mass,vel,absC,surf):
        self.charge = charge #C
        self.absC = absC #m
        self.mass = mass #kg
        self.surf = surf #m2
        self.vel = vel #m/s
        
pygame.init()
WHITE = (250,250,250)
window_sz = 800
window = 800
void = pygame.Surface((window_sz,window_sz))
void.fill(WHITE)
center_xdis = 0
center_ydis = 0
center_xchange = 0
center_ychange = 0
window_change = 0
screen = pygame.display.set_mode((window_sz,window_sz))#, flags)
pygame.display.set_caption("Electro-Magnetism")
clock = pygame.time.Clock()
particulate = pygame.Surface((10,10))
particulate.fill((250,0,0))
Particles = [Particle(1,0.01,(1,0),(0,window_sz/2),particulate),Particle(1,0.01,(1,0),(800,window_sz/2),particulate)]

tick = 0
while True:
    screen.blit(void,(0,0))
    mouse_point = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for P in Particles:
        window_blit(P)
        forces = []
        for P2 in Particles:
            if P != P2: forces.append((8.987*(10**9)*P.charge*P2.charge)/dis(P.absC,P2.absC))
        for F in forces:
            a = F/P.mass
            P.vel = (P.vel[0] + a,P.vel[1])
    print(P)
    pygame.display.update()
    tick += 1
    clock.tick(60)