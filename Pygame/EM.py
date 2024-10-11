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
window = 400
void.fill(WHITE)
center_xdis = 0
center_ydis = 0
center_xchange = 0
center_ychange = 0
window_change = 0
screen = pygame.display.set_mode((window_sz,window_sz))#, flags)
pygame.display.set_caption("Electro-Magnetism")
clock = pygame.time.Clock()
particulate_pos = pygame.Surface((10,10))
particulate_neg = pygame.Surface((10,10))
particulate_pos.fill((250,0,0))
particulate_neg.fill((0,0,250))
Particles = []
for p_rand in range(100):
    if p_rand%2 == 0: Particles.append(Particle(1.6*10**-19,1.67*10**-27,(0,0),(random.randint(0,window_sz),random.randint(0,window_sz)),particulate_pos))
    else: Particles.append(Particle(-1.6*10**-19,9.11*10**-31,(0,0),(random.randint(0,window_sz),random.randint(0,window_sz)),particulate_pos))

tick = 0
while True:
    
    #______________________________ CAMERA ___________________________
    
    screen.blit(void,(0,0))
    mouse_point = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    window_change = 0
                if event.key == pygame.K_i:
                    window_change = 0
                if event.key == pygame.K_w:
                    center_ychange = 0
                if event.key == pygame.K_s:
                    center_ychange = 0 
                if event.key == pygame.K_a:
                    center_xchange = 0
                if event.key == pygame.K_d:
                    center_xchange = 0
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_v:
                    window = window_sz
                    center_ydis = 0
                    center_xchange = 0
                    center_xdis = 0
                    center_ychange = 0
                if event.key == pygame.K_o:
                    if window - 100 > 0:
                        window_change = -400
                if event.key == pygame.K_i:
                    window_change = 400
                if event.key == pygame.K_w:
                    center_ychange = 200
                if event.key == pygame.K_s:
                    center_ychange = -200
                if event.key == pygame.K_a:
                    center_xchange = 200
                if event.key == pygame.K_d:
                    center_xchange = -200
    center_xdis += center_xchange
    center_ydis += center_ychange
    if window < 100:
        if window_change < 0:
            window_change = 0
    window += window_change
    
    #______________________________ MECHANICS ___________________________
    
    for P in Particles:
        if P.charge < 0: P.surf = particulate_neg
        else: P.surf = particulate_pos
        window_blit(P)
        forces = []
        for P2 in Particles:
            if P != P2: forces.append(((8.987*(10**9)*P.charge*P2.charge)/dis(P.absC,P2.absC),angle(P2.absC,P.absC)))
        for F in forces:
            ax = vectorcomponent(F[1], F[0]/P.mass, "x")
            ay = vectorcomponent(F[1], F[0]/P.mass, "y")
            P.vel = (P.vel[0] + ax,P.vel[1] +ay)
        P.absC = (P.absC[0] + P.vel[0],P.absC[1] + P.vel[1])
        
        
    pygame.display.update()
    tick += 1
    clock.tick(60)