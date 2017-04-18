import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *


pygame.init()

police=pygame.font.Font("Polices/Perfect DOS VGA 437.ttf",20)

with open("Polices/tuto.txt") as fichier:
    f1=fichier.readlines()

f2=[]
for i in f1:
    if i[-1:]=="\n":
        f2.append(i[:-1])

tuto=[]
tuto_rect=[]
for texte in f2:
    t=police.render(texte,0,NOIR)
    tuto.append(t)
    tuto_rect.append(t.get_rect())




pygame.quit()