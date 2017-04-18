import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *
from fonctions import *


#----------------------------Classes---------------------------------------
class Niveau():
    liste=[]
    """
        Attributs:  theme :     Numero du theme
                    fichier:    Nom du fichier
                    structure:  Liste de liste
                    dict_image: Images


        Méthodes:   creation()
                    update()

    """

    def __init__(self,n,c_fichier,images,theme):

        self.numero=n
        self.theme=theme    #Numero du theme
        self.fichier=c_fichier

        self.structure=[]
        self.dict_element={ "bloc":[],
                            "fin":None,
                            "tp":[],
                            "torche":[],
                            "porte":[],
                            "goomba":[],
                            "bulle":[],
                            "boule feu":[],
                            "interrupteur":[]
                            }

        self.liste_ombre=[]
        self.vent=False,None
        self.noir=False
        self.eclair=False

        self.dict_images=images
        self.creation()
        Niveau.liste.append(self)

    def creation(self):

        with open(self.fichier,'r') as fichier:
            grille=fichier.readlines()
            for ligne in grille:
                if ligne[-1]=='\n':
                    self.structure.append(ligne[:-1])
                else:
                    self.structure.append(ligne)


        for y,ligne in enumerate(self.structure):
            for x,car in enumerate(ligne):

                if car=='1':
                    r=Bloc(self.dict_images["bloc"],(x*bloc_x , y*bloc_y))
                    self.dict_element["bloc"].append(r)

                elif car=='2':
                    f=Fin(self.dict_images["porte"],(x*bloc_x , y*bloc_y))
                    self.dict_element["fin"]=f

                elif car=='3':
                    t=Teleport(self.dict_images["tp"],(x*bloc_x , y*bloc_y))
                    self.dict_element["tp"].append(t)

                elif car=='4':
                    t=Torche(self.dict_images["torche"],(x*bloc_x , y*bloc_y))
                    self.dict_element["torche"].append(t)

                elif car=='5':
                    p=Porte(self.dict_images["portail"],(x*bloc_x , y*bloc_y))
                    self.dict_element["porte"].append(p)

                elif car=='6':
                    go=Goomba(self.dict_images["goomba"],(x*bloc_x , y*bloc_y))
                    self.dict_element["goomba"].append(go)
                
                elif car=='7':
                    i= Interrupteur(self.dict_images["interrupteur"],(x*bloc_x,y*bloc_y))
                    self.dict_element["interrupteur"].append(i)

                elif car=="n":
                    self.noir=True

    def update(self,perso):
        #Ombre
        self.liste_ombre=[]
        if self.noir==True:
            for y in range(0,fenetre_y,self.dict_images["ombre"].get_height()):
                for x in range(0,fenetre_x,self.dict_images["ombre"].get_width()):
                    self.liste_ombre.append((x,y))
            if self.eclair==True:
                self.liste_ombre=[]



        #Vent
        liste_obj_vent=[]
        for i in self.dict_element["goomba"]:
            liste_obj_vent.append(i)
        liste_obj_vent.append(perso)

        if self.vent[0]==True:

            for i in liste_obj_vent:

                if self.vent[1]=="droite":
                    i.acceleration_x=15
                elif self.vent[1]=="gauche":
                    i.acceleration_x=-15
        else:
            for i in liste_obj_vent:
                i.acceleration_x=0

class Personnage():

    def __init__(self,pos,dict_img):

        self.dict_img=dict_img
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


    def update(self,d_frame,niveau_actuel):

        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)

        #Mouvement

        self.ancien=self.rect

        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)

        self.saut=True #Le perso est en saut dans tous les cas sauf cas il touche le sol


        #Restraindre position dans la fenetre
        if self.rect.bottom>=fenetre_y:
            print("T'es mort!!!!!!!!!!!!!!!!!!!")
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
            if self.rect.bottom>=rect.top and self.ancien.bottom<=rect.top:
                self.rect.bottom=rect.top
                self.vitesse_y=0
            elif self.rect.top<=rect.bottom and self.ancien.top>=rect.bottom:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.rect.right>=rect.left and self.ancien.right<=rect.left:
                self.rect.right=rect.left
            elif self.rect.left<=rect.right and self.ancien.left>=rect.right:
                self.rect.left=rect.right

        for rect in liste_rect:
            if (self.rect.bottom==rect.top) and ((self.rect.left>rect.left and self.rect.left<rect.right) or (self.rect.right>rect.left and self.rect.right<rect.right)):
                self.saut=False
                self.double_saut=False


        #Animation

        if self.deplacement==True:
            self.img=self.dict_img[self.direction]["cours"][self.animation]
        if self.saut==True:
            self.img=self.dict_img[self.direction]["saute"]
        if self.deplacement==False and self.saut==False:
            self.img=self.dict_img[self.direction]["debout"]

        #Verification victoire
        if self.rect.collidelist(niveau_actuel.dict_element["goomba"])!=-1:
            print("LOLOLOL! T'es mort!")
        if self.rect.colliderect(niveau_actuel.dict_element["fin"].rect):
            return "win"

class Bloc():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos


class Fin():
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos

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

    def update(self,d_frame,niveau_actuel):

        liste_rect=[]

        for i in niveau_actuel.dict_element["bloc"]:
            liste_rect.append(i.rect)

        for i in niveau_actuel.dict_element["porte"]:
            if i.ouvert==False:
                liste_rect.append(i.rect)


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

            if self.rect.bottom>=rect.top and self.ancien.bottom<=rect.top:
                self.rect.bottom=rect.top
                self.vitesse_y=0
            elif self.rect.top<=rect.bottom and self.ancien.top>=rect.bottom:
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.rect.right>=rect.left and self.ancien.right<=rect.left:
                self.rect.right=rect.left
                self.vitesse_x=-50
            elif self.rect.left<=rect.right and self.ancien.left>=rect.right:
                self.rect.left=rect.right
                self.vitesse_x=50

        #Animation
        self.img=self.liste_img[self.animation]



class Teleport():

    def __init__(self,liste_img,pos):
        self.etat=4
        self.liste_img=liste_img
        self.img=self.liste_img[self.etat]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos

    def update(self,perso):
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

    def update(self,d_frame,niveau_actuel):


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

    def update(self,niveau_actuel):
        if self.enflamme==True:
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

    def update(self):
        self.img=self.liste_img[self.animation]


class Bulle():
    liste=[]
    def __init__(self,img,obj):
        self.img=img
        self.obj=obj
        self.rect=self.img.get_rect()
        self.rect.center=self.obj.rect.center

    def update(self,niveau_actuel):

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
    liste= []
    def __init__(self, dict_image, pos):
        self.dict_image= dict_image
        self.img= dict_image["Ouvert"]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=True

        Interrupteur.liste.append(self)

    def update(self):
        if self.ouvert==False:
            self.img=self.dict_image["Ferme"]












