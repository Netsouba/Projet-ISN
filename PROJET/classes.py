﻿import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from init import *


#----------------------------Classes---------------------------------------
class Niveau():
    liste=[]

    def __init__(self,n,images,theme,depart):

        self.numero=n
        self.theme=theme    #Numero du theme
        self.fichier="Niveaux//"+str(self.numero+1)+".txt"
        self.dict_images=images

        self.depart=depart
        self.creation()

        Niveau.liste.append(self)

    def creation(self):

        self.dict_images["ombre"].set_alpha(240)
        self.noir=False
        self.eclair=False
        self.ralenti=False
        self.liste_ombre=[]
        self.structure=[]
        self.astuce=[]
        self.dict_element={ "bloc":[],
                            "fin":[],
                            "tp":[],
                            "torche":[],
                            "porte":[],
                            "goomba":[],
                            "koopa":[],
                            "bulle":[],
                            "boule feu":[],
                            "interrupteur":[],
                            "porte interrupteur":[],
                            "bouton":[],
                            "porte bouton":[],
                            "pic":[],
                            "pot":[],
                            "coeur":[],
                            "caisse":[]
                            }

        with open(self.fichier,'r') as fichier:
            grille=fichier.readlines()
            for ligne in grille:
                if ligne[-1]=='\n':
                    self.structure.append(ligne[:-1])
                else:
                    self.structure.append(ligne)


        for y,ligne in enumerate(self.structure):
            if y<=17:
                for x,car in enumerate(ligne):
                    if car!=" ":
                        try:
                            int(car)
                            chiffre=True
                        except ValueError:
                            chiffre=False


                        if chiffre:
                            if car=='1':
                                r=Bloc(self.dict_images["bloc"],(x*bloc_x , y*bloc_y))
                                self.dict_element["bloc"].append(r)

                            elif car=='2':
                                f=Fin(self.dict_images["fin"],(x*bloc_x , y*bloc_y))
                                self.dict_element["fin"].append(f)

                            elif car=='3':
                                t=Teleport(self.dict_images["tp"],(x*bloc_x , y*bloc_y))
                                self.dict_element["tp"].append(t)

                            elif car=='4':
                                t=Torche(self.dict_images["torche"],(x*bloc_x , y*bloc_y))
                                self.dict_element["torche"].append(t)

                            elif car=='5':
                                p=Porte(self.dict_images["porte"],(x*bloc_x , y*bloc_y))
                                self.dict_element["porte"].append(p)

                            elif car=='6':
                                go=Goomba(self.dict_images["goomba"],(x*bloc_x , y*bloc_y))
                                self.dict_element["goomba"].append(go)

                            elif car=="7":
                                b=Bouton(self.dict_images["bouton"],(x*bloc_x , y*bloc_y))
                                self.dict_element['bouton'].append(b)
                            elif car=="8":
                                p=Porte_interrupeur(self.dict_images["porte bouton"],(x*bloc_x , y*bloc_y),car)
                                self.dict_element["porte bouton"].append(p)
                            elif car=="9":
                                p=Pic(self.dict_images["pic"],(x*bloc_x , y*bloc_y))
                                self.dict_element["pic"].append(p)

                        else:
                            if car=="p":
                                p=Pot(self.dict_images["pot"],(x*bloc_x+15 , y*bloc_y+15))
                                self.dict_element["pot"].append(p)
                            elif car=="c":
                                c=Coeur(self.dict_images["coeur"],(x*bloc_x+15, y*bloc_y+15))
                                self.dict_element["coeur"].append(c)
                            elif car=="k":
                                ko=Koopa(self.dict_images["koopa"],(x*bloc_x,y*bloc_y))
                                self.dict_element["koopa"].append(ko)
                            elif car=="x":
                                box=Caisse(self.dict_images["caisse"],(x*bloc_x,y*bloc_y))
                                self.dict_element["caisse"].append(box)


                            elif car=="n":
                                self.noir=True
                            elif car.lower()==car:
                                i= Interrupteur(self.dict_images["interrupteur"],(x*bloc_x,y*bloc_y),car)
                                self.dict_element["interrupteur"].append(i)
                            elif car.upper()==car:
                                p=Porte_interrupeur(self.dict_images["porte interrupteur"],(x*bloc_x , y*bloc_y),car)
                                self.dict_element["porte interrupteur"].append(p)


                for i in self.dict_element["interrupteur"]:
                    for indice,p in enumerate(self.dict_element["porte interrupteur"]):
                        if i.car==p.car:
                            i.liste_porte.append(indice)
            else:
                self.astuce.append(ligne)
        self.texte_astuce=[p_perfect.render(i,0,JAUNE) for i in self.astuce]

    def update(self,perso):
        #Ombre
        self.liste_ombre=[]
        if self.noir==True:
            for y in range(0,fenetre_y,self.dict_images["ombre"].get_height()):
                for x in range(0,fenetre_x,self.dict_images["ombre"].get_width()):
                    self.liste_ombre.append((x,y))

        if self.eclair==True:
            self.dict_images["ombre"].set_alpha(self.dict_images["ombre"].get_alpha()+10)
        if self.dict_images["ombre"].get_alpha()>=240:
            self.dict_images["ombre"].set_alpha(240)
            self.eclair=False



class Personnage():

    def __init__(self,pos,dict_img):

        self.dict_img=dict_img
        self.pv=5
        self.energie=15
        self.invincible=False
        self.img=dict_img["droite"]["debout"]
        self.rect=self.img.get_rect()
        self.ancien=self.rect
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.vitesse_x=0
        self.vitesse_y=0
        self.acceleration_x=0
        self.acceleration_y=g
        self.animation=0
        self.saut=True
        self.double_saut=False
        self.deplacement=False
        self.direction="droite"
        self.clignotant=False


    def update(self,d_frame,niveau_actuel):

        #Animation
        if self.invincible==True:
            self.clignotant=True
        else:
            self.clignotant=False
        if self.deplacement==True:
            self.img=self.dict_img[self.direction]["cours"][self.animation]
        if self.saut==True:
            self.img=self.dict_img[self.direction]["saute"]
        if self.deplacement==False and self.saut==False:
            self.img=self.dict_img[self.direction]["debout"]

        #Liste des elements de collision
        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["porte bouton"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["bouton"]:
            liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["caisse"]:
            if i.hold==False:
                liste_rect.append(i.rect)


        #Mouvement

        self.ancien=self.rect

        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)

        self.saut=True #Le perso est en saut dans tous les cas sauf cas il touche le sol


        #Restraindre position dans la fenetre
        if self.rect.top>=fenetre_y:
            return "mort"
        elif self.rect.top<0:
            self.rect.top=0
            self.vitesse_y=0
        if self.rect.right>=fenetre_x:
            self.rect.right=fenetre_x
            self.vitesse_x=0
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=0

        #Collision
        i_collision=self.rect.collidelistall(liste_rect)
        for rect in [liste_rect[i] for i in i_collision]:
            if self.ancien.bottom<=rect.top<=self.rect.bottom:
                self.rect.bottom=rect.top
                self.vitesse_y=0
            elif self.rect.top<=rect.bottom<=self.ancien.top:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.ancien.right<=rect.left<=self.rect.right:
                self.rect.right=rect.left


            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right



        for rect in liste_rect:
            if (self.rect.bottom==rect.top) and (rect.left<self.rect.left<rect.right or rect.left<self.rect.right<rect.right):
                self.saut=False
                self.double_saut=False





        #Verification victoire
        if self.rect.collidelist(niveau_actuel.dict_element["goomba"])!=-1 and self.invincible==False:
                self.pv-=3
                return "touche"
        if self.rect.collidelist(niveau_actuel.dict_element["koopa"])!=-1 and self.invincible==False:
            return "mort"
        if self.rect.collidelist(niveau_actuel.dict_element["pic"])!=-1 and self.invincible==False:
            return "mort"

        i=self.rect.collidelist(niveau_actuel.dict_element["pot"])
        if i!=-1 and self.energie<15:
            if self.energie<=10:    self.energie+=5
            else:                   self.energie=15
            niveau_actuel.dict_element["pot"].pop(i)

        i=self.rect.collidelist(niveau_actuel.dict_element["coeur"])
        if i!=-1 and self.pv<5:
            if self.pv<=3:    self.pv+=2
            else:                   self.pv=5
            niveau_actuel.dict_element["coeur"].pop(i)

        if self.rect.colliderect(niveau_actuel.dict_element["fin"][0].rect):
            return "suivant"
        if self.pv==0:
            return "mort"

class Goomba():
    def __init__(self,liste_img,pos):
        self.liste_img=liste_img
        self.img=self.liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ancien=self.rect
        self.vitesse_x=-50
        self.vitesse_y=0
        self.acceleration_x=0
        self.acceleration_y=g
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):

    #Liste des elements de collision
        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte bouton"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["bouton"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["caisse"]:
            liste_rect.append(i.rect)

        #Mouvement
        self.ancien=self.rect
        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)



        #Restraindre position dans la fenetre
        if self.rect.top>fenetre_y:
            niveau_actuel.dict_element["goomba"].remove(self)
            del self
            return 0
        if self.rect.top<0:
            self.rect.top=0
            self.vitesse_y=0
        if self.rect.right>=fenetre_x:
            self.rect.right=fenetre_x
            self.vitesse_x=-50
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=50


        #Collision
        i_collision=self.rect.collidelistall(liste_rect)
        for rect in [liste_rect[i] for i in i_collision]:

            if self.ancien.bottom<=rect.top<=self.rect.bottom:
                self.rect.bottom=rect.top
                self.vitesse_y=0
            elif self.rect.top<=rect.bottom<=self.ancien.top:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.ancien.right<=rect.left<=self.rect.right:
                self.rect.right=rect.left
                self.vitesse_x=-50

            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right
                self.vitesse_x=50


        #Animation
        self.img=self.liste_img[self.animation]

class Koopa():

    def __init__(self, liste_img, pos):
        self.liste_img=liste_img
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ancien=self.rect
        self.vitesse_x=-500
        self.vitesse_y=0
        self.acceleration_x=0
        self.acceleration_y=g
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):

    #Liste des elements de collision
        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)
        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte bouton"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["bouton"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["caisse"]:
            liste_rect.append(i.rect)

        #Mouvement
        self.ancien=self.rect
        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)



        #Restraindre position dans la fenetre
        if self.rect.top>fenetre_y:
            niveau_actuel.dict_element["koopa"].remove(self)
            del self
            return 0
        if self.rect.top<0:
            self.rect.top=0
            self.vitesse_y=0
        if self.rect.right>=fenetre_x:
            self.rect.right=fenetre_x
            self.vitesse_x=-500
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=500


        #Collision
        i_collision=self.rect.collidelistall(liste_rect)
        for rect in [liste_rect[i] for i in i_collision]:

            if self.ancien.bottom<=rect.top<=self.rect.bottom:
                self.rect.bottom=rect.top
                self.vitesse_y=0
            elif self.rect.top<=rect.bottom<=self.ancien.top:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.ancien.right<=rect.left<=self.rect.right:
                self.rect.right=rect.left
                self.vitesse_x=-500

            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right
                self.vitesse_x=500


        #Animation
        self.img=self.liste_img[self.animation]


class Bloc():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass

class Pot():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass

class Coeur():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass

class Pic():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass

class Bouton():
    def __init__(self,liste_img,pos):
        self.liste_img=liste_img
        self.img=self.liste_img[1]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.appuye=False

    def update(self,perso,d_frame,niveau_actuel):
        liste_collision=[]
        liste_collision.append(perso.rect)
        for i in niveau_actuel.dict_element["goomba"]:
            liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["koopa"]:
            liste_collision.append(i.rect)

        self.appuye=False
        for rect in liste_collision:
            if rect.bottom==self.rect.top and self.rect.left<rect.centerx<self.rect.right:
                self.appuye=True


        if False not in [i.appuye for i in niveau_actuel.dict_element["bouton"]]:
            for i in niveau_actuel.dict_element["porte bouton"]:
                i.ouvert=True
        else:
            for i in niveau_actuel.dict_element["porte bouton"]:
                i.ouvert=False

        if self.appuye: self.img=self.liste_img[0]
        else:           self.img=self.liste_img[1]

class PorteBouton():

    def __init__(self,liste_img,pos):
        self.liste_img=liste_img
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation]

class Fin():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass






class Teleport():

    def __init__(self,liste_img,pos):
        self.etat=4
        self.liste_img=liste_img
        self.img=self.liste_img[self.etat]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos

    def update(self,perso,d_frame,niveau_actuel):
        #Changement couleur
        d=distance(perso.rect.center,self.rect.center)

        if d<100:       self.etat=0
        elif d<200:     self.etat=1
        elif d<300:     self.etat=2
        elif d<400:     self.etat=3
        else:           self.etat=4

        self.img=self.liste_img[self.etat]

class BouleFeu():

    def __init__(self,dict_img,direction,perso):

        self.dict_img=dict_img
        self.direction=direction
        self.img=self.dict_img[self.direction][0]

        self.rect=self.img.get_rect()
        self.rect.center=perso.rect.center
        self.acceleration_x=0
        self.acceleration_y=0

        if self.direction=="droite":
            self.vitesse_x=200
            self.vitesse_y=0
        elif self.direction=="gauche":
            self.vitesse_x=-200
            self.vitesse_y=0
        elif self.direction=="haut":
            self.vitesse_x=0
            self.vitesse_y=-6
        elif self.direction=="bas":
            self.vitesse_x=0
            self.vitesse_y=6


        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):


        #Mouvement

        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y
        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)


        #Animation
        self.img=self.dict_img[self.direction][self.animation]

        #Restraindre position dans la fenetre
        if self.rect.left>fenetre_x or self.rect.bottom<0 or self.rect.right<0 or self.rect.top>fenetre_y:
            niveau_actuel.dict_element["boule feu"].remove(self)
            del self
            return 0

        #Collision

        liste_collision=[]  #Liste des objets ou la boule s'arrete sans effets
        for i in niveau_actuel.dict_element["bloc"]:
            liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["caisse"]:
            liste_collision.append(i.rect)

        i_collision_torche=self.rect.collidelist(niveau_actuel.dict_element["torche"])
        i_collision_goomba=self.rect.collidelist(niveau_actuel.dict_element["goomba"])

        if i_collision_torche!=-1 and niveau_actuel.dict_element["torche"][i_collision_torche].enflamme==False:
            niveau_actuel.dict_element["torche"][i_collision_torche].enflamme=True
            niveau_actuel.dict_element["boule feu"].remove(self)
            del self
            return 0

        elif self.rect.collidelist(liste_collision)!=-1:
            niveau_actuel.dict_element["boule feu"].remove(self)
            del self
            return 0

        elif i_collision_goomba!=-1:
            niveau_actuel.dict_element["goomba"].pop(i_collision_goomba)
            niveau_actuel.dict_element["boule feu"].remove(self)
            del self
            return 0


        #Eclairage
        l=[]
        for o in niveau_actuel.liste_ombre:
            if distance(self.rect.topleft,o)<=100:
                l.append(o)
        for o in l:
            niveau_actuel.liste_ombre.remove(o)

class Torche():

    def __init__(self,dict_img,pos):

        self.dict_img=dict_img
        self.img=dict_img["Arret"]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.enflamme=False
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        if self.enflamme==True:
            #Animation
            self.img=self.dict_img["Flamme"][self.animation]

            #Eclairage
            l=[]
            for o in niveau_actuel.liste_ombre:
                if distance(self.rect.topleft,o)<=100:
                    l.append(o)
            for i in l:
                niveau_actuel.liste_ombre.remove(i)
        else:
            self.img=self.dict_img["Arret"]


class Porte():

    def __init__(self,liste_img,pos):
        self.liste_img=liste_img
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation]


class Bulle():
    liste=[]
    def __init__(self,img,obj):
        self.img=img
        self.obj=obj
        self.rect=self.img.get_rect()
        self.rect.center=self.obj.rect.center

    def update(self,perso,d_frame,niveau_actuel):

        self.rect.center=self.obj.rect.center
        self.obj.acceleration_y=-g/2
        t=type(self.obj)
        if t!=Personnage:
            if t==Goomba:

                if self.obj not in niveau_actuel.dict_element["goomba"]:
                    niveau_actuel.dict_element["bulle"].remove(self)
                    del self
                    return 0

class Interrupteur():
    def __init__(self, dict_image, pos,car):
        self.car=car
        self.dict_image= dict_image
        self.img= dict_image["Ouvert"]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=True
        self.liste_porte=[]

    def update(self,perso,d_frame,niveau_actuel):
        if self.ouvert==False:
            self.img=self.dict_image["Ferme"]
            for i,porte in enumerate(niveau_actuel.dict_element["porte interrupteur"]):
                if i in self.liste_porte:
                    porte.ouvert=True

        else:
            self.img=self.dict_image["Ouvert"]
            for i,porte in enumerate(niveau_actuel.dict_element["porte interrupteur"]):
                if i in self.liste_porte:
                    porte.ouvert=False

class Porte_interrupeur():

    def __init__(self,liste_img,pos,car):
        self.car=car.lower()
        self.liste_img=liste_img
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation]

class Caisse():
    def __init__(self,img,pos,):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ancien=self.rect
        self.vitesse_x=0
        self.vitesse_y=0
        self.acceleration_x=0
        self.acceleration_y=g
        self.hold=False

    def update(self, perso, d_frame, niveau_actuel):
        #Liste des elements de collision
        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte bouton"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["bouton"]:
            liste_rect.append(i.rect)


        #Mouvement
        self.ancien=self.rect
        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)



        #Restraindre position dans la fenetre
        if self.rect.top>fenetre_y:
            niveau_actuel.dict_element["caisse"].remove(self)
            del self
            return 0
        if self.rect.top<0:
            self.rect.top=0
            self.vitesse_y=0
        if self.rect.right>=fenetre_x:
            self.rect.right=fenetre_x
            self.vitesse_x=-0
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=0


        #Collision


        i_collision=self.rect.collidelistall(liste_rect)

        for rect in [liste_rect[i] for i in i_collision]:

            if self.ancien.bottom<=rect.top<=self.rect.bottom:
                self.rect.bottom=rect.top
                self.vitesse_y=0

            elif self.rect.top<=rect.bottom<=self.ancien.top:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.ancien.right<=rect.left<=self.rect.right:
                self.rect.right=rect.left
                self.vitesse_x=-0



            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right
                self.vitesse_x=0


        if self.hold==True:
            self.vitesse_x=perso.vitesse_x

        elif self.hold==False:
            self.vitesse_x=0









