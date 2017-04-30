import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


#----------------------------Constantes----------------------------------

#Dimensions
fenetre_x=960
fenetre_y=540
taille_fenetre=fenetre_x,fenetre_y

bloc_x=30
bloc_y=30
taille_bloc=bloc_x,bloc_y

nb_bloc_x=fenetre_x//bloc_x
nb_bloc_y=fenetre_y//bloc_y

taille_perso=50,50

#Couleurs
BLANC=255,255,255
GRIS=127,127,127
NOIR=0,0,0
ROUGE=255,0,0
VERT=0,255,0
BLEU=0,0,255
JAUNE=255,255,0
CYAN=0,255,255
MAGENTA=255,0,255

#Events
POP_BULLE=24
ANIMER=25
INVINCIBLE=26
TRAIT=27
POINT=28
CERCLE=29
TP=30
ANGLE=31
ECLAIR=32
ELLIPSE=33



#Divers
g=0.3
