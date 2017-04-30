import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from classes import *
from init import *
from fonctions_jeu import *



#-----------------------------Début--------------------------------------
pygame.init()
pygame.display.set_icon(icone)
pygame.display.set_caption("C'est mon jeu!!!")

#-----------------------------Création des variables--------------------


#Creation des niveaux
for i in range(24):
    if i==1:pos=40,40
    else:pos=40,480
    Niveau(i,img_niveau,pos)

if accueil()=="continuer":
    continuer=True
    while continuer:

        niveau_actuel=menu()
        if niveau_actuel!=None:

            while True:

                try:
                    etat=jeu(Niveau.liste[niveau_actuel])
                    pygame.mixer.stop()
                except IndexError:  #Si c'etait le dernier niveau
                    continuer=False
                    break

                if etat=="suivant":
                    niveau_actuel+=1
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

