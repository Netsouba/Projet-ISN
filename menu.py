import os
import pygame
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

    fenetre_actuel=0

    rect_fleche_droite=img_fleche_droite.get_rect()
    rect_fleche_gauche=img_fleche_gauche.get_rect()
    rect_fleche_droite.centery=rect_fleche_gauche.centery=9*fenetre_y/10
    rect_fleche_droite.centerx=7*fenetre_x/8
    rect_fleche_gauche.centerx=fenetre_x/8

    liste_boite_rect=[]
    titre_menu_rect.center=fenetre_x/2,fenetre_y/4

    for i in range(len(nombres)//4):

        nombres_rect[i].center=(i+1)*fenetre_x/7,fenetre_y/2
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i].center
        liste_boite_rect.append(rect)
    for i in range(len(nombres)//4):
        nombres_rect[i+6].center=(i+1)*fenetre_x/7,3*fenetre_y/4
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i+6].center
        liste_boite_rect.append(rect)
    for i in range(len(nombres)//4):
        nombres_rect[i+12].center=(i+1)*fenetre_x/7,fenetre_y/2
    for i in range(len(nombres)//4):
        nombres_rect[i+18].center=(i+1)*fenetre_x/7,3*fenetre_y/4




    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                return None
            if event.type==MOUSEBUTTONDOWN:
                for i,rect in enumerate(liste_boite_rect):
                    if rect.collidepoint(event.pos):
                        print(i+fenetre_actuel)
                        return i+fenetre_actuel

                if rect_fleche_droite.collidepoint(event.pos):
                    fenetre_actuel=12
                elif rect_fleche_gauche.collidepoint(event.pos):
                    fenetre_actuel=0


        fenetre.blit(img_fond_menu,(0,0))

        fenetre.blit(titre_menu,titre_menu_rect)
        for i in range(len(nombres)//2):
            fenetre.blit(img_boite,liste_boite_rect[i])
            fenetre.blit(nombres[i+fenetre_actuel],nombres_rect[i+fenetre_actuel])

        if fenetre_actuel==0:
            fenetre.blit(img_fleche_droite,rect_fleche_droite)
        else:
            fenetre.blit(img_fleche_gauche,rect_fleche_gauche)
        pygame.display.flip()


#----------------------------Gestion du temps-----------------------------
        timer.tick(30)
        fps=timer.get_fps()
        if fps!=0:
            duree_frame=1/fps
        else:
            duree_frame=0