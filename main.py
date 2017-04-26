import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
from fonctions import *
from classes import *
from init import *
from jeu import *
from menu import *


#-----------------------------Début--------------------------------------

pygame.init()
pygame.display.set_icon(icone)
pygame.display.set_caption("C'est mon jeu!!!")

#-----------------------------Création des variables--------------------


#Creation des niveaus
for i in range(7):
    if i==1:pos=40,40
    else:pos=40,480
    Niveau(i,img_theme_1,1,pos)

#Events
pygame.time.set_timer(ANIMER,100)

continuer=True
while continuer:

    niveau_actuel=menu()
    if niveau_actuel!=None:

        while True:
            try:
                etat=jeu(Niveau.liste[niveau_actuel])



            except IndexError:
                continuer=False
                break
            if etat=="win":
                niveau_actuel+=1
            elif etat=="mort":
                pass
            elif etat=="menu":
                break
            elif etat=="reset":
                pass
            elif etat=="fin":
                continuer=False
                break
    else:
        continuer=False
pygame.quit()

