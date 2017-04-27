import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
from fonctions import *
from classes import *
from init import *

def jeu(niveau_actuel):

    #Variables diverses
    niveau_actuel.creation()
    perso=Personnage(niveau_actuel.depart,megaman_images)
    liste_pos=[]
    duree_frame=0
    etat_jeu=0  # 0: jeu de plateforme  1:jeu de dessin
    timer=pygame.time.Clock()

    #-----------------------------Boucle--------------------------------------

    while True:

    #----------------------------Gestion des events---------------------------
        for event in pygame.event.get():

            if event.type==QUIT:
                return "fin"

            if event.type==KEYUP:
                if event.key==K_RIGHT or event.key==K_LEFT:
                    perso.vitesse_x=0
                    perso.deplacement=False

            if event.type==MOUSEBUTTONDOWN:
                if event.button==3 and etat_jeu==0:
                    etat_jeu=1

                    liste_pos=[]

                if event.button==1:
                    if pygame.Rect(400,2,40,40).collidepoint(event.pos):
                        return "menu"
                    if pygame.Rect(450,2,40,40).collidepoint(event.pos):
                        return "reset"

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
                            if perso.double_saut==False and perso.rect.collidepoint(pos_point) and perso.energie>1:
                                perso.energie-=1
                                perso.double_saut=True
                                perso.vitesse_y=-6

                        #Teleportation

                        elif i_tp!=-1:
                            tp=niveau_actuel.dict_element["tp"][i_tp]
                            if tp.etat!=4 and perso.energie>tp.etat:
                                perso.energie-=tp.etat
                                perso.vitesse_y=0
                                perso.rect.center=tp.rect.center

                        #Eclair
                        elif b_eclair and perso.energie>3:
                            perso.energie-=3
                            son_electric.play()
                            niveau_actuel.dict_images["ombre"].set_alpha(0)
                            niveau_actuel.eclair=True
                            for i in niveau_actuel.dict_element["interrupteur"]:
                                for p in liste_pos:
                                    if i.rect.collidepoint(p):
                                        i.ouvert=not i.ouvert
                                        break
                            for go in niveau_actuel.dict_element["goomba"]:
                                for p in liste_pos:
                                    if go.rect.collidepoint(p):
                                        niveau_actuel.dict_element["goomba"].remove(go)
                                        break
                            for t in niveau_actuel.dict_element["torche"]:
                                for p in liste_pos:
                                    if t.rect.collidepoint(p):
                                        t.enflamme=True


                        #Cercle
                        elif b_cercle and perso.energie>2:
                            perso.energie-=2
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
                        elif b_ellipse and perso.energie>2:
                            perso.energie-=2
                            print('ellipse',e_centre,(e_a,e_b))

                        #Angle
                        elif b_angle!=False and perso.energie>3:
                            perso.energie-=3
                            son_fire.play()
                            boule_de_feu=BouleFeu(boule_de_feu_img,b_angle,perso)
                            niveau_actuel.dict_element["boule feu"].append(boule_de_feu)

                        #Trait
                        elif b_trait and perso.energie>1:
                            perso.energie-=1
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
                    elif p.ouvert==False and p.animation>0:
                        p.animation-=1

                for p in niveau_actuel.dict_element["porte interrupteur"]:
                    if p.ouvert==True and p.animation<3:
                        p.animation+=1
                    elif p.ouvert==False and p.animation>0:
                        p.animation-=1

                for p in niveau_actuel.dict_element["porte bouton"]:
                    if p.ouvert==True and p.animation<3:
                        p.animation+=1
                    elif p.ouvert==False and p.animation>0:
                        p.animation-=1

            if event.type==INVINCIBLE:
                pygame.time.set_timer(INVINCIBLE,0)
                perso.invincible=False


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


            p=perso.update(duree_frame,niveau_actuel)
            if p!=None:
                if p=="mort" or p=="win":
                    return p
                if p=="touche":
                    pygame.time.set_timer(INVINCIBLE,2000)
                    perso.invincible=True

            for a in niveau_actuel.dict_element.values():
                for i in a:
                    etat=i.update(perso,duree_frame,niveau_actuel)




    #---------------------------Affichage-------------------------------------
        #Fond
        fenetre.blit(niveau_actuel.dict_images['fond'],(0,0))

        #Elements du niveau
        for a in niveau_actuel.dict_element.values():
            for i in a:
                fenetre.blit(i.img,i.rect)

        #Perso
        if perso.clignotant==False or perso.animation%2==0:
            fenetre.blit(perso.img,perso.rect)

        #Ombres
        for o in niveau_actuel.liste_ombre:

            fenetre.blit(niveau_actuel.dict_images["ombre"],o)
        #Pause
        if etat_jeu==1:
            fenetre.blit(niveau_actuel.dict_images['pause'],(0,0))

            for i in range(len(liste_pos)-1):
                pygame.draw.line(fenetre,ROUGE,liste_pos[i+1],liste_pos[i],8)

        #Interface
        pygame.draw.rect(fenetre,VERT,(2,2,10+60*perso.pv,26))
        pygame.draw.rect(fenetre,NOIR,(2,2,10+60*perso.pv,26),2)
        pygame.draw.rect(fenetre,BLEU,(2,30,10+20*perso.energie,26))
        pygame.draw.rect(fenetre,NOIR,(2,30,10+20*perso.energie,26),2)
        for i,forme in enumerate(liste_img_formes):
            if i<niveau_actuel.numero:
                fenetre.blit(forme,(618+i*50,2))
        fenetre.blit(img_menu,(400,2))
        fenetre.blit(img_reset,(450,2))
        pygame.display.flip()

    #----------------------------Gestion du temps-----------------------------
        timer.tick(30)
        fps=timer.get_fps()
        if fps!=0:
            duree_frame=1/fps
        else:
            duree_frame=0
