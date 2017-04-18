import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
import texte
from fonctions import *
from classes import *


#-----------------------------Début--------------------------------------

pygame.init()

#----------------------------Chargement des Surfaces--------------------
fenetre=pygame.display.set_mode(taille_fenetre)



#Theme 1

ombre=pygame.Surface((30,30))
ombre.fill(NOIR)
ombre.set_alpha(245)

fond=pygame.image.load('Images/fond.jpg')

img_bulle=pygame.image.load("Images/bulle.png").convert_alpha()

img_porte=pygame.image.load('Images/Fin.bmp')
img_porte.set_colorkey(BLANC)

bloc_plateforme=pygame.image.load("Images//block.png")


img_tp=[pygame.image.load("Images/Teleportation/1.png").convert(),pygame.image.load("Images/Teleportation/2.png").convert(),pygame.image.load("Images/Teleportation/3.png").convert(),pygame.image.load("Images/Teleportation/4.png").convert(),pygame.image.load("Images/Teleportation/5.png").convert()]
for i in img_tp:
    i.set_colorkey(MAGENTA)


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

goomba_img=[pygame.image.load("Images/Goomba/0.png").convert(),pygame.image.load("Images/Goomba/1.png").convert(),pygame.image.load("Images/Goomba/2.png").convert()]
for i in goomba_img:
    i.set_colorkey(MAGENTA)

boule_de_feu_img=   {
                        "droite":[pygame.image.load("Images/Boule de feu/Droite/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Droite/1.bmp").convert(),pygame.image.load("Images/Boule de feu/Droite/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Droite/3.bmp").convert()],
                        "gauche":[pygame.image.load("Images/Boule de feu/Gauche/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Gauche/1.bmp").convert(),pygame.image.load("Images/Boule de feu/Gauche/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Gauche/3.bmp").convert()],
                        "haut":[pygame.image.load("Images/Boule de feu/Haut/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Haut/1.bmp").convert(),pygame.image.load("Images/Boule de feu/Haut/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Haut/3.bmp").convert()],
                        "bas":[pygame.image.load("Images/Boule de feu/Bas/0.bmp").convert(),pygame.image.load("Images/Boule de feu/Bas/1.bmp").convert(),pygame.image.load("Images/Boule de feu/Bas/2.bmp").convert(),pygame.image.load("Images/Boule de feu/Bas/3.bmp").convert()],
                    }

for i in boule_de_feu_img["droite"]:
    i.set_colorkey(CYAN)
for i in boule_de_feu_img["gauche"]:
    i.set_colorkey(CYAN)
for i in boule_de_feu_img["haut"]:
    i.set_colorkey(CYAN)
for i in boule_de_feu_img["bas"]:
    i.set_colorkey(CYAN)


torche_img= {
                "Arret":    pygame.image.load("Images/Torche/Arret.png").convert(),
                "Flamme":   [pygame.image.load("Images/Torche/0.png").convert(),pygame.image.load("Images/Torche/1.png").convert(),pygame.image.load("Images/Torche/2.png").convert(),pygame.image.load("Images/Torche/3.png").convert()]
                }

torche_img["Arret"].set_colorkey(BLANC)
for i in torche_img["Flamme"]:
    i.set_colorkey(BLANC)

img_portail=[pygame.image.load("Images/Porte/0.bmp").convert(),pygame.image.load("Images/Porte/1.bmp").convert(),pygame.image.load("Images/Porte/2.bmp").convert(),pygame.image.load("Images/Porte/3.bmp").convert()]

interrupteur_img={
                    "Ouvert" : pygame.image.load("Images/Interrupteur/Ouvert.png").convert(),
                    "Ferme" : pygame.image.load("Images/Interrupteur/Ferme.png").convert()
                    }

interrupteur_img["Ouvert"].set_colorkey(MAGENTA)
interrupteur_img["Ferme"].set_colorkey(MAGENTA)


fond_pause=pygame.Surface(taille_fenetre)
fond_pause.fill(NOIR)
fond_pause.set_alpha(100)


img_theme_1={
                "fond":fond                         ,
                "porte":img_porte                   ,
                "bloc":bloc_plateforme              ,
                "tp":img_tp                         ,
                "perso":megaman_images              ,
                "torche":torche_img                 ,
                "pause": fond_pause                 ,
                "portail":img_portail               ,
                "ombre":ombre                       ,
                "goomba":goomba_img                 ,
                "interrupteur":interrupteur_img
            }

icone=pygame.image.load("Images/icon.png")
icone.set_colorkey(MAGENTA)
pygame.display.set_icon(icone)
pygame.display.set_caption("C'est mon jeu!!!")

#-----------------------------Création des variables--------------------

#Sons

son_slash=pygame.mixer.Sound("Sons/Slash.wav")
son_wind=pygame.mixer.Sound("Sons/wind.wav")
son_fire=pygame.mixer.Sound("Sons/fire.wav")
son_pop=pygame.mixer.Sound("Sons/pop.wav")
son_electric=pygame.mixer.Sound("Sons/electricity.wav")


duree_frame=0

etat_jeu=0  # 0: jeu de plateforme  1:jeu de dessin
liste_pos=[]

#Creation du niveau
niveau1=Niveau(0,"Niveaux//1.txt",img_theme_1,1)
niveau2=Niveau(1,"Niveaux//2.txt",img_theme_1,1)

#Timer
timer=pygame.time.Clock()

#Events
pygame.time.set_timer(SECONDE,1000)
pygame.time.set_timer(ANIMER,100)

#Pointage
niveau_actuel=niveau1

perso=Personnage((40,480),niveau_actuel.dict_images["perso"])


#-----------------------------Boucle--------------------------------------
continuer=True

while continuer:
#----------------------------Gestion des events---------------------------
    for event in pygame.event.get():

        if event.type==QUIT:
            continuer=False

        if event.type==KEYUP:
            if event.key==K_RIGHT or event.key==K_LEFT:
                perso.vitesse_x=0
                perso.deplacement=False

        if event.type==MOUSEBUTTONDOWN:
            if event.button==3 and etat_jeu==0:
                etat_jeu=1

                liste_pos=[]



        if event.type==MOUSEBUTTONUP:
            if event.button==1 and etat_jeu==1:
                etat_jeu=0
                #Reconnaissance
                if liste_pos!=[]:
                    i_tp=r_tp(liste_pos,perso.rect,[i.rect for i in niveau_actuel.dict_element["tp"]])
                    b_angle,pos_angle=r_angle(liste_pos)
                    b_arc=r_arc_cercle(liste_pos)
                    b_eclair=r_eclair(liste_pos)
                    b_cercle,(c_centre,c_rayon)=r_cercle(liste_pos)
                    b_point,pos_point=r_point(liste_pos)
                    b_trait,trait_l_point=r_droite(liste_pos)
                    b_ellipse,(e_centre,(e_a,e_b))=r_ellipse(liste_pos)


                    #Point
                    if b_point:
                        if perso.double_saut==False and perso.rect.collidepoint(pos_point):
                            perso.double_saut=True
                            perso.vitesse_y=-6

                    #Teleportation

                    elif i_tp!=-1:
                        tp=niveau_actuel.dict_element["tp"][i_tp]
                        if tp.etat!=4:
                            perso.vitesse_y=0
                            perso.rect.center=tp.rect.center

                    #Eclair
                    elif b_eclair:
                        elif b_eclair:
                            for i in interrupteur.liste:
                                if i.rect.collidepoint(liste_pos[-1]):
                                    son_electric.play()
                                    interrupteur.ouvert=False
                                    for porte in Porte.liste:
                                        porte.ouvert=True

                    #Cercle
                    elif b_cercle:
                        son_pop.play()
                        liste_obj_bulle=[]
                        liste_obj_bulle.append(perso)
                        for i in niveau_actuel.dict_element["goomba"]:
                            liste_obj_bulle.append(i)

                        liste_obj_proche=[i for i in liste_obj_bulle if distance(i.rect.center,c_centre)<c_rayon]
                        for i,elem in enumerate([distance(i.rect.center,c_centre) for i in liste_obj_proche]):
                            if elem==min([distance(i.rect.center,c_centre) for i in liste_obj_proche]):
                                obj=liste_obj_proche[i]
                        try :
                            b=Bulle(img_bulle,obj)
                            niveau_actuel.dict_element["bulle"].append(b)
                            del obj
                        except NameError:
                            pass


                    #Ellipse
                    elif b_ellipse:
                        print('ellipse',e_centre,(e_a,e_b))
                    
                    #Angle
                    elif b_angle!=False:
                        son_fire.play()
                        boule_de_feu=BouleFeu(boule_de_feu_img,b_angle,perso)
                        niveau_actuel.dict_element["boule feu"].append(boule_de_feu)
                    
                    
                    #Arc de cercle
                    elif b_arc!=False:
                        son_wind.play()
                        niveau_actuel.vent=True,b_arc
                        pygame.time.set_timer(VENT,1000)
                        niveau_actuel.dict_element["boule feu"]=[]
                        for i in niveau_actuel.dict_element["torche"]:
                            i.enflamme=False
                    #Trait
                    elif b_trait:
                        son_slash.play()

                        for point in trait_l_point:

                            for porte in niveau_actuel.dict_element["porte"]:
                                if porte.rect.collidepoint(point):
                                    porte.ouvert=True
                            for torche in niveau_actuel.dict_element["torche"]:
                                if torche.rect.collidepoint(point):
                                    torche.enflamme=False
                            for bulle in niveau_actuel.dict_element["bulle"]:
                                if bulle.rect.collidepoint(point):
                                    bulle.obj.acceleration_y=g
                                    bulle.obj.vitesse_y=0
                                    niveau_actuel.dict_element["bulle"].remove(bulle)
                                    del bulle
                            for goomba in niveau_actuel.dict_element["goomba"]:
                                if goomba.rect.collidepoint(point):
                                    niveau_actuel.dict_element["goomba"].remove(goomba)
                                    del goomba

                    b_point,b_arc,b_eclair,b_angle,b_trait,b_cercle,i_tp=False,False,False,False,False,False,-1

        if event.type==ANIMER:
            perso.animation+=1
            if perso.animation>=4:
                perso.animation=0

            for b in niveau_actuel.dict_element["boule feu"]:
                b.animation+=1
                if b.animation>=4:
                    b.animation=0

            for go in niveau_actuel.dict_element["goomba"]:
                go.animation+=1
                if go.animation>=3:
                    go.animation=0

            for t in niveau_actuel.dict_element["torche"]:
                t.animation+=1
                if t.animation>=4:
                    t.animation=0
            for p in niveau_actuel.dict_element["porte"]:
                if p.ouvert==True and p.animation<3:
                    p.animation+=1

        if event.type==VENT:
            pygame.time.set_timer(VENT,0)
            niveau_actuel.vent=False,None


    touches=pygame.key.get_pressed()

    if touches[K_RIGHT] and perso.deplacement==False:
        perso.vitesse_x+=100
        perso.deplacement=True
        perso.direction="droite"

    if touches[K_LEFT] and perso.deplacement==False:
        perso.vitesse_x-=100
        perso.deplacement=True
        perso.direction="gauche"

    if touches[K_UP] and perso.saut==False:
        perso.vitesse_y=-6


    if etat_jeu==1:
        souris=pygame.mouse.get_pressed()
        if souris[0]:

            liste_pos.append(pygame.mouse.get_pos())



#---------------------------Gestion des variable--------------------------
    if etat_jeu==0:
        niveau_actuel.update(perso)

        victoire=perso.update(duree_frame,niveau_actuel)

        for b in niveau_actuel.dict_element["boule feu"]:
            b.update(duree_frame,niveau_actuel)
        for t in niveau_actuel.dict_element["torche"]:
            t.update(niveau_actuel)
        for p in niveau_actuel.dict_element["porte"]:
            p.update()
        for b in niveau_actuel.dict_element["bulle"]:
            b.update(niveau_actuel)
        for t in niveau_actuel.dict_element["tp"]:
            t.update(perso)
        for go in niveau_actuel.dict_element["goomba"]:
            go.update(duree_frame,niveau_actuel)
        for i in Interrupteur.liste:
            i.update()

        if victoire=="win":
            perso=Personnage((40,480),niveau_actuel.dict_images["perso"])
            try:
                niveau_actuel=Niveau.liste[niveau_actuel.numero+1]
            except IndexError:
                print("TU AS GAGNE T'ES LE MEILLEUR DE TOUS!!")
#---------------------------Affichage-------------------------------------
    fenetre.blit(niveau_actuel.dict_images['fond'],(0,0))

    for i in niveau_actuel.dict_element["bloc"]:
        fenetre.blit(i.img,i.rect)

    fenetre.blit(niveau_actuel.dict_element["fin"].img,niveau_actuel.dict_element["fin"].rect)

    for i in niveau_actuel.dict_element["tp"]:
        fenetre.blit(i.img,i.rect)

    for i in niveau_actuel.dict_element["torche"]:
        fenetre.blit(i.img,i.rect)

    for i in niveau_actuel.dict_element["porte"]:
        fenetre.blit(i.img,i.rect)

    for i in niveau_actuel.dict_element["goomba"]:
        fenetre.blit(i.img,i.rect)


    for boule in niveau_actuel.dict_element["boule feu"]:
        fenetre.blit(boule.img,boule.rect)

    for bulle in niveau_actuel.dict_element["bulle"]:
        fenetre.blit(bulle.img,bulle.rect)
        
    for interrupteur in Interrupteur.liste:
        fenetre.blit(interrupteur.img,interrupteur.rect)

    fenetre.blit(perso.img,perso.rect)

    #Textes
    if niveau_actuel.numero==0:
        fenetre.blit(texte.tuto[0],(0,0))
        fenetre.blit(texte.tuto[1],(0,25))


    if etat_jeu==1:
        fenetre.blit(niveau_actuel.dict_images['pause'],(0,0))

        for i in range(len(liste_pos)-1):
            pygame.draw.line(fenetre,ROUGE,liste_pos[i+1],liste_pos[i],8)

    for o in niveau_actuel.liste_ombre:
        fenetre.blit(niveau_actuel.dict_images["ombre"],o)

    pygame.display.flip()

#----------------------------Gestion du temps-----------------------------
    timer.tick(30)
    fps=timer.get_fps()
    if fps!=0:
        duree_frame=1/fps
    else:
        duree_frame=0

pygame.quit()

