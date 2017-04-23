import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *

pygame.init()

son_slash=pygame.mixer.Sound("Sons/Slash.wav")
son_wind=pygame.mixer.Sound("Sons/wind.wav")
son_fire=pygame.mixer.Sound("Sons/fire.wav")
son_pop=pygame.mixer.Sound("Sons/pop.wav")
son_electric=pygame.mixer.Sound("Sons/electricity.wav")
