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

#-----------------------------Début--------------------------------------

pygame.init()
pygame.display.set_icon(icone)
pygame.display.set_caption("C'est mon jeu!!!")

#-----------------------------Création des variables--------------------


#Creation des niveaus
niveau1=Niveau(0,"Niveaux//1.txt",img_theme_1,1)
niveau2=Niveau(1,"Niveaux//2.txt",img_theme_1,1)
niveau_actuel=niveau1


#Events
pygame.time.set_timer(SECONDE,1000)
pygame.time.set_timer(ANIMER,100)


etat=jeu(niveau_actuel)
if etat=="win":
    print("GG")
elif etat=="mort":
    print("T'es mort")

pygame.quit()

