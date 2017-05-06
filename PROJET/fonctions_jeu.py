import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from classes import *
from init import *

#Ces fonctions sont appellées dans main.py où la gestion de ce qui est retourné est expliquée

def accueil():
    """L'écran d'accueil. La fonction retourne None si l'utilisateur quitte le jeu ou "continuer" s'il appuie sur une touche
    """
    musique("Sons/fond_menu.wav")                           #On lance la musique de l'accueil

    titre_rect=titre.get_rect()                             #On crée les rectangles correspondant à leur texte                                   
    titre_2_rect=titre_2.get_rect()         
    titre_rect.center=fenetre_x/2,fenetre_y/4               #On les place sur des emplacements qui dépendent de la taille de la fenetre
    titre_2_rect.center=fenetre_x/2,4*fenetre_y/5
    
    visible=True                                            #Cette variable est True quand le texte "Appuyez sur une touche pour continuer" est visible et False quand elle ne l'est pas pour créer un clignotement
    
    pygame.time.set_timer(ANIMER,500)                       #On va appeller l'évenement ANIMER toutes les 0.5 secondes qui va servir à faire clignoter le texte



    while True:                                             #Comme pour tous les programmes pygame, on crée un boucle infinie
        
        for event in pygame.event.get():                    #On capture tous les évenements que l'ordinateur va intercepter en tant que la variable event
            if event.type==QUIT:    return None             #Si l'évenement est un ordre de quitter le jeu (comme cliquer sur la croix rouge), retourne None
            if event.type==KEYDOWN or event.type==MOUSEBUTTONDOWN:  return "continuer"  #Si l'utilisateur appuie sur une touche ou sur sa souris, retourne "continuer"
            if event.type==ANIMER: visible=not visible      #Si l'évenement appelé est ANIMER, on inverse le booléen visible.
                
        #---------------------------------Affichage-------------------------------------------
        
        fenetre.blit(fond_ecran,(0,0))                      #On affiche le fond d'écran
        fenetre.blit(titre,titre_rect)                      #On affiche le titre du jeu
        if visible:fenetre.blit(titre_2,titre_2_rect)       #Si le texte doit être visible, on l'affiche    
        pygame.display.flip()                               #On met à jour l'affichage de l'écran


def menu():                             
    """ L'écran du choix du niveau. La fonction retourne None si le joueur quitte le jeu ou le numéro du niveau qu’il a sélectionné
    """

    titre_menu_rect=titre_menu.get_rect()                   #On crée les rectangles correspondant à leur texte  
    titre_menu_rect.center=fenetre_x/2,fenetre_y/4          #On le place sur l'écran
    
    nombres_rect=[i.get_rect() for i in nombres]            #On met dans la liste les rectangles correspondant aux textes des nombres



    rect_fleche_droite=img_fleche_droite.get_rect()         #On crée les rectangles correspondant à leur image
    rect_fleche_gauche=img_fleche_gauche.get_rect()
    
    rect_fleche_droite.centery=rect_fleche_gauche.centery=9*fenetre_y/10    #On les place sur l'écran
    rect_fleche_droite.centerx=7*fenetre_x/8
    rect_fleche_gauche.centerx=fenetre_x/8

    liste_boite_rect=[]                                     #On crée les rectangles correspondant aux images des boites
    
                                                            #On les place en fonction du numero grâce des boucles et on place également les rectangles des nombres
    for i in range(len(nombres)//4):
        nombres_rect[i].center=(i+1)*fenetre_x/7,fenetre_y/2    
        rect=img_boite.get_rect()
        rect.center=nombres_rect[i].center                  #On pose chaque boite au même centre que son numéro
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
    #Il y a donc 12 rectangles boites, et 24 rectangles numéro, car il y a 2 fenêtres          
        
    fenetre_actuelle=0                                      #0 si on est sur la première fenetre, 12 si on est sur la deuxième



    while True:                                                     #Boucle infinie

        for event in pygame.event.get():                    #On capture tous les évenements que l'ordinateur va intercepter en tant que la variable event
            if event.type==QUIT:    return None             #Si l'évenement est un ordre de quitter le jeu (comme cliquer sur la croix rouge), retourne None
            if event.type==MOUSEBUTTONDOWN:                 #Si l'utilisateur clique avec sa souris
                for i,rect in enumerate(liste_boite_rect):  #On parcours les rectangles boites avec leur numéro 
                    if rect.collidepoint(event.pos):        #Si il y a collision entre la position du curseur et une de ces boites    
                        return i+fenetre_actuelle           #On retourne le numéro de cette boite en additionnant 12 si on est sur la deuxième fenêtre

                if rect_fleche_droite.collidepoint(event.pos):  #Si on clique la flèche droite, on met la fenetre à 12
                    fenetre_actuelle=12
                elif rect_fleche_gauche.collidepoint(event.pos): #Si on clique la flèche gauche, on met la fenetre à 0
                    fenetre_actuelle=0

        #---------------------------------Affichage-------------------------------------------
        
        fenetre.blit(img_fond_menu,(0,0))                                               #On affiche le fond et le titre
        fenetre.blit(titre_menu,titre_menu_rect)
        
        for i in range(len(nombres)//2):                                                #On affiche 12 fois:
            fenetre.blit(img_boite,liste_boite_rect[i])                                 #Les boites
            fenetre.blit(nombres[i+fenetre_actuelle],nombres_rect[i+fenetre_actuelle])  #Les numéros selon la fenetre

        #Si on est sur la premiere fenetre, on affiche la flèche de droite, si on est sur la deuxième, on affiche la flèche de gauche.
        if fenetre_actuelle==0:
            fenetre.blit(img_fleche_droite,rect_fleche_droite)
        else:
            fenetre.blit(img_fleche_gauche,rect_fleche_gauche)
                
        pygame.display.flip()                                                           #On met à jour l'affichage de l'écran



def jeu(niveau_actuel):
    """La fonction prend en paramètre le niveau joué. 
    Il retourne “fin” si le joueur quitte le jeu, “menu” s’il appuie sur le bouton du menu, 
    “reset” s’il appuie sur le bouton “reset”, “suivant” quand la méthode perso.update() retourne “suivant”, 
    et ce que la fonction game_over() retourne quand la méthode perso.update() retourne “mort”.
    """
    
    #-----------------------------------------------------Variables diverses---------------------------------------

    niveau_actuel.creation()                                        #Réinitialisation du niveau
    perso=Personnage(niveau_actuel.depart,megaman_images)           #Recréation du personnage
    
    liste_pos=[]                                                    #Liste qui va contenir tous les points du dessin 
    
    #Pour les listes des formes qui suivent, l'ordre est :Trait,point,cercle,tp,angle,eclair,ellipse
    liste_t_forme=[0,0,0,0,0,0,0]                                   #Liste qui possède pour chaque pouvoir le temps à chauque fois que le pouvoir est utilisé
    liste_base_cooldown=[3000,2000,8000,1,5000,5000,10000]          #Liste qui gère le temps nécessaire à attendre entre chaque sort
    liste_cooldown=[0,0,0,0,0,0,0]                                  #Liste qui indique le temps restant avant que le sort soit réutilisable
    
    duree_frame=0                                                   #La durée d'une frame. Elle est actualisée à la fin de la boucle. Elle est égale à 0 pour la première frame pour éviter les erreurs de valeurs non définies.
    etat_jeu=0  #Variable qui change selon ce qui doit être affiché (0: jeu de plateforme  1:jeu de dessin     2:astuce)
    pygame.time.set_timer(ANIMER,100)                               #On va appeller l'évenement ANIMER toutes les 0.1 secondes qui va servir à animer les objets
    timer=pygame.time.Clock()                                       #On crée l'objet timer pour gérer le temps
    animation=0                                                     #Indique quel image de l'animation doit être affichée pour l'animation du tutoriel
    longueur=0                                                      #Indique la longeur de l'animation du tutoriel
    
    #Boucle infinie
    while True:

    #----------------------------Gestion des events---------------------------
        for event in pygame.event.get():

        for event in pygame.event.get():                        #On capture tous les évenements que l'ordinateur va intercepter en tant que la variable event
            if event.type==QUIT:    return "fin"                #Si l'évenement est un ordre de quitter le jeu (comme cliquer sur la croix rouge), retourne "fin"

            if event.type==KEYDOWN and event.key==K_SPACE:      #Si l'utilisateur appuis sur la barre espace. 
                for i in niveau_actuel.dict_element["caisse"]:  #On parcours la liste des caisses du niveau
                    if distance(perso.rect.center,i.rect.center)<=30:   #Si le personnage et la caisse sont suffisament proches
                        if i.hold==None:                        #Si la caisse n'était pas déjà tenue
                            if perso.rect.x<i.rect.x:           #Si le personnage est à gauche de la caisse
                                i.hold="gauche"
                            else:                               #Si le personnage est à droite de la caisse
                                i.hold="droite"
                        else:                                   #Si la caisse était déjà tenue
                            i.hold=None                         

            if event.type==KEYUP:                               #Si l'utilisateur enlève le doigt des touches:
                if event.key==K_RIGHT or event.key==K_LEFT:     #droite ou gauche
                    perso.vitesse_x=0                           #La vitesse du personnage redevient nulle
                    perso.deplacement=False                     #Le personnage n'est plus en déplacement

            if event.type==MOUSEBUTTONDOWN:                     #L'utilisateur appuie sur un bouton de la souris
                if event.button==3 and etat_jeu==0:             #S'il appuyé sur le clic droit et qu'il était dans le jeu de plateforme
                    etat_jeu=1                                  #On met l'interface de dessin
                    liste_pos=[]                                #On remet à 0 la liste des points du dessin précédent

                if event.button==1:                                         #Si l'utilisateur appuie sur le clic gauche
                    if pygame.Rect(400,2,40,40).collidepoint(event.pos):    #Si la position de sa souris collisione avec le rectangle du menu
                        musique("Sons/fond_menu.wav")                       #On met la musique du menu
                        return "menu"                                       #On retourne "menu"
                    if pygame.Rect(450,2,40,40).collidepoint(event.pos):    #Si la position de sa souris collisione avec le rectangle du reset
                        return "reset"                                      #On retourne "reset"
                    if pygame.Rect(500,2,40,40).collidepoint(event.pos):    #Si la position de sa souris collisione avec le rectangle du tutoriel
                        a_e=etat_jeu                                        #On enregistre dans a_e l'état précédent pour y revenir quand on quittera le tuto
                        etat_jeu=2                                          #On met l'interface du tutoriel
                    if pygame.Rect(550,2,40,40).collidepoint(event.pos) and etat_jeu==2:        #Si on appuie sur le rectangle retour du tutoriel et qu'on est dans le tutoriel
                        if niveau_actuel.dict_element["bloc_tuto"]!=[]:                         #S'il y a un bloc tutoriel dans le niveau
                            niveau_actuel.dict_element["bloc_tuto"][0].toucher=True             #On dit qu'on a touché ce bloc pour éviter de toujours lancer le tutoriel quand on le collisionne
                        etat_jeu=a_e                                                            #On remet l'état du jeu à l'état précédent


            if event.type==MOUSEBUTTONUP:                       #Si l'utilisateur lache un bouton de la souris
                if event.button==1 and etat_jeu==1:             #S'il lache le clic gauche et qu'il était dans l'interface de dessin
                    etat_jeu=0                                  #On remet l'interface du jeu 

                    #---------------------------------------------Reconnaissance--------------------------------------------------------
                    if liste_pos!=[]:                           #S'il y a bien au moins un point (ce qui est toujours le cas, sauf en cas de bug)
                        #On donne à b_(forme) les valeurs True ou False selon si les fonctions ont "reconnu" la forme, et eventuellement les valeurs nécessaires
                        i_tp=r_tp(liste_pos,perso.rect,[i.rect for i in niveau_actuel.dict_element["tp"]])
                        b_angle,pos_angle=r_angle(liste_pos)
                        b_arc=r_arc_cercle(liste_pos)
                        b_eclair=r_eclair(liste_pos)
                        b_cercle,(c_centre,c_rayon)=r_cercle(liste_pos)
                        b_point,pos_point=r_point(liste_pos)
                        b_trait,trait_l_point=r_droite(liste_pos)
                        b_ellipse,(e_centre,(e_a,e_b))=r_ellipse(liste_pos)
                        
                        #Toutes les pouvoirs ne se lancent que si le personnage a assez d'energie et que le sort n'est pas pendant le délai de récupération
                        
                        #--------------------------------Point-------------------------------
                        if b_point:                             #Si un point a été reconnu

                            if perso.double_saut==False and perso.rect.collidepoint(pos_point) and perso.energie>1 and liste_cooldown[1]==liste_base_cooldown[1]:   #Si le personnage peut faire un double saut, et si le point collision avec le rectangle du personnage
                                liste_t_forme[1]=pygame.time.get_ticks()        #On met à jour la liste_t_forme
                                perso.energie-=1                                #On fait perdre de l'énergie au personnage
                                perso.double_saut=True                          #Le personnage ne peut plus faire de double saut jusqu'a qu'il touche le sol
                                perso.vitesse_y=-6                              #On donne une vitesse de 6 pixels/frames vers le haut (saut)

                        #------------------------------Teleportation-------------------------

                        elif i_tp!=-1:                          #Si la téléportation est reconnue
                            tp=niveau_actuel.dict_element["tp"][i_tp]       #tp prend la valeur de l'objet Teleportation en question
                            if tp.etat!=4 and perso.energie>tp.etat and liste_cooldown[3]==liste_base_cooldown[3]:  #Si le bloc n'est pas marron
                                liste_t_forme[3]=pygame.time.get_ticks()
                                perso.energie-=3*tp.etat
                                perso.vitesse_y=0                           #On remet la vitesse y du personnage à 0
                                perso.rect.center=tp.rect.center            #On met le rectangle du personnage au niveau du rectangle téléportation (les centres au même endroit)

                        #--------------------------------Eclair----------------------------------------
                        elif b_eclair and perso.energie>3 and liste_cooldown[5]==liste_base_cooldown[5]:
                            liste_t_forme[5]=pygame.time.get_ticks()
                            perso.energie-=3    
                            son_electric.play()                                 #On joue l'effet sonore correspondant
                            niveau_actuel.dict_images["ombre"].set_alpha(0)     #Les ombres du niveau deviennent entièrement transparentes
                            niveau_actuel.eclair=True                           #On change l'attribut eclair du niveau
                            for i in niveau_actuel.dict_element["interrupteur"]:#On parcours les interrupteurs
                                for p in liste_pos:                             #On parcours les points du trait
                                    if i.rect.collidepoint(p):                  #Si le point collisionne avec l'interrupteur
                                        i.ouvert=not i.ouvert                   #L'attribut ouvert de l'interrupteur change
                                        break                                   #On quitte la boucle
                                for go in niveau_actuel.dict_element["goomba"]: #On parcours les objets "goomba" du niveau
                                for p in liste_pos:                             
                                    if go.rect.collidepoint(p):                 #Si le point collision avec le goomba
                                        niveau_actuel.dict_element["goomba"].remove(go)     #On l'enlève de sa liste
                                        break                                   #On quitte la boucle
                            for t in niveau_actuel.dict_element["torche"]:      #On parcours les torches du niveau
                                for p in liste_pos:
                                    if t.rect.collidepoint(p):                  #Si le point collision avec la torche 
                                        t.enflamme=True                         #L'attribut enflamme de la torche devient True


                        #----------------------------Cercle-----------------------------------------
                        elif b_cercle and perso.energie>2 and liste_cooldown[2]==liste_base_cooldown[2]:
                            liste_t_forme[2]=pygame.time.get_ticks()
                            perso.energie-=2
                            son_pop.play()
                            liste_obj_bulle=[]                                  #La liste prend tous les objets qui peuvent s'envoler grâce à la bulle
                            liste_obj_bulle.append(perso)                       #On met le personnage
                            for i in niveau_actuel.dict_element["goomba"]:      #On met tous les "goomba"
                                liste_obj_bulle.append(i)
                            for i in niveau_actuel.dict_element["caisse"]:      #On met toutes les caisses
                                liste_obj_bulle.append(i)

                            liste_obj_proche=[i for i in liste_obj_bulle if distance(i.rect.center,c_centre)<c_rayon]   #On met dans la liste_obj_proche tous les éléments qui sont dans la bulle en vérifiant si la distance entre l'objet et le centre du cercle est inférieur au rayon (maximum pour être indulgeant)
                            for i,elem in enumerate([distance(i.rect.center,c_centre) for i in liste_obj_proche]):      #On selectionne l'objet de cette liste qui est le plus proche du centre en faisant une liste distance
                                if elem==min([distance(i.rect.center,c_centre) for i in liste_obj_proche]):             
                                    obj=liste_obj_proche[i]
                            try :                                                                   
                                b=Bulle(img_bulle,obj)                          #On crée l'objet Bulle
                                niveau_actuel.dict_element["bulle"].append(b)   #On la rajoute dans la liste des éléments du niveau
                                del obj                                         #La suppression permet d'éviter les erreurs lors de la réutilisation de cette variable temporaire
                                pygame.time.set_timer(POP_BULLE,4000)           #On appelera l'évenement POP_BULLE dans 4 secondes pour la détruire
                            except NameError:                                   #S'il n'a pas d'obj :
                                pass                        


                        #-------------------------------------Ellipse-----------------------------------------
                        elif b_ellipse and perso.energie>2 and liste_cooldown[6]==liste_base_cooldown[6]:
                            liste_t_forme[6]=pygame.time.get_ticks()
                            perso.energie-=2
                            niveau_actuel.ralenti=0.1           #L'attribut ralenti du niveau devient 0.1 qui va ralentir les ennemis
                            pygame.time.set_timer(RALENTI,8000) #On appelera l'évenement RALENTI dans 8 secondes pour arreter le ralenti
                            pygame.time.set_timer(ANIMER,1000)  #Les animations deviennent plus lentes

                        #------------------------------------------Angle---------------------------------------------
                        elif b_angle!=False and perso.energie>3 and liste_cooldown[4]==liste_base_cooldown[4]:
                            liste_t_forme[4]=pygame.time.get_ticks()
                            perso.energie-=3
                            son_fire.play() 
                            boule_de_feu=BouleFeu(boule_de_feu_img,b_angle,perso)           #On crée la boule de feu
                            niveau_actuel.dict_element["boule feu"].append(boule_de_feu)    #On la rajoute dans la liste des éléments du niveau

                        #--------------------------------------Trait---------------------------------------
                        elif b_trait and perso.energie>1 and liste_cooldown[0]==liste_base_cooldown[0]:
                            liste_t_forme[0]=pygame.time.get_ticks()
                            perso.energie-=1
                            son_slash.play()

                            for point in trait_l_point:                                     #On parcours les points de la droite
                                                                                            #On va parcourir les éléments qui interragissent avec le trait
                                for porte in niveau_actuel.dict_element["porte"]:           
                                    if porte.rect.collidepoint(point):                      #S'il y a collision avec une porte
                                        porte.ouvert=True                                   #Son attribut ouvert devient True et la porte s'ouvre
                                for torche in niveau_actuel.dict_element["torche"]:         
                                    if torche.rect.collidepoint(point):                     #S'il y a collision avec une torche
                                        torche.enflamme=False                               #Son attribut enflamme devient True et il s'éteint
                                for bulle in niveau_actuel.dict_element["bulle"]:
                                    if bulle.rect.collidepoint(point):                      #S'il y a collision avec une bulle
                                        bulle.obj.acceleration_y=g                          #L'objet de la bulle est de nouveau accéléré vers le bas par la gravité
                                        bulle.obj.vitesse_y=0                               #Sa vitesse redevient nulle
                                        niveau_actuel.dict_element["bulle"].remove(bulle)   #On retire la bulle de la liste des éléments du niveau
                                        del bulle                                           #On supprimer la bulle
                                for goomba in niveau_actuel.dict_element["goomba"]:         
                                    if goomba.rect.collidepoint(point):                     #S'il y a collision avec un "goomba"
                                        niveau_actuel.dict_element["goomba"].remove(goomba) #On le retire de la liste des éléments du niveau
                                        del goomba                                          #On le supprime
    
                        b_point=b_ellipse=b_eclair=b_angle=b_trait=b_cercle=False           #On remet les valeurs par défaut pour éviter les bugs
                        i_tp=-1

            if event.type==ANIMER:                                                          #Si l'évenement ANIMER est appelé (toutes les 0.1 secondes en général)
    
                perso.animation+=1                                                          #L'image à afficher désignée par l'attribut animation change.
                if perso.animation>=4:                                                      #Si l'animation dépasse le nombre d'images, on remet à 0 pour faire ainsi une boucle
                    perso.animation=0

                for b in niveau_actuel.dict_element["boule feu"]:                           #On anime de la même manière tous les éléments du niveau qui possèdent une animation
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

                if etat_jeu==2:                                                             #Si on est dans le tutoriel:                    
                    animation+=1                                                            #On anime l'image grâce à la longueur définie plus tôt
                    if animation>=longueur:
                        animation=0



    
            if event.type==INVINCIBLE:                                                      #Si l'évenement INVINCIBLE est appelé pour la première fois (quelquees secondes après être touché)
                pygame.time.set_timer(INVINCIBLE,0)                                         #On arrete l'appel de l'évenement
                perso.invincible=False                                                      #L'attribut invincible du personnage redevient False

            if event.type==POP_BULLE:                                                       #Si l'évenement POP_BULLE est appelé pour la première fois (quelquees secondes après avoir créé la bulle)
                pygame.time.set_timer(POP_BULLE,0)                                          #On arrete l'appel de l'évenement
                if niveau_actuel.dict_element["bulle"]!=[]:                                 #S'il y a bien une bulle
                    bulle=niveau_actuel.dict_element["bulle"][0]                            #La seule bulle est désignée par la variable bulle
                    bulle.obj.acceleration_y=g                                              #L'objet dans la bulle redevient attiré par le bas
                    bulle.obj.vitesse_y=0                                                   #On remet sa vitesse y à 0
                    niveau_actuel.dict_element["bulle"].remove(bulle)                       #On retire la bulle de la liste des éléments du niveau
                    del bulle                                                               #Puis la supprime
        
            if event.type==RALENTI:                                                         #Si l'évenement RALENTI est appelé pour la première fois (quelquees secondes après avoir fait le pouvoir de ralentissement)
                pygame.time.set_timer(RALENTI,0)                                            #On arrete l'appel de l'évenement   
                pygame.time.set_timer(ANIMER,100)                                           #On remet la vitesse d'animation à 0.1 secondes
                niveau_actuel.ralenti=1                                                     #On remet l'attribut ralenti du niveau à 1

        #----------------------------Gestion du mouvement--------------------------
        touches=pygame.key.get_pressed()                                                    #C'est une liste de l'état de chaque touche du clavier
                                                                                            #L'avantage de cette technique est qu'on peut gérer plusieurs touches pressées en même temps
        if touches[K_RIGHT] and perso.deplacement==False:                                   #Si on appuie sur la flèche directionnelle droite pour la première fois
            perso.vitesse_x+=100                                                            #On ajoute une vitesse de 100 pixels par seconde
            perso.deplacement=True                                                          #On met déplacement True (notamment utile pour l'animation)
            perso.direction="droite"                                                        #On met direction à droite
    
        if touches[K_LEFT] and perso.deplacement==False:                                    #Même raisonnement que pour la droite
            perso.vitesse_x-=100                                                            #On soustrait maintenant la vitesse
            perso.deplacement=True
            perso.direction="gauche"

        if touches[K_UP] and perso.saut==False:                                             #Si on appuie sur la flèche directionnelle haut pour la première fois
            perso.vitesse_y=-6                                                              #On met une vitesse y de 6 pixels par frame vers le haut

        if etat_jeu==1:                                                                     #Si on est dans l'interface de dessin
            souris=pygame.mouse.get_pressed()                                               #C'est une liste de l'état des boutons de la souris. L'avantage est de pouvoir gérer plusieurs boutons pressés en même temps
            if souris[0]:                                                                   #Si le clic gauche est maintenu
                liste_pos.append(pygame.mouse.get_pos())                                    #On rajoute dans la liste_pos la position de la souris



    #---------------------------Gestion des variables--------------------------
        if etat_jeu==0:                                                                     #Si on est dans le jeu (ainsi, dans le tutoriel ou l'interface de dessin, les objets ne se mettent pas à jour, ce qui donne l'impression d'arreter le temps)
                                                                                            #On va mettre à jour tous les éléments grâce à la méthode update()
                                                                                            
            niveau_actuel.update(perso)                                                     #On met à jour le niveau 
            
            p=perso.update(duree_frame,niveau_actuel)                                       #On met à jour le personnage, et l'éventuel retour de la méthode est capturé dans une variable
            if p!=None:                                                                     #S'il ne c'est pas rien passé
                if p=="mort":                                                               #Si la méthode a retourné "mort" (la mort du personnage)
                    pygame.mixer.music.stop()                                               #On arrete la musique
                    son_game_over.play()                                                    #On joue l'effet sonore du Game Over
                    pygame.image.save(fenetre,"temp/save.png")                              #On fait une capture de l'écran actuel
                    return game_over(pygame.image.load("temp/save.png"))                    #On lance le game over en passant en paramètre l'image de cette capture d'écran
                if p=="suivant":                                                            #Si la méthode a retourné "suivant" (si le personnage arrive à la fin du niveau ou s'il passe le niveau)
                    son_clap.play()                                                         #On joue l'effet sonore de la victoire
                    return p                                                                #On retourne "suivant" vers le main.py
                if p=="touche":                                                             #Si la méthode a retourné "touche" (si le personnage a touché un ennemi basique)
                    pygame.time.set_timer(INVINCIBLE,2000)                                  #On appelle l'évenement INVINCIBLE toutes les 2 secondes (il ne sera appelé qu'une fois) pour éviter une collision avec les ennemis juste après avoir été touché
                    perso.invincible=True                                                   #L'attribut invicible du personnage devient True
    
            for a in niveau_actuel.dict_element.values():                                   #On fait un parcours des valeurs du dictionnaire 
                for i in a:                                                                 
                    i.update(perso,duree_frame,niveau_actuel)                               #On met à jour tous les éléments interractifs

            #---------------------Gestion du délai de récupération--------------------------------
            temps_actuel=pygame.time.get_ticks()                                    #On met le temps écoulé dans temps_actuel
            for i,t_forme in enumerate(liste_t_forme):                              #On travaille sur tous les pouvoirs avec un parcours de liste
                d_ecoulee=temps_actuel-t_forme                                      #On a le temps écoulé depuis le dernier lancement du sort
                liste_cooldown[i]=liste_base_cooldown[i]-d_ecoulee                  #On met à jour la liste qui indique le temps restant avant que le sort soit réutilisable
                if liste_cooldown[i]<=0:liste_cooldown[i]=liste_base_cooldown[i]    #Si ce temps atteint 0, on le remet au début
            liste_texte_cooldown=[p_perfect.render(str(round(i/1000,1)),1,NOIR) for i in liste_cooldown]        #On met à jour les textes qui indiquent le temps restant dans l'interface

            
            for i in niveau_actuel.dict_element["bloc_tuto"]:                       #On travaille sur tous les blocs tutoriels avec un parcours de liste
                if perso.tuto==True and i.toucher==False:                           #Si collision avec le bloc tuto pour la première fois     
                    a_e=etat_jeu                                                    #On sauvegarde l'ancien etat_jeu dans a_e
                    etat_jeu=2                                                      #On met l'interface du tutoriel


    #---------------------------Affichage-------------------------------------
        fenetre.blit(niveau_actuel.dict_images['fond'],(0,0))                       #Affichage du fond
        
        for a in niveau_actuel.dict_element.values():                               #Affichage de tous les éléments dans le dict_element du niveau avec un parcours des valeurs du dictionnaire
            for i in a:
                fenetre.blit(i.img,i.rect)                                          #On affiche l'image de l'objet à l'emplacement de son rectangle

        #-----------Personnage--------------
        if perso.clignotant==False or perso.animation%2==0:                         #Dans le cas où le personnage est clignotant(à cause de l'invicibilité), on ne l'affiche pas une image sur 2
            fenetre.blit(perso.img,perso.rect)

        for o in niveau_actuel.liste_ombre:                                         #On place les ombres
            fenetre.blit(niveau_actuel.dict_images["ombre"],o)
            
        if etat_jeu==1:                                                             #Si on est dans l'interface de dessin
            fenetre.blit(niveau_actuel.dict_images['pause'],(0,0))                  #On met le rectangle sombre
            for i in range(len(liste_pos)-1):                                       #On fait un parcours de la liste des points dessinés
                pygame.draw.line(fenetre,ROUGE,liste_pos[i+1],liste_pos[i],8)       #On dessine trait entre les points

        #-----------Interface-------------
        pygame.draw.rect(fenetre,VERT,(2,2,150*perso.pv,26))                        #Le rectangle vert des points de vie qui a une longueur qui dépend de la quantité de points de vie restants
        pygame.draw.rect(fenetre,NOIR,(2,2,150*perso.pv,26),2)                      #Le rectangle noir qui encadre ce dernier
        pygame.draw.rect(fenetre,BLEU,(2,30,20*perso.energie,26))                   #Le rectangle bleu de l'énergie qui a une longueur qui dépend de la quantité d'énergie restantes
        pygame.draw.rect(fenetre,NOIR,(2,30,20*perso.energie,26),2)                 #Le rectangle noir qui encadre ce dernier
        for i,forme in enumerate(liste_img_formes):                                 #On affiche les formes en haut à droite avec une boucle
            if i<niveau_actuel.numero:                                              #On affiche pas tous les pouvoirs dans les premiers niveaux.
                fenetre.blit(forme,(618+i*50,2))                                    
                if liste_cooldown[i]!=liste_base_cooldown[i]:                       #Si le sort est en rechargement:
                    fenetre.blit(filtre_cooldown,(618+i*50,2))                      #On affiche un petit rectangle sombre qui couvre l'image
                    fenetre.blit(liste_texte_cooldown[i],(618+i*50,2))              #On affiche les secondes qui restent
                    
        fenetre.blit(img_menu,(400,2))                                              #Affichage du bouton menu                 
        fenetre.blit(img_reset,(450,2))                                             #Affichage du bouton recommencer
        fenetre.blit(img_info,(500,2))                                              #Affichage du bouton tutoriel
        
        #---Tutoriel---
        if etat_jeu==2:                                                             #Si on est dans l'interface tutoriel
            fenetre.blit(pause_tuto,(0,0))                                          #Affichage du rectangle sombre
            fenetre.blit(img_retour,(550,2))                                        #Affichage de la flèche "retour au jeu"
            for i,texte in enumerate(niveau_actuel.texte_astuce):                   #Affichage du texte du tutoriel
                fenetre.blit(texte,(200,200+20*i))                                  

            #On rajoute les animations expliquant les formes à dessiner dans certains niveaux
            if niveau_actuel.numero==1:                             
                longueur=len(anim_tuto["trait"])                            #On met à jour la longueur
                fenetre.blit(anim_tuto["trait"][animation],(200,120))       #Puis on affiche l'image qui correspond à l'animation(qui change toutes les 0.1 secondes)
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

        pygame.display.flip()                                                       #Mise à jour de l'affichage de l'écran
    #----------------------------Gestion du temps-----------------------------
        timer.tick(30)                                                              #Le programme ne peut pas être tourné à plus de 30 frames par secondes pour économiser de la puissance
        fps=timer.get_fps()                                                         #On capture le nombre de frame par seconde
        if fps!=0:                                                                  #Le FPS est parfois égal à 0 lors de forts ralentissements
            duree_frame=1/fps                                                       #La durée d'une frame est notamment utile pour les déplacements
        else:
            duree_frame=0



def game_over(fond):
    """La fonction prend en paramètre une capture d’écran du jeu. 
        Ce qu’il retourne va être retourné par la fonction jeu(). 
        Il peut retourner “fin” si le joueur quitte le jeu, “menu” s’il appuie sur le bouton du menu, “reset” s’il appuie sur le bouton “réessayer”, “suivant” s’il appuie sur le bouton “niveau suivant”
    """
    
    #-------------------------Création et placement des rectangles des textes et images----------------------------------------------
    rect_gameover=texte_gameover.get_rect()                     
    rect_reessayer=texte_reessayer.get_rect()
    rect_menu=texte_menu.get_rect()
    rect_suivant=texte_suivant.get_rect()

    rect_reessayer.centerx=rect_menu.centerx=rect_suivant.centerx=rect_gameover.centerx=fenetre_x/2

    rect_gameover.centery=fenetre_y/8
    rect_reessayer.centery=3*fenetre_y/8
    rect_menu.centery=fenetre_y/2
    rect_suivant.centery=5*fenetre_y/8


    #Boucle infinie
    while True:
        
        for event in pygame.event.get():                    #On capture tous les évenements que l'ordinateur va intercepter en tant que la variable event
            if event.type==QUIT:    return "fin"             #Si l'évenement est un ordre de quitter le jeu (comme cliquer sur la croix rouge), retourne "fin"
            if event.type==MOUSEBUTTONDOWN and event.button==1: #Si l'utilisateur fait un clic gauche
                if rect_menu.collidepoint(event.pos):           #Si la position du curseur collisionne avec le rectangle "retour au menu"
                    musique("Sons/fond_menu.wav")               #On lance la musique du menu
                    return "menu"                               #On retourne "menu"
                elif rect_reessayer.collidepoint(event.pos):    #Si la position du curseur collisionne avec le rectangle "réessayer"
                    musique("Sons/music_jeu.wav")               #On relance la musique du jeu
                    return "reset"                              #On retourne "reset"
                elif rect_suivant.collidepoint(event.pos):      #Si la position du curseur collisionne avec le rectangle "niveau suivant"
                    musique("Sons/music_jeu.wav")               #On relance la musique du jeu
                    return "suivant"                            #On retourne "suivant"


        fenetre.blit(fond,(0,0))                            #Afficher le fond en arrière plan, qui est la capture d'écran
        fenetre.blit(fond_pause,(0,0))                      #Afficher un rectangle noir transparent pour assombrir l'écran
        fenetre.blit(texte_menu,rect_menu)                  #Affichier tous les textes
        fenetre.blit(texte_gameover,rect_gameover)
        fenetre.blit(texte_suivant,rect_suivant)
        fenetre.blit(texte_reessayer,rect_reessayer)      
        pygame.display.flip()                               #Mettre à jour l'affichage de l'écran


def victoire(fond):
    """La fonction prend en paramètre une capture d’écran du jeu. 
    Il peut retourner “fin” si le joueur quitte le jeu, “menu” s’il appuie sur le bouton du menu

    """
    pygame.mixer.music.stop()           #On arrete la musique du jeu
    son_victory.play()                  #On joue l'effet sonore correspondant
    
    rect_vctr=vctr.get_rect()           #Création et placement des rectangles textes
    rect_congrats=congrats.get_rect()
    rect_txt_vctr=txt_vctr.get_rect()
    rect_menu=menu_vctr.get_rect()

    rect_vctr.centerx=rect_congrats.centerx=rect_txt_vctr.centerx=rect_menu.centerx=fenetre_x/2
    rect_vctr.centery=fenetre_y/4
    rect_congrats.centery=(fenetre_y/2)-25
    rect_txt_vctr.centery=(fenetre_y/2)+25
    rect_menu.centery=3*fenetre_y/4

    #Boucle infinie
    while True:
        for event in pygame.event.get():                        #On capture tous les évenements que l'ordinateur va intercepter en tant que la variable event
            if event.type==QUIT:    return "fin"                #Si l'évenement est un ordre de quitter le jeu (comme cliquer sur la croix rouge), retourne "fin"

            if event.type==MOUSEBUTTONDOWN and event.button==1: #Si l'utilisateur fait un clic gauche
                if rect_menu.collidepoint(event.pos):           #Si la position du curseur collisionne avec le rectangle "retour au menu"
                    musique("Sons/fond_menu.wav")               #On lance la musique du menu
                    return "menu"                               #On retourne menu
        
        fenetre.blit(fond,(0,0))                                #Afficher le fond en arrière plan, qui est la capture d'écran
        fenetre.blit(fond_vctr,(0,0))                           #Afficher un rectangle noir transparent pour assombrir l'écran
        fenetre.blit(menu_vctr,rect_menu)                       #Afficher tous les textes
        fenetre.blit(vctr,rect_vctr)
        fenetre.blit(congrats,rect_congrats)
        fenetre.blit(txt_vctr,rect_txt_vctr)
        pygame.display.flip()                                   #Mise à jour de affichage de l'écan



