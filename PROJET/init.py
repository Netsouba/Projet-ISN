import pygame
from pygame.locals import *
import os
import math
from copy import deepcopy


from constantes import *

pygame.init()

#--------------------------------------------Sons----------------------------------------------------------------------------------------------------------------
son_slash=pygame.mixer.Sound("Sons/Slash.wav")
son_wind=pygame.mixer.Sound("Sons/wind.wav")
son_fire=pygame.mixer.Sound("Sons/fire.wav")
son_pop=pygame.mixer.Sound("Sons/pop.wav")
son_electric=pygame.mixer.Sound("Sons/electricity.wav")


#----------------------------------------------Texte--------------------------------------------------------------------------------------------------------------
p_funny=pygame.font.Font("Polices/Packaging Funny.otf",40)
p_candy=pygame.font.Font("Polices/Candy_Pop!-demo-font.ttf",90)
p_perfect=pygame.font.Font("Polices/Perfect DOS VGA 437.ttf",20)

#-------------------------Menu--------------------------------------------------
titre=p_candy.render("NOM DU JEU",1,CYAN)
titre_2=p_funny.render("Appuyez sur une touche pour continuer",1,BLANC)
nombres=[p_funny.render(str(i+1),1,JAUNE) for i in range(24)]
titre_menu=p_candy.render("Choix du niveau",1,JAUNE)

#-----------Game over--------------------
police=pygame.font.Font("Polices/Packaging Funny.otf",100)

titre_over= police.render("GAME OVER",0, ROUGE )
titre_over_rect= titre_over.get_rect()

bloc_menu=police.render("Menu",0,ROUGE)
bloc_retry=police.render("Retry",0,ROUGE)

bloc_menu_rect=bloc_menu.get_rect()
bloc_retry_rect=bloc_retry.get_rect()


#--------------------------------------------Images---------------------------------------------------------------------------------------------------------------

fenetre=pygame.display.set_mode(taille_fenetre)

#--------------------------------------------------Menu----------------------------------------------
fond_ecran=pygame.image.load("Images/Fonds/fond_ecran.jpg")
img_fond_menu=pygame.image.load("Images/Fonds/ecran_accueil.jpg").convert()
img_boite=pygame.image.load("Images/Structure/boite.png").convert()
img_boite.set_colorkey(BLANC)

img_fleche_droite=pygame.image.load("Images/Fleche/droite.png").convert()
img_fleche_droite.set_colorkey(BLANC)
img_fleche_gauche=pygame.image.load("Images/Fleche/gauche.png").convert()
img_fleche_gauche.set_colorkey(BLANC)

#--------------------------------------------------Game Over----------------------------------------------
game_over_fond= pygame.Surface(taille_fenetre)
game_over_fond.fill(NOIR)
game_over_fond.set_alpha(100)

menu_over=pygame.image.load("Images/Game Over/Menu_over.png").convert()
retry_over=pygame.image.load("Images/Game Over/Retry_over.png").convert()
skip_over=pygame.image.load("Images/Game Over/Skip.png").convert()

menu_over.set_colorkey(BLANC)
retry_over.set_colorkey(BLANC)
skip_over.set_colorkey(NOIR)


#----------------------------------Perso---------------------

megaman_images= {
                    "droite":
                    {"debout":  pygame.image.load("Images\\Megaman\\Droite\\Debout.png").convert(),
                     "cours":   [pygame.image.load("Images\\Megaman\\Droite\\Cours\\1.png").convert(),pygame.image.load("Images\\Megaman\\Droite\\Cours\\2.png").convert(),pygame.image.load("Images\\Megaman\\Droite\\Cours\\3.png").convert(),pygame.image.load("Images\\Megaman\\Droite\\Cours\\2.png").convert()],
                     "saute":   pygame.image.load("Images\\Megaman\\Droite\\Saute.png").convert()},

                    "gauche":
                    {"debout":  pygame.image.load("Images\\Megaman\\Gauche\\Debout.png").convert(),
                     "cours":   [pygame.image.load("Images\\Megaman\\Gauche\\Cours\\1.png").convert(),pygame.image.load("Images\\Megaman\\Gauche\\Cours\\2.png").convert(),pygame.image.load("Images\\Megaman\\Gauche\\Cours\\3.png").convert(),pygame.image.load("Images\\Megaman\\Gauche\\Cours\\2.png").convert()],
                    "saute":    pygame.image.load("Images\\Megaman\\Gauche\\Saute.png").convert()}
                }

megaman_images["droite"]["debout"].set_colorkey(MAGENTA)
megaman_images["droite"]["saute"].set_colorkey(MAGENTA)
for i in megaman_images["droite"]["cours"]:
    i.set_colorkey(MAGENTA)
megaman_images["gauche"]["debout"].set_colorkey(MAGENTA)
megaman_images["gauche"]["saute"].set_colorkey(MAGENTA)
for i in megaman_images["gauche"]["cours"]:
    i.set_colorkey(MAGENTA)


#Interface
img_reset=pygame.image.load("Images/Structure/Reset.png").convert_alpha()
img_menu=pygame.image.load("Images/Structure/menu.png").convert_alpha()
img_info=pygame.image.load("Images/Structure/info.png").convert_alpha()
img_retour=pygame.image.load("Images/Structure/retour.png").convert_alpha()
liste_img_formes=   [pygame.image.load("Images/Formes/Trait.png").convert(),pygame.image.load("Images/Formes/Point.png").convert(),pygame.image.load("Images/Formes/Cercle.png").convert(),pygame.image.load("Images/Formes/TP.png").convert(),
                    pygame.image.load("Images/Formes/Angle.png").convert(),pygame.image.load("Images/Formes/Eclair.png").convert(),pygame.image.load("Images/Formes/Ellipse.png")]
filtre_cooldown=pygame.Surface((40,40))
filtre_cooldown.fill(NOIR)
filtre_cooldown.set_alpha(100)

#--------------------------------------Theme 1------------------------------------------------

ombre=pygame.Surface((30,30))
ombre.fill(NOIR)


fond=pygame.image.load('Images/Fonds/fond.jpg')


img_bulle=pygame.image.load("Images/Structure/bulle.png").convert_alpha()


img_porte=pygame.image.load('Images/Structure/Fin.bmp')
img_porte.set_colorkey(BLANC)


bloc_plateforme=pygame.image.load("Images/Structure/block.png")


img_tp=[pygame.image.load("Images/Teleportation/1.png").convert(),pygame.image.load("Images/Teleportation/2.png").convert(),pygame.image.load("Images/Teleportation/3.png").convert(),pygame.image.load("Images/Teleportation/4.png").convert(),pygame.image.load("Images/Teleportation/5.png").convert()]
for i in img_tp:
    i.set_colorkey(MAGENTA)


goomba_img=[pygame.image.load("Images/Goomba/0.png").convert(),pygame.image.load("Images/Goomba/1.png").convert(),pygame.image.load("Images/Goomba/2.png").convert()]
for i in goomba_img:
    i.set_colorkey(MAGENTA)

koopa_img= [pygame.image.load("Images/Koopa/1.png").convert(),pygame.image.load("Images/Koopa/2.png").convert(),pygame.image.load("Images/Koopa/3.png").convert(),pygame.image.load("Images/Koopa/4.png").convert(),]
for i in koopa_img:
    i.set_colorkey(MAGENTA)


boule_de_feu_img=   {
                        "droite":   [pygame.image.load("Images/Boule de feu/Droite/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Droite/1.bmp").convert(),
                                    pygame.image.load("Images/Boule de feu/Droite/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Droite/3.bmp").convert()],

                        "gauche":   [pygame.image.load("Images/Boule de feu/Gauche/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Gauche/1.bmp").convert(),
                                    pygame.image.load("Images/Boule de feu/Gauche/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Gauche/3.bmp").convert()],

                        "haut":     [pygame.image.load("Images/Boule de feu/Haut/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Haut/1.bmp").convert(),
                                    pygame.image.load("Images/Boule de feu/Haut/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Haut/3.bmp").convert()],

                        "bas":      [pygame.image.load("Images/Boule de feu/Bas/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Bas/1.bmp").convert(),
                                    pygame.image.load("Images/Boule de feu/Bas/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Bas/3.bmp").convert()],
                    }
for i in boule_de_feu_img.values():
    i=[e.set_colorkey(CYAN) for e in i]


torche_img= {
                "Arret":    pygame.image.load("Images/Torche/Arret.png").convert(),
                "Flamme":   [pygame.image.load("Images/Torche/0.png").convert(),pygame.image.load("Images/Torche/1.png").convert(),pygame.image.load("Images/Torche/2.png").convert(),
                            pygame.image.load("Images/Torche/3.png").convert()]
                }
torche_img["Arret"].set_colorkey(BLANC)
for i in torche_img["Flamme"]:
    i.set_colorkey(BLANC)


img_portail=[pygame.image.load("Images/Porte/0.bmp").convert(),pygame.image.load("Images/Porte/1.bmp").convert(),pygame.image.load("Images/Porte/2.bmp").convert(),pygame.image.load("Images/Porte/3.bmp").convert()]
for i in img_portail:
    i.set_colorkey(BLANC)

img_portail_b=[pygame.image.load("Images/Porte button/0.bmp").convert(),pygame.image.load("Images/Porte button/1.bmp").convert(),pygame.image.load("Images/Porte button/2.bmp").convert(),pygame.image.load("Images/Porte button/3.bmp").convert()]
for i in img_portail_b:
    i.set_colorkey(BLANC)

img_portail_i=  [pygame.image.load("Images/Porte interrupteur/0.bmp").convert(),pygame.image.load("Images/Porte interrupteur/1.bmp").convert(),
                pygame.image.load("Images/Porte interrupteur/2.bmp").convert(),pygame.image.load("Images/Porte interrupteur/3.bmp").convert()]
for i in img_portail_i:
    i.set_colorkey(BLANC)

interrupteur_img={
                    "Ouvert" : pygame.image.load("Images/Interrupteur/Ouvert.png").convert(),
                    "Ferme" : pygame.image.load("Images/Interrupteur/Ferme.png").convert()
                    }

interrupteur_img["Ouvert"].set_colorkey(MAGENTA)
interrupteur_img["Ferme"].set_colorkey(MAGENTA)

bouton_img=[pygame.image.load("Images/Bouton/0.png").convert(),pygame.image.load("Images/Bouton/1.png").convert()]


fond_pause=pygame.Surface(taille_fenetre)
fond_pause.fill(NOIR)
fond_pause.set_alpha(100)

pic=pygame.image.load('Images/Structure/pics.png').convert()
pic.set_colorkey(MAGENTA)

pot=pygame.image.load('Images/Structure/ink_pot.png').convert_alpha()

coeur=pygame.image.load('Images/Structure/coeur.png').convert_alpha()

img_caisse=pygame.image.load("Images/Structure/box.png").convert()

img_theme_1={
                "fond":fond                         ,
                "fin":img_porte                     ,
                "bloc":bloc_plateforme              ,
                "tp":img_tp                         ,
                "torche":torche_img                 ,
                "pause": fond_pause                 ,
                "porte":img_portail                 ,
                "ombre":ombre                       ,
                "goomba":goomba_img                 ,
                "koopa": koopa_img                  ,
                "interrupteur":interrupteur_img     ,
                "porte interrupteur":img_portail_i  ,
                "porte bouton":img_portail_b        ,
                "bouton":bouton_img                 ,
                "pic":pic                           ,
                "pot":pot                           ,
                "coeur":coeur                       ,
                "caisse":img_caisse
            }


#-------------------------------------------------------------------------Autre-----------------------------------------------------------------
icone=pygame.image.load("Images/Structure/icon.png")
icone.set_colorkey(MAGENTA)
