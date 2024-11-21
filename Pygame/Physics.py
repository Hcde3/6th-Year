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

def g(b1,b2):
    distance = dis(b1.absC,b2.absC)
    gravity = 6.7*(10**-11)*(b1.mass*b2.mass/(distance**2))
    return gravity
    
def LorentzEquation(q,E,B,v):
    x = math.cos(90-0)
    F = q*(E + v*x*B)
    return F

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

class Body:
    def __init__(self,mass,absC,vel,surf):
        self.absC = absC #m
        self.mass = mass #kg
        self.surf = surf #m2
        self.vel = vel #m/s
        
class SolidFloor:
    def __init__(self,colour,height,side,friction):
        self.height = height
        self.colour = colour
        self.side = side
        self.friction = friction
        
pygame.init()
WHITE = (250,250,250)
window_sz = 800
window = 800
void = pygame.Surface((window_sz,window_sz))
window = 400
center_xdis = 0
center_ydis = 0
center_xchange = 0
center_ychange = 0
window_change = 0
screen = pygame.display.set_mode((window_sz,window_sz))#, flags)
pygame.display.set_caption("Gravity")
sphere = pygame.Surface((60,60))
sphere.fill("Blue")
sphere2 = pygame.Surface((60,60))
sphere2.fill("White")
floor = pygame.Surface((window_sz,window_sz))
floor.fill("Green")
Bodies = [Body(6,(0,0),(10,0),sphere),Body(2,(150,150),(0,0),sphere2)]
NormalGround = SolidFloor("green",600,"v",1)
SolidFloors = [NormalGround]

clock = pygame.time.Clock()
tick = 0
sectransform = 1/60
while True:
    #______________________________ INPUTS ___________________________
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
                    window_change = -2
                if event.key == pygame.K_i:
                    window_change = 2
                if event.key == pygame.K_w:
                    center_ychange = 10
                if event.key == pygame.K_s:
                    center_ychange = -10
                if event.key == pygame.K_a:
                    center_xchange = 10
                if event.key == pygame.K_d:
                    center_xchange = -10
    
    #______________________________ MECHANICS ___________________________
    
    for B in Bodies:
        forces = []
        forces.append((0,9.8*B.mass))
        for B2 in Bodies:
            if not B == B2:
                forces.append((vectorcomponent(angle(B.absC,B2.absC),g(B,B2),"x"),vectorcomponent(angle(B.absC,B2.absC),g(B,B2),"y")))
        for Floor in SolidFloors:
            if Floor.side == "v":
                if Floor.height < B.absC[1]:
                    forces.append((Floor.friction*-B.vel[0],-20*B.mass))
                    B.absC = (B.absC[0],Floor.height)
        for F in forces:
            B.vel = (B.vel[0] + (F[0]/B.mass),B.vel[1] + (F[1]/B.mass))
        
    
    #______________________________ GRAPHICS ______________________________
    screen.blit(void,(0,0))
    for B in Bodies:
        B.absC = (B.absC[0]+(B.vel[0]*sectransform),B.absC[1]+(B.vel[1]*sectransform))
        window_blit(B)
    
    for F in SolidFloors:
        screen.blit(floor,(0, 0+abswin_convert(F.height+59,"abs","y")))
    
    mouse_point = pygame.mouse.get_pos()
    center_xdis += center_xchange
    center_ydis += center_ychange
    if window < 100:
        if window_change < 0:
            window_change = 0
    window += window_change
    pygame.display.update()
    tick += 1
    clock.tick(60)
