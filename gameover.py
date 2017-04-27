import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
from fonctions import *
from classes import *
from init import *



def game_over(fond):
#-----------------------Game over-----------------------------------------------


    rect_reessayer.centerx=rect_menu.centerx=rect_suivant.centerx=rect_gameover.centerx=fenetre_x/2
    rect_gameover.centery=fenetre_y/8

    rect_reessayer.centery=3*fenetre_y/8
    rect_menu.centery=fenetre_y/2
    rect_suivant.centery=5*fenetre_y/8


    continuer=True
    while continuer:
        for event in pygame.event.get():
            if event.type==QUIT:
                return "fin"
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                if rect_menu.collidepoint(event.pos):
                    return "menu"
                elif rect_reessayer.collidepoint(event.pos):
                    return "reset"
                elif rect_suivant.collidepoint(event.pos):
                    return "suivant"
        fenetre.blit(fond,(0,0))
        fenetre.blit(fond_pause,(0,0))
        fenetre.blit(texte_menu,rect_menu)
        fenetre.blit(texte_gameover,rect_gameover)
        fenetre.blit(texte_suivant,rect_suivant)
        fenetre.blit(texte_reessayer,rect_reessayer)
        pygame.display.flip()