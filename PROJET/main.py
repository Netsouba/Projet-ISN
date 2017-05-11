import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from classes import *
from init import *          #Création de la fenetre, des images et des sons
from fonctions_jeu import *



#-----------------------------Début--------------------------------------
pygame.init()                                                   #Initialisation du module pygame
pygame.display.set_icon(icone)                                  #Mise en place de l'icone du jeu
pygame.display.set_caption("Puzzling Drawer")                   #Création du titre de la fenetre


#---------------------------Creation des niveaux------------------------
for i in range(24):                                             #On fait une boucle pour créer tous les niveaux
    if i==1:pos=40,40                                           #La position de départ change selon le numero du niveau
    elif i==18:pos=40,110
    elif i==19:pos=40,40
    else:pos=40,480
    Niveau(i,img_niveau,pos)                                    #On créer l'objet Niveau.

if accueil()=="continuer":                                      #On lance l'écran d'accueil. On continue si il a choisi de continuer.
    continuer=True                                              #On fait une boucle infini qui exécute le menu et le jeu.
    while continuer:

        niveau_actuel=menu()                                    #On excécute le menu et on capture le numero choisi

        if niveau_actuel!=None:                                 #On teste si l'utilisateur n'a pas quitté le jeu
            musique("Sons/music_jeu.wav")                       #On lance la musique grâce à notre fonction musique
            while True:                                         #On fait une boucle infini qui éxecute le jeu

                if niveau_actuel<len(Niveau.liste):             #Si le niveau à executer est cohérent par rapport à la liste des niveaux
                    etat=jeu(Niveau.liste[niveau_actuel])       #On exécute le jeu, et on capture dans etat quelque chose si le jeu est fini
                    if etat=="suivant":                         #Si le joueur doit aller au niveau suivant
                        niveau_actuel+=1                        #On incrémente la variable niveau_actuel, puis la boucle recommence avec le nouveau niveau
                    elif etat=="menu":                          #Si le joueur doit revenir au menu
                        break                                   #On sort de la boucle de la ligne 37, sans quitter la boucle de la ligne 31, pour revenir au menu
                    elif etat=="reset":                         #Si le joueur doit recommencer le niveau
                        pass                                    #On ne fait rien, donc la boucle recommence, avec le même niveau
                    elif etat=="fin":                           #Si le joueur quitte le jeu
                        continuer=False                         #On sort de la boucle de la ligne 31
                        break                                   #On sort de la boucle de la ligne 37

                else:                                           #Si le niveau à executer n'appartient plus à la liste des niveaux
                    pygame.image.save(fenetre,"temp/save.png")  #On fait une capture de l'écran
                    img_vctr=pygame.image.load("temp/save.png")
                    v=victoire(img_vctr)                        #Puis on exécute l'écran de victoire
                    if v=="fin":                                #Si l'utilisateur a quitté dans l'écran de victoire:
                        continuer=False                         #On sort de la boucle de la ligne 31
                        break                                   #On sort de la boucle de la ligne 37
                    elif v=="menu":                             #Si l'utilisateur a choisi de retourner au menu:
                        son_victory.stop()                      #On stoppe l'effet sonore de la victoire
                        pygame.mixer.music.play()               #On rejoue la musique
                        break                                   #On sort de la boucle de la ligne 37, sans quitter la boucle de la ligne 31, pour revenir au menu




        else:                                                   #Si l'utilisateur a quitté le jeu pendant le menu:
            continuer=False                                     #On quitte la boucle

pygame.quit()                                                   #Une fois que l'utilisateur a quitté les deux boucles, on déinitialise pygame et le programme est fini
