import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


#----------------------------Constantes----------------------------------

#---------------------------Dimensions-----------------------------------
fenetre_x=960                             #Largeur de la fenêtre
fenetre_y=540                             #Hauteur de la fenêtre
taille_fenetre=fenetre_x,fenetre_y        #Taille de la fenêtre
                                          #Ces constantes seront utiles notamment pour centrer des images ou des textes
  
bloc_x=30                                 #Largeur d'un bloc  
bloc_y=30                                 #Hauteur d'un bloc
taille_bloc=bloc_x,bloc_y                 #Taille d'un bloc
                                          #Ces constantes seront utiles pour le quadrillage de l'écran
  
nb_bloc_x=fenetre_x//bloc_x               #Nombre de blocs de gauche à droite
nb_bloc_y=fenetre_y//bloc_y               #Nombre de blocs de haut en bas


#--------------------------------Couleurs------------------------------------
BLANC=255,255,255                         #Des constantes sur le RGB des couleurs est utile pour raccourcir et simplifier le programme
GRIS=127,127,127
NOIR=0,0,0
ROUGE=255,0,0
VERT=0,255,0
BLEU=0,0,255
JAUNE=255,255,0
CYAN=0,255,255
MAGENTA=255,0,255

#-----------------------------------Events-----------------------------------
                                          #Des USERSEVENTS sont mis à disposition par pygame pour créer ses propres évenements
POP_BULLE=24                              #L'évenement sera appelé quand une bulle doit éclater
ANIMER=25                                 #L'évement est appelé régulierement pour animer les objets
INVINCIBLE=26                             #L'évenement sera appelé quand l'invincibilité du personnage doit d'arreter
RALENTI=27                                #L'évenement sera appelé quand le rallentissement des ennemis est fini


#------------------------------------Divers-----------------------------------
g=0.3                                     #Valeur arbitraire de l'acceleration dûe à la gravitation
                                          #Ainisi, les objets vont accelerer de 0.3 pixels par frame vers le bas.
