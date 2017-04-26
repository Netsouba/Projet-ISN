﻿import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
from fonctions import *
from classes import *
from init import *

def menu():
    duree_frame=0
    timer=pygame.time.Clock()

    liste_boite_rect=[]
    titre_menu_rect.center=fenetre_x/2,fenetre_y/4
    for i in range(len(nombres)//2):
        nombres_rect[i].center=(i+1)*fenetre_x/7,fenetre_y/2
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i].center
        liste_boite_rect.append(rect)
    for i in range(len(nombres)//2):
        nombres_rect[i+6].center=(i+1)*fenetre_x/7,3*fenetre_y/4
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i+6].center
        liste_boite_rect.append(rect)


    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                return None
            if event.type==MOUSEBUTTONUP:
                for i,rect in enumerate(liste_boite_rect):
                    if rect.collidepoint(event.pos):
                        return i





        fenetre.blit(img_fond_menu,(0,0))

        fenetre.blit(titre_menu,titre_menu_rect)
        for i in range(len(nombres)):
            fenetre.blit(img_boite,liste_boite_rect[i])
            fenetre.blit(nombres[i],nombres_rect[i])
        pygame.display.flip()

#----------------------------Gestion du temps-----------------------------
        timer.tick(30)
        fps=timer.get_fps()
        if fps!=0:
            duree_frame=1/fps
        else:
            duree_frame=0