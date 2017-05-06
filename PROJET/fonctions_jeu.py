import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from classes import *
from init import *



def accueil():
    musique("Sons/fond_menu.wav")
    titre_rect=titre.get_rect()
    titre_2_rect=titre_2.get_rect()
    titre_rect.center=fenetre_x/2,fenetre_y/4
    titre_2_rect.center=fenetre_x/2,4*fenetre_y/5
    visible=True
    pygame.time.set_timer(ANIMER,500)



    while True:
        for event in pygame.event.get():
            if event.type==QUIT:    return None
            if event.type==KEYDOWN or event.type==MOUSEBUTTONDOWN:  return "continuer"
            if event.type==ANIMER: visible=not visible

        fenetre.blit(fond_ecran,(0,0))
        fenetre.blit(titre,titre_rect)
        if visible:fenetre.blit(titre_2,titre_2_rect)
        pygame.display.flip()


def menu():


    titre_menu_rect=titre_menu.get_rect()
    nombres_rect=[i.get_rect() for i in nombres]

    fenetre_actuelle=0

    rect_fleche_droite=img_fleche_droite.get_rect()
    rect_fleche_gauche=img_fleche_gauche.get_rect()
    rect_fleche_droite.centery=rect_fleche_gauche.centery=9*fenetre_y/10
    rect_fleche_droite.centerx=7*fenetre_x/8
    rect_fleche_gauche.centerx=fenetre_x/8

    liste_boite_rect=[]
    titre_menu_rect.center=fenetre_x/2,fenetre_y/4

    for i in range(len(nombres)//4):

        nombres_rect[i].center=(i+1)*fenetre_x/7,fenetre_y/2
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i].center
        liste_boite_rect.append(rect)
    for i in range(len(nombres)//4):
        nombres_rect[i+6].center=(i+1)*fenetre_x/7,3*fenetre_y/4
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i+6].center
        liste_boite_rect.append(rect)
    for i in range(len(nombres)//4):
        nombres_rect[i+12].center=(i+1)*fenetre_x/7,fenetre_y/2
    for i in range(len(nombres)//4):
        nombres_rect[i+18].center=(i+1)*fenetre_x/7,3*fenetre_y/4




    while True:

        for event in pygame.event.get():
            if event.type==QUIT:
                return None
            if event.type==MOUSEBUTTONDOWN:
                for i,rect in enumerate(liste_boite_rect):
                    if rect.collidepoint(event.pos):
                        return i+fenetre_actuelle

                if rect_fleche_droite.collidepoint(event.pos):
                    fenetre_actuelle=12
                elif rect_fleche_gauche.collidepoint(event.pos):
                    fenetre_actuelle=0


        fenetre.blit(img_fond_menu,(0,0))

        fenetre.blit(titre_menu,titre_menu_rect)
        for i in range(len(nombres)//2):
            fenetre.blit(img_boite,liste_boite_rect[i])
            fenetre.blit(nombres[i+fenetre_actuelle],nombres_rect[i+fenetre_actuelle])

        if fenetre_actuelle==0:
            fenetre.blit(img_fleche_droite,rect_fleche_droite)
        else:
            fenetre.blit(img_fleche_gauche,rect_fleche_gauche)
        pygame.display.flip()



def jeu(niveau_actuel):

    #Variables diverses


    niveau_actuel.creation()
    perso=Personnage(niveau_actuel.depart,megaman_images)
    liste_pos=[]
                                 # 0      1     2    3    4     5       6
    liste_t_forme=[0,0,0,0,0,0,0]#Trait,point,cercle,tp,angle,eclair,ellipse
    liste_base_cooldown=[3000,2000,8000,1,5000,5000,10000]
    liste_cooldown=deepcopy(liste_base_cooldown)
    duree_frame=0
    etat_jeu=0  # 0: jeu de plateforme  1:jeu de dessin     2:astuce
    pygame.time.set_timer(ANIMER,100)
    timer=pygame.time.Clock()
    animation=0
    longueur=0

    #-----------------------------Boucle--------------------------------------

    while True:

    #----------------------------Gestion des events---------------------------
        for event in pygame.event.get():

            if event.type==QUIT:
                return "fin"

            if event.type==KEYDOWN:
                for i in niveau_actuel.dict_element["caisse"]:
                    if event.key==K_SPACE and distance(perso.rect.center,i.rect.center)<=30:
                        if i.hold==None:
                            if perso.rect.x<i.rect.x:
                                i.hold="gauche"
                            else:
                                i.hold="droite"
                        else:
                            i.hold=None

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
                        musique("Sons/fond_menu.wav")
                        return "menu"
                    if pygame.Rect(450,2,40,40).collidepoint(event.pos):
                        return "reset"
                    if pygame.Rect(500,2,40,40).collidepoint(event.pos):
                        a_e=etat_jeu
                        etat_jeu=2
                    if pygame.Rect(550,2,40,40).collidepoint(event.pos) and etat_jeu==2:
                        if niveau_actuel.dict_element["bloc_tuto"]!=[]:
                            niveau_actuel.dict_element["bloc_tuto"][0].toucher=True
                        etat_jeu=a_e


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

                            if perso.double_saut==False and perso.rect.collidepoint(pos_point) and perso.energie>1 and liste_cooldown[1]==liste_base_cooldown[1]:
                                liste_t_forme[1]=pygame.time.get_ticks()
                                perso.energie-=1
                                perso.double_saut=True
                                perso.vitesse_y=-6

                        #Teleportation

                        elif i_tp!=-1:
                            tp=niveau_actuel.dict_element["tp"][i_tp]
                            if tp.etat!=4 and perso.energie>tp.etat and liste_cooldown[3]==liste_base_cooldown[3]:
                                liste_t_forme[3]=pygame.time.get_ticks()
                                perso.energie-=3*tp.etat
                                perso.vitesse_y=0
                                perso.rect.center=tp.rect.center

                        #Eclair
                        elif b_eclair and perso.energie>3 and liste_cooldown[5]==liste_base_cooldown[5]:
                            liste_t_forme[5]=pygame.time.get_ticks()
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
                        elif b_cercle and perso.energie>2 and liste_cooldown[2]==liste_base_cooldown[2]:
                            liste_t_forme[2]=pygame.time.get_ticks()
                            perso.energie-=2
                            son_pop.play()
                            liste_obj_bulle=[]
                            liste_obj_bulle.append(perso)
                            for i in niveau_actuel.dict_element["goomba"]:
                                liste_obj_bulle.append(i)
                            for i in niveau_actuel.dict_element["caisse"]:
                                liste_obj_bulle.append(i)

                            liste_obj_proche=[i for i in liste_obj_bulle if distance(i.rect.center,c_centre)<c_rayon]
                            for i,elem in enumerate([distance(i.rect.center,c_centre) for i in liste_obj_proche]):
                                if elem==min([distance(i.rect.center,c_centre) for i in liste_obj_proche]):
                                    obj=liste_obj_proche[i]
                            try :
                                b=Bulle(img_bulle,obj)
                                niveau_actuel.dict_element["bulle"].append(b)
                                del obj
                                pygame.time.set_timer(POP_BULLE,4000)
                            except NameError:
                                pass


                        #Ellipse
                        elif b_ellipse and perso.energie>2 and liste_cooldown[6]==liste_base_cooldown[6]:
                            liste_t_forme[6]=pygame.time.get_ticks()
                            perso.energie-=2
                            niveau_actuel.ralenti=0.1
                            pygame.time.set_timer(RALENTI,8000)
                            pygame.time.set_timer(ANIMER,1000)

                        #Angle
                        elif b_angle!=False and perso.energie>3 and liste_cooldown[4]==liste_base_cooldown[4]:
                            liste_t_forme[4]=pygame.time.get_ticks()
                            perso.energie-=3
                            son_fire.play()
                            boule_de_feu=BouleFeu(boule_de_feu_img,b_angle,perso)
                            niveau_actuel.dict_element["boule feu"].append(boule_de_feu)

                        #Trait
                        elif b_trait and perso.energie>1 and liste_cooldown[0]==liste_base_cooldown[0]:
                            liste_t_forme[0]=pygame.time.get_ticks()
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

                        b_point=b_ellipse=b_eclair=b_angle=b_trait=b_cercle=False
                        i_tp=-1

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

                for go in niveau_actuel.dict_element["koopa"]:
                    go.animation+=1
                    if go.animation>=4:
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

                if etat_jeu==2:
                    animation+=1
                    if animation>=longueur:
                        animation=0




            if event.type==INVINCIBLE:
                pygame.time.set_timer(INVINCIBLE,0)
                perso.invincible=False

            if event.type==POP_BULLE:
                pygame.time.set_timer(POP_BULLE,0)
                if niveau_actuel.dict_element["bulle"]!=[]:
                    bulle=niveau_actuel.dict_element["bulle"][0]
                    bulle.obj.acceleration_y=g
                    bulle.obj.vitesse_y=0
                    niveau_actuel.dict_element["bulle"].remove(bulle)
                    del bulle

            if event.type==RALENTI:
                pygame.time.set_timer(RALENTI,0)
                pygame.time.set_timer(ANIMER,100)
                niveau_actuel.ralenti=1

        touches=pygame.key.get_pressed()

        if touches[K_RIGHT] and perso.deplacement==False:
            perso.vitesse_x+=100
            perso.deplacement=True
            perso.direction="droite"
            for i in niveau_actuel.dict_element["caisse"]:
                if distance(i.rect.center,perso.rect.center)>35:
                    i.hold=False

        if touches[K_LEFT] and perso.deplacement==False:
            perso.vitesse_x-=100
            perso.deplacement=True
            perso.direction="gauche"
            for i in niveau_actuel.dict_element["caisse"]:
                if distance(i.rect.center,perso.rect.center)>35:
                    i.hold=False

        if touches[K_UP] and perso.saut==False:
            perso.vitesse_y=-6
            for i in niveau_actuel.dict_element["caisse"]:
                i.hold=False


        if etat_jeu==1:
            souris=pygame.mouse.get_pressed()
            if souris[0]:

                liste_pos.append(pygame.mouse.get_pos())



    #---------------------------Gestion des variable--------------------------
        if etat_jeu==0:


            niveau_actuel.update(perso)


            p=perso.update(duree_frame,niveau_actuel)
            if p!=None:
                if p=="mort":
                    pygame.mixer.music.stop()
                    pygame.image.save(fenetre,"temp/save.png")
                    son_game_over.play()
                    return game_over(pygame.image.load("temp/save.png"))
                if p=="suivant":
                    son_clap.play()
                    return p
                if p=="touche":
                    pygame.time.set_timer(INVINCIBLE,2000)
                    perso.invincible=True

            for a in niveau_actuel.dict_element.values():
                for i in a:
                    etat=i.update(perso,duree_frame,niveau_actuel)


            temps_actuel=pygame.time.get_ticks()
            for i,t_forme in enumerate(liste_t_forme):
                d_ecoulee=temps_actuel-t_forme
                liste_cooldown[i]=liste_base_cooldown[i]-d_ecoulee
                if liste_cooldown[i]<=0:liste_cooldown[i]=liste_base_cooldown[i]
            liste_texte_cooldown=[p_perfect.render(str(round(i/1000,1)),1,NOIR) for i in liste_cooldown]

            for i in niveau_actuel.dict_element["bloc_tuto"]:
                if perso.tuto==True and i.toucher==False: #Collision avec bloc tuto
                    a_e=etat_jeu
                    etat_jeu=2


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
        pygame.draw.rect(fenetre,VERT,(2,2,150*perso.pv,26))
        pygame.draw.rect(fenetre,NOIR,(2,2,150*perso.pv,26),2)
        pygame.draw.rect(fenetre,BLEU,(2,30,20*perso.energie,26))
        pygame.draw.rect(fenetre,NOIR,(2,30,20*perso.energie,26),2)
        for i,forme in enumerate(liste_img_formes):
            if i<niveau_actuel.numero:
                fenetre.blit(forme,(618+i*50,2))
                if liste_cooldown[i]!=liste_base_cooldown[i]:
                    fenetre.blit(filtre_cooldown,(618+i*50,2))
                    fenetre.blit(liste_texte_cooldown[i],(618+i*50,2))
        fenetre.blit(img_menu,(400,2))
        fenetre.blit(img_reset,(450,2))
        fenetre.blit(img_info,(500,2))

        if etat_jeu==2:
            fenetre.blit(pause_tuto,(0,0))
            fenetre.blit(img_retour,(550,2))
            for i,texte in enumerate(niveau_actuel.texte_astuce):
                fenetre.blit(texte,(200,200+20*i))

            if niveau_actuel.numero==1:
                longueur=len(anim_tuto["trait"])
                fenetre.blit(anim_tuto["trait"][animation],(200,120))
            elif niveau_actuel.numero==2:
                longueur=len(anim_tuto["point"])
                fenetre.blit(anim_tuto["point"][animation],(200,120))
            elif niveau_actuel.numero==3:
                longueur=len(anim_tuto["cercle"])
                fenetre.blit(anim_tuto["cercle"][animation],(200,120))
            elif niveau_actuel.numero==4:
                longueur=len(anim_tuto["TP"])
                fenetre.blit(anim_tuto["TP"][animation],(200,120))
            elif niveau_actuel.numero==5:
                longueur=len(anim_tuto["angle droite"])
                fenetre.blit(anim_tuto["angle haut"][animation],(200,120))
                fenetre.blit(anim_tuto["angle droite"][animation],(300,120))
            elif niveau_actuel.numero==6:
                longueur=len(anim_tuto["eclair"])
                fenetre.blit(anim_tuto["eclair"][animation],((200,100)))
            elif niveau_actuel.numero==7:
                longueur=len(anim_tuto["ellipse"])
                fenetre.blit(anim_tuto["ellipse"][animation],((200,120)))

        pygame.display.flip()
    #----------------------------Gestion du temps-----------------------------
        timer.tick(30)
        fps=timer.get_fps()
        if fps!=0:
            duree_frame=1/fps
        else:
            duree_frame=0



def game_over(fond):

    rect_gameover=texte_gameover.get_rect()
    rect_reessayer=texte_reessayer.get_rect()
    rect_menu=texte_menu.get_rect()
    rect_suivant=texte_suivant.get_rect()

    rect_reessayer.centerx=rect_menu.centerx=rect_suivant.centerx=rect_gameover.centerx=fenetre_x/2

    rect_gameover.centery=fenetre_y/8
    rect_reessayer.centery=3*fenetre_y/8
    rect_menu.centery=fenetre_y/2
    rect_suivant.centery=5*fenetre_y/8


    continuer=True
    while continuer:
        for event in pygame.event.get():
            if event.type==QUIT:
                return "fin"
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                if rect_menu.collidepoint(event.pos):
                    musique("Sons/fond_menu.wav")
                    return "menu"
                elif rect_reessayer.collidepoint(event.pos):
                    musique("Sons/music_jeu.wav")
                    return "reset"
                elif rect_suivant.collidepoint(event.pos):
                    musique("Sons/music_jeu.wav")
                    return "suivant"


        fenetre.blit(fond,(0,0))
        fenetre.blit(fond_pause,(0,0))
        fenetre.blit(texte_menu,rect_menu)
        fenetre.blit(texte_gameover,rect_gameover)
        fenetre.blit(texte_suivant,rect_suivant)
        fenetre.blit(texte_reessayer,rect_reessayer)
        pygame.display.flip()


def victoire(fond):
    pygame.mixer.music.stop()
    son_victory.play()
    rect_vctr=vctr.get_rect()
    rect_congrats=congrats.get_rect()
    rect_txt_vctr=txt_vctr.get_rect()
    rect_menu=menu_vctr.get_rect()

    rect_vctr.centerx=rect_congrats.centerx=rect_txt_vctr.centerx=rect_menu.centerx=fenetre_x/2
    rect_vctr.centery=fenetre_y/4
    rect_congrats.centery=(fenetre_y/2)-25
    rect_txt_vctr.centery=(fenetre_y/2)+25
    rect_menu.centery=3*fenetre_y/4


    continuer=True
    while continuer:
        for event in pygame.event.get():
            if event.type==QUIT:

                return "fin"
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                if rect_menu.collidepoint(event.pos):
                    musique("Sons/fond_menu.wav")
                    return "menu"

        fenetre.blit(fond,(0,0))
        fenetre.blit(fond_vctr,(0,0))
        fenetre.blit(menu_vctr,rect_menu)
        fenetre.blit(vctr,rect_vctr)
        fenetre.blit(congrats,rect_congrats)
        fenetre.blit(txt_vctr,rect_txt_vctr)
        pygame.display.flip()


def musique(music):
    pygame.mixer.stop()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()


    return True


