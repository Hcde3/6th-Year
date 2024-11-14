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
    gravity = 6.7*10**-11*(b1.mass*b2.mass/(distance**2))
    return gravity
    

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
        self.absC = absC #1000km
        self.mass = mass #kg
        self.surf = surf #m2
        self.vel = vel #1000km/s
        
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
sphere = pygame.Surface((6,6))
sphere.fill("Blue")
Bodies = [Body(6*10**24,(0,0),(0,0),sphere),Body(6*10**24,(149597,149597),(0,0),sphere)]
clock = pygame.time.Clock()
tick = 0
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
                    if window - 1 > 0:
                        window_change = -40
                if event.key == pygame.K_i:
                    window_change = 40
                if event.key == pygame.K_w:
                    center_ychange = 2
                if event.key == pygame.K_s:
                    center_ychange = -2
                if event.key == pygame.K_a:
                    center_xchange = 2
                if event.key == pygame.K_d:
                    center_xchange = -2
    
    #______________________________ MECHANICS ___________________________
    
    for B in Bodies:
        forces = []
        acceleration = (0,0)
        print(B.absC)
        for B2 in Bodies:
            if not B == B2:
                forces.append([g(B,B2),angle(B.absC,B2.absC)]) #strength,angle
                print(forces)
                for F in forces:
                    acceleration = (acceleration[0]+vectorcomponent(F[1],F[0]/B.mass,"x"),acceleration[1]+vectorcomponent(F[1],F[0]/B.mass,"y"))
                    print(acceleration)
                    acceleration = (acceleration[0],acceleration[1]) #sec>day
                    print(vectorcomponent(F[1],F[0]/B.mass,"x"))
        B.vel = (B.vel[0] + acceleration[0],B.vel[1] + acceleration[1])
        print(B.vel,"vel")
        B.absC = (B.absC[0]+B.vel[0],B.absC[1]+B.vel[1])
            
        
    
    #______________________________ GRAPHICS ______________________________
    screen.blit(void,(0,0))
    for B in Bodies: window_blit(B)
    
    
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