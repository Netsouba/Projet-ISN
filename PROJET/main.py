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
for i in range(13):
    if i==1:pos=40,40
    else:pos=40,480
    Niveau(i,img_niveau,pos)

if accueil()=="continuer":
    continuer=True
    while continuer:

        niveau_actuel=menu()
        pygame.mixer.music.stop()

        if niveau_actuel!=None:

            while True:

                if niveau_actuel<len(Niveau.liste):

                    etat=jeu(Niveau.liste[niveau_actuel])
                    pygame.mixer.stop()

                else:  #Si c'etait le dernier niveau
                    pygame.image.save(fenetre,"temp/save.png")
                    img_vctr=pygame.image.load("temp/save.png")
                    if victoire(img_vctr)=="fin":
                        continuer=False
                        break
                    elif victoire(img_vctr)=="menu":
                        son_victory.stop()
                        pygame.mixer.music.play()
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

