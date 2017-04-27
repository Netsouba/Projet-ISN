import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
import texte
from fonctions import *
from classes import *
from surfaces import *
from sons import *
from jeu import *
from menu import *

#-----------------------------Début--------------------------------------

pygame.init()
pygame.display.set_icon(icone)
pygame.display.set_caption("C'est mon jeu!!!")

#-----------------------------Création des variables--------------------


#Creation des niveaus
niveau1=Niveau(0,img_theme_1,1,(40,480))
niveau2=Niveau(1,img_theme_1,1,(40,40))
niveau3=Niveau(2,img_theme_1,1,(40,480))
niveau4=Niveau(3,img_theme_1,1,(40,480))
niveau5=Niveau(4,img_theme_1,1,(40,480))
niveau6=Niveau(5,img_theme_1,1,(40,480))

#Events
pygame.time.set_timer(SECONDE,1000)
pygame.time.set_timer(ANIMER,100)

m=menu()
if m!=None:
    etat=jeu(Niveau.liste[m])
    if etat=="win":
        print("GG")
    elif etat=="mort":
        print("T'es mort")

pygame.quit()

