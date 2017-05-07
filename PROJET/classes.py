import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *
from fonctions import *
from init import *


#----------------------------Classes---------------------------------------
class Niveau():
    """L'objet niveau est l'environnement dans lequel évolue le personnage. Il possède par exemple tous les éléments interactifs.
    """
    liste=[]                                                                                #La classe possède une liste qui possède tous les niveaux.

    def __init__(self,n,images,depart): 
        """Cette méthode est automatiquement appelée quand on défini un objet Niveau
        La création du niveau prend 3 paramètres : son numéro, son dictionnaire d'image (crée dans init.py) et la position de départ du personnage
        """

        self.numero=n                                                                       #correspond au numéro du niveau
        self.fichier="Niveaux//"+str(self.numero+1)+".txt"                                  #charge le fichier txt du niveau actuel (numero+1 car le numéro commence à partir de 0)
        self.dict_images=images                                                             #créer un dictionnaire de toutes les images des éléments du niveau 

        self.depart=depart                                                                  #correspond à la position de départ du personnage
        self.creation()                                                                     #lance la fnction création

        Niveau.liste.append(self)                                                           #insert dans la liste tous les niveaux

    def creation(self):                 
        '''La méthode crée le niveau à partir du fichier qui lui correspond. 
        Il est appelé dans __init__ mais aussi quand on veut réinitialiser le niveau'''

        self.dict_images["ombre"].set_alpha(240)                                            #établi une transparance sur les images "ombres" du dictionnaire d'image
        self.noir=False                                                                     #détermine si le niveau est sombre ou pas, par défaut le niveau n'est pas sombre
        self.eclair=False                                                                   #détermine si l'éclair est actif ou non, par défaut l'éclair n'est pas actif
        self.ralenti=1                                                                      #permet de faire un ralenti dans le niveau, la valeur prise est un mutliplicateur de la vitesse des ennemis
        self.liste_ombre=[]                                                                 #créer une liste qui va contenir tous les blocs "ombre", qui vont perlettre de faire des niveaux sombres
        self.structure=[]                                                                   #créer une liste qui va contenir des chaines de caractères. Cette liste va permettre de créer la composition des niveaux
        self.astuce=[]                                                                      #créer une liste qui va contenir les texte permettant de faire le menu des astuces
        self.dict_element={ "bloc":[],                                                      #dictionnaire de tous les éléments qui peuventy composer un niveau
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
                            "caisse":[],
                            "bloc_tuto":[],
                            }

        with open(self.fichier,'r') as fichier:                                             #ouvre le fichier texte du niveau actuel en mode lecture en donnant "fichier" comme nom
            grille=fichier.readlines()                                                      #lis la totalité du texte on inserant chaques lignes dans une liste appelée "grille"
            for ligne in grille:                                                            #parcours la liste "grille", chaque élément est une chaine de caractère que l'on a appelé "ligne"
                if ligne[-1]=='\n':                                                         #test si le dernier caractère de la ligne est un retour à la ligne
                    self.structure.append(ligne[:-1])                                       #si c'est le cas, on insert la ligne sans le dernier caractère dans la liste "structure"
                else:
                    self.structure.append(ligne)                                            #si ce n'est pas le cas, on insert la totalité de la ligne dans la liste "structure"


        for y,ligne in enumerate(self.structure):                                           #parcours la liste "structure" en donnant l'élément ("ligne") et son indice ("y")
            if y<=17:                                                                       #test si l'indice de la ligne est inférieur ou égal à 17. 17 correspond au nombre de ligne de structure du fichier text. Au dela de 17, ce sont des lignes d'astuce
                for x,car in enumerate(ligne):                                              #parcours la chaine de caractère "ligne" en donnant le caractère ("car") et son indice ("x")                                        
                    if car!=" ":                                                            #test si "car" n'est pas un espace. Nos fichiers textes sont fait de sorte que un espace ne correspond à rien  
                        try:                    
                            int(car)                                                        #test si "car" est un chiffre
                            chiffre=True                                                    #si "car" est un chiffre, alors la variable "chiffre est True
                        except ValueError:                                                  #évite le message d'erreur si "car" n'est pas un chiffre
                            chiffre=False                                                   #si "car n'est pas un chiffre, alors la variable "chiffre" est False


                        if chiffre:                                                         #test si "chiffre" est True, donc test si "car" est un chiffre
                            if car=='1':                                                    #"car" est un chiffre, test si "car" est égal à 1
                                r=Bloc(self.dict_images["bloc"],(x*bloc_x , y*bloc_y))      #"car"=1, on crée un objet de la classe bloc avec comme parametre l'image du dictionnaire d'image qui correspond à "bloc", et la position qu'aura le bloc dans le niveau. On multiplie x (qui est le numero de la colonne) par bloc_x (qui est la longueur d'un bloc) et y (qui est le numero de la ligne) par bloc_y (qui est la hauteur d'un bloc)
                                self.dict_element["bloc"].append(r)                         #on ajoute le bloc dans le dictionnaire d'élément du niveau

                            elif car=='2':                                                  #test si "car"=2
                                f=Fin(self.dict_images["fin"],(x*bloc_x , y*bloc_y))        #"car"=2, on crée un objet de la classe fin avec comme parametre l'image du dictionnaire d'image qui correspond à "fin", et la position qu'aura le bloc dans le niveau. On multiplie x (qui est le numero de la colonne) par bloc_x (qui est la longueur d'un bloc) et y (qui est le numero de la ligne) par bloc_y (qui est la hauteur d'un bloc)
                                self.dict_element["fin"].append(f)                          #on ajoute la fin dans le dictionnaire d'élément du niveau

                            elif car=='3':                                                  #test si le chiffre "car" est égal à 3
                                t=Teleport(self.dict_images["tp"],(x*bloc_x , y*bloc_y))    #"car"=3, on crée un objet de la classe Teleport et utilise  l'image du dictionnaire qui represente le "Teleportation", et la position qu'aura le bloc teleportation dans le niveau. Ensuite on multiplie x (qui est le numero de la colonne) par bloc_x (qui est la longueur d'un bloc) et y (qui est le numero de la ligne) par bloc_y (qui est la hauteur d'un bloc)
                                self.dict_element["tp"].append(t)                           #on ajoute finalement  l'element du niveau dans le dictionnaire

                            elif car=='4':                                                 #on test si le chiffre "car" est égal à 4
                                t=Torche(self.dict_images["torche"],(x*bloc_x , y*bloc_y)) #"car"=4, on crée un objet de la classe Torche. Ensuite on utilise l'image du dictionnaire qui represente la "Torche", et la position qu'aura la torche dans le niveau. Ensuite on multiplie x (qui est le numero de la colonne) par bloc_x (qui est la longueur d'un bloc) et y (qui est le numero de la ligne) par bloc_y (qui est la hauteur d'un bloc)
                                self.dict_element["torche"].append(t)                      #on ajoute finalement l'element du niveau dans le dictionnaire

                            elif car=='5':                                                 #on test si le chiffre "car" est égal à 5
                                p=Porte(self.dict_images["porte"],(x*bloc_x , y*bloc_y))   #"car"=5, on crée un objet de la classe Porte. Ensuite on utilise l'image du dictionnaire qui represente la "Porte" et la position qu'aura la porte dans le niveau. Ensuite on multiplie x (qui est le numero de la colonne) par bloc_x (qui est la longueur d'un bloc) et y (qui est le numero de la ligne) par bloc_y (qui est la hauteur d'un bloc)
                                self.dict_element["porte"].append(p)                       #on ajoute finalement l'element du niveau dans le dictionnaire

                            elif car=='6':                                                 #on test si le chifre "car" est égal a 6
                                go=Goomba(self.dict_images["goomba"],(x*bloc_x , y*bloc_y))#"car"=6, on crée un objet de la classe Goomba. Ensuite on utilise l'image du dictionnaire qui represente la "Goomba" et la position qu'aura le goomba dans le niveau
                                self.dict_element["goomba"].append(go)                     #on ajoute finalement l'element du niveau dans le dictionnaire

                            elif car=="7":                                                  #on test si le chifre "car" est égal a 7
                                b=Bouton(self.dict_images["bouton"],((x*bloc_x , y*bloc_y)))#"car"=7, on crée un objet de la classe Bouton. Ensuite on utilise l'image du dictionnaire qui represente la "Bouton" et la position qu'aura le bouton dans le niveau
                                self.dict_element['bouton'].append(b)                       #on ajoute finalement l'element du niveau dans le dictionnaire
                                 
                            elif car=="8":                                                               #on test si le chifre "car" est égal a 8
                                p=PorteBouton(self.dict_images["porte bouton"],(x*bloc_x , y*bloc_y))#"car"=8, on crée un objet de la classe PorteBouton. Ensuite on utilise l'image du dictionnaire qui represente la "PorteBouton" et la position qu'aura la portebouton dans le niveau
                                self.dict_element["porte bouton"].append(p)                              #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car=="9":                                          #on test si le chifre "car" est égal a 9
                                p=Pic(self.dict_images["pic"],(x*bloc_x , y*bloc_y))#"car"=9, on crée un objet de la classe Pic. Ensuite on utilise l'image du dictionnaire qui represente la "Pic" et la position qu'aura le pic dans le niveau
                                self.dict_element["pic"].append(p)                  #on ajoute finalement l'element du niveau dans le dictionnaire

                        else:
                            if car=="p":                                                  #on test si le chifre "car" est égal a p
                                p=Pot(self.dict_images["pot"],(x*bloc_x+15 , y*bloc_y+15))#"car"=p, on crée un objet de la classe Pot. Ensuite on utilise l'image du dictionnaire qui represente la "Pot" et la position qu'aura le pot dans le niveau
                                self.dict_element["pot"].append(p)                        #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car=="c":                                                   #on test si le chifre "car" est égal a c
                                c=Coeur(self.dict_images["coeur"],(x*bloc_x+15, y*bloc_y+15))#"car"=c, on crée un objet de la classe Coeur. Ensuite on utilise l'image du dictionnaire qui represente la "Coeur" et la position qu'aura le coeur dans le niveau 
                                self.dict_element["coeur"].append(c)                         #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car=="k":                                             #on test si le chifre "car" est égal a k
                                ko=Koopa(self.dict_images["koopa"],(x*bloc_x,y*bloc_y))#"car"=k, on crée un objet de la classe Koopa. Ensuite on utilise l'image du dictionnaire qui represente la "Koopa" et la position qu'aura le koopa dans le niveau 
                                self.dict_element["koopa"].append(ko)                  #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car=="x":                                                #on test si le chifre "car" est égal a x
                                box=Caisse(self.dict_images["caisse"],(x*bloc_x,y*bloc_y))#"car"=x, on crée un objet de la classe Caisse. Ensuite on utilise l'image du dictionnaire qui represente la "Caisse" et la position qu'aura la caisse dans le niveau 
                                self.dict_element["caisse"].append(box)                   #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car=="t":                                               #on test si le chifre "car" est égal a t
                                t=Tuto(self.dict_images["bloc_tuto"],(x*bloc_x,y*bloc_y))#"car"=t, on crée un objet de la classe Tuto. Ensuite on utilise l'image du dictionnaire qui represente la "Tuto" et la position qu'aura le tuto dans le niveau
                                self.dict_element["bloc_tuto"].append(t)                 #on ajoute finalement l'element du niveau dans le dictionnaire

                            elif car=="n":                                               #on test si le chiffre "car" égal a n
                                self.noir=True                                           #l'ecran du jeu deviendra automatiquement noir car self.noir= True. Donc le noir est activé
                                
                            elif car.lower()==car:                                                       #on test si le chifre "car" est égal à une minuscule. La fonction lower va detecter les lettres en minuscule
                                i= Interrupteur(self.dict_images["interrupteur"],(x*bloc_x,y*bloc_y),car)#"car"=i, on crée un objet de la classe Interrupteur. Ensuite on utilise l'image du dictionnaire qui represente la "Interrupteur" et la position qu'aura l'interrupteur dans le niveau
                                self.dict_element["interrupteur"].append(i)                              #on ajoute finalement l'element du niveau dans le dictionnaire
                                
                            elif car.upper()==car:                                                                    #on test si le chifre "car" est égal à une majuscule. La fonction upper va detecter les lettres en majuscule
                                p=Porte_interrupteur(self.dict_images["porte interrupteur"],(x*bloc_x , y*bloc_y),car)#"car"=p, on crée un objet de la classe Porte Interrupteur. Ensuite on utilise l'image du dictionnaire qui represente la "Porte Interrupteur" et la position qu'aura la porte interrupteur dans le niveau
                                self.dict_element["porte interrupteur"].append(p)                                     #on ajoute finalement l'element du niveau dans le dictionnaire


                for i in self.dict_element["interrupteur"]:                              #pour chaque objet Interrupteur dans le dictionnaire
                    for indice,p in enumerate(self.dict_element["porte interrupteur"]):  #pour chaque objet PorteInterruptuer
                        if i.car==p.car:                                                 #on vérifie si les deux objets (interrupteur et porte) ont le même caractère pour les relier ensemble
                            i.liste_porte.append(indice)                                 #on peut mettre l'indice dans l'attribut liste_porte de l'interrupteur qui possède toutes les portes avec lesquelles elle interragit
            else:                                                                        #s'il s'agit d'une ligne après la ligne 17 (le texte de l'astuce)
                self.astuce.append(ligne)                                                #on rajoute la ligne de texte
        self.texte_astuce=[p_perfect.render(i,0,JAUNE) for i in self.astuce]             #à la fin, on crée les textes (Surface) avec un parcours de la liste astuce

    def update(self):                                     
        '''Le méthode permet de mettre à jour le niveau. Elle est appelée à chaque frame'''
        #-----------------Mise à jour des ombres--------------------
        self.liste_ombre=[]                                                              #La liste va contenir la postion de chaque rectangle d'ombres        
        if self.noir==True:                                                              #Si le niveau est sombre, on peut rajouter les ombres 
            for y in range(0,fenetre_y,self.dict_images["ombre"].get_height()):          #On fait une boucle for allant de 0 à la hauteur de la fenêtre avec un pas de la hauteur d'un rectangle d'ombre
                for x in range(0,fenetre_x,self.dict_images["ombre"].get_width()):       #On fait une boucle for allant de 0 à la largeur de la fenêtre avec un pas de la hauteur d'un rectangle d'ombre
                    self.liste_ombre.append((x,y))                                       #On peut rajouter les coordonnées dans la liste ombre (Il y a donc par défaut des rectangles d'ombres sur tout l'écran. Certains rectangles pourront être supprimés notamment par la torche et la boule de feu (voir leur update() )

        if self.eclair==True:                                                            #si l'attribut éclair est True (après avoir fait un éclair)
            self.dict_images["ombre"].set_alpha(self.dict_images["ombre"].get_alpha()+10)#nous allons rajouter une opacité de 10 aux ombres
        if self.dict_images["ombre"].get_alpha()>=240:                                   #une fois que la transparence redevient suffisament basse
            self.dict_images["ombre"].set_alpha(240)                                     #on la remet à sa valeur initiale
            self.eclair=False                                                            #pour arreter le réglage de l'opacité




class Personnage():                                         
    """L'objet Personnage représente le personnage joué. Il possède de nombreux attributs.
        Ainsi, un seul objet appartient à la classe Personnage: 
    """

    def __init__(self,pos,dict_img):                          
        """La création de l'objet nécessite 2 paramètres : sa position de départ et son dicionnaire d'images 
        """

        self.dict_img=dict_img                                #ce dictionnaire possède toutes les images des animations (voir megaman_images dans init.py)
        self.pv=2                                             #son niveau de vie est égale à 2 par défaut
        self.energie=15                                       #son niveau d'energie est donc de 15 par défaut
        self.invincible=False                                 #Cet attribut est True quand le personnage doit être invincible (False par défaut)
        self.img=dict_img["droite"]["debout"]                 #Il s'agit de l'image à afficher. (Par défaut, on le met immobile vers la droite.)
        self.rect=self.img.get_rect()                         #Il s'agit de son Rect (La classe appartient à pygame). Il permet de gérer facilement la position de surfaces rectangulaires.
        self.ancien=self.rect                                 #Il s'agit du rect de la frame précédent. Il sera utile dans la gestion des collisions    
        self.rect.x=pos[0]                                    #On met par défaut la position du rectangle (défini par les paramètres)
        self.rect.y=pos[1]                                    
        self.vitesse_x=0                                      #La vitesse va permettre le déplacement du personnage (par défaut, elle est de 0)
        self.vitesse_y=0                                      
        self.acceleration_x=0                                 #L'acceleration va accelerer le personnage (0 dans l'axe x, et g dans l'axe y) (voir constantes)
        self.acceleration_y=g                                
        self.animation=0                                      #Cet attribut va désigner l'image à afficher dans une liste d'animation (elle va changer toutes les 0.1 secondes)
        self.saut=True                                        #Savoir si le personnage est en saut permet notamment d'éviter les doubles sauts
        self.double_saut=False                                #Savoir si le personnage est en double saut permet notamment d'éviter les triples sauts (il s'active avec le pouvoir du point)
        self.deplacement=False                                #L'attribut est True quand le personnage est en déplacement (notamment utilse pour les animations)
        self.direction="droite"                               #L'attribut donne la direction du regard du personnage pour les animations (par défaut, à droite)
        self.clignotant=False                                 #L'attribut est True si le personnage doit clignoter (fortement lié avec invincible) 
        self.tuto=False                                       #True si on active le tutoriel. Cela permet de gérer des problèmes de variables entre fonctions


    def update(self,d_frame,niveau_actuel):               
        """ La méthode prend en paramètre la durée d’une frame et le niveau actuel et peut renvoyer None si rien de particulier est arrivé ou des chaînes de caractères dans le cas contraire. 
        On renvoie :
        “mort” si le personnage n’a plus de point de vie, s’il sort de la fenêtre par le bas, s’il touche un pic ou un ennemi invisible.
        “ touche” s’il se fait toucher par un ennemi basique,
        “suivant” s’il touche le point de fin du niveau
        La méthode est appelée à chaque frame
        """
        
        #----------------------Animation------------------------------
        self.clignotant=self.invincible                                     #le personnage clignote quand il est invincible 
        
                                                                            #Le dictionnaire est sous la forme dict["direction"]["état"][numero de l'animation]
        if self.deplacement==True:                                          #si le personnage est en deplacement alors l'état est "cours" et on anime le personnage avec l'attribut animation(qui devient successivement 0,1,2,3 puis redevient 0 toutes les 0.1 secondes)
            self.img=self.dict_img[self.direction]["cours"][self.animation] 
        if self.saut==True:                                                 
            self.img=self.dict_img[self.direction]["saute"]                #si le personnage est en saut alors l'état est "saut"        
        if self.deplacement==False and self.saut==False:                    
            self.img=self.dict_img[self.direction]["debout"]               #dans les autre cas l'état est "debout"     

             

        #----------------Mouvement----------------------

        self.ancien=deepcopy(self.rect)                                     #Ancien devient le Rect précédent

        self.vitesse_x+=self.acceleration_x                                 #On accelère la vitesse. (Voir annexe pour le fonctionnement)
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)     #On bouge le rectangle en fonction de la vitesse. (Voir annexe pour le fonctionnement de d_frame)

        self.saut=True                                                      #Le perso est en saut dans tous les cas sauf cas il touche le sol


        #--------Restraindre position dans la fenetre-----------    (voir annexe pour schémas)
        if self.rect.top>=fenetre_y:            #Si le haut du personnage est en dessous du bas de la fenetre
            return "mort"                       #Le personnage est mort, on retourne "mort" vers la fonction jeu()
        elif self.rect.top<0:                   #Si le haut du personnage percute le haut de la fenetre
            self.rect.top=0                     #On remet le haut au bon endroit
            self.vitesse_y=0                    #Le personnage perd sa vélocité verticale
        if self.rect.right>=fenetre_x:          #Même raisonnement
            self.rect.right=fenetre_x
            self.vitesse_x=0
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=0

        #-----------------------------Collision----------------------- 
        
        liste_rect=[]                                                       #La liste possède tous les Rect des objets avec lesquel le personnage peut collisioner (sans problème contrairement aux ennemis)                                  
                                                                            #Il y donc :
        for i in niveau_actuel.dict_element["bloc"]:                        #Les blocs (basiques)          
            liste_rect.append(i.rect)                                       
        for i in niveau_actuel.dict_element["porte"]:                       #Les portes si elles sont ouvertes
            if i.ouvert==False:                                             
                liste_rect.append(i.rect)                                  
        for i in niveau_actuel.dict_element["porte interrupteur"]:          
            if i.ouvert==False:                                            
                liste_rect.append(i.rect)                                 
        for i in niveau_actuel.dict_element["porte bouton"]:              
            if i.ouvert==False:                                       
                liste_rect.append(i.rect)                               
        for i in niveau_actuel.dict_element["bouton"]:                      #Les boutons
            liste_rect.append(i.rect)                                   
        for i in niveau_actuel.dict_element["caisse"]:                      #Les caisses
            if i.hold==None:                                                #On ne met pas de collision quand le personnage tient la caisse pour éviter certains bugs
                liste_rect.append(i.rect)           
                
                
        i_collision=self.rect.collidelistall(liste_rect)                    #On trouve la liste des indices des objets avec lesquels le personnage est en collision
        for rect in [liste_rect[i] for i in i_collision]:                   #On parcours la liste des rectangles en collision 
            if self.ancien.bottom<=rect.top<=self.rect.bottom:              #Si le personnage avait son bas au dessus du haut de l'obstacle et qu'il est maintenant en dessous de l'obstacle : il y a eu collision par le haut de l'obstacle
                self.rect.bottom=rect.top                                   #On remet le bas du personnage sur l'obstacle
                self.vitesse_y=0                                            #Sa vitesse redevient nulle
            elif self.rect.top<=rect.bottom<=self.ancien.top:               #Meme raisonnement pour les quatres directions
                self.rect.top=rect.bottom
                self.vitesse_y=0

            elif self.ancien.right<=rect.left<=self.rect.right:             
                self.rect.right=rect.left                                   

            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right


        for rect in liste_rect:                                             #On veut mainenant gérer les collisions manuellement car pygame ne gère pas les collisions où les bordures des deux rectangles sont au même endroit
            if (self.rect.bottom==rect.top) and (rect.left<self.rect.left<rect.right or rect.left<self.rect.right<rect.right): #Donc, si le bas du personnage est exactement sur l'obstacle (ce qui se passe également quand il y a eu collision par la haut grâce à la remise en position ci-dessus) et que le personnage se trouve bien au dessus de l'obstacle (ce qui arrive également quand il y a eu collision)
                self.saut=False             #Le personnage a les pieds sur terre, on peut remettre saut et double saut à False
                self.double_saut=False
                
        #------------------Autres collisions-----------------------
        for i in niveau_actuel.dict_element["bloc_tuto"]:               #On regarde maintenant s'il y a eu collision avec un bloc
            if self.rect.colliderect(i.rect):                           #S'il y a collision:
                self.tuto=True                                          #L'attribut tuto devient True pour lancer le tutoriel
            else:       
                self.tuto=False                                         #Sinon l'attribut devient False
                i.toucher=False                                         #L'attribut touché du bloc tutoriel redevient False 
                
        #Les collisions avec les ennemis ne fonctionnent que si le personnage n'est pas invicible.
        #collidelist() renvoie -1 s'il n'y a aucune collision ou l'indice de l'objet avec lequel il y a collisiobn
        if self.rect.collidelist(niveau_actuel.dict_element["goomba"])!=-1 and self.invincible==False:  #Collision avec un "goomba"
            self.pv-=1                                                  #Le personnage pert un point de vie
            return "touche"                                             #On retourne "touche" vers le main.py
        if self.rect.collidelist(niveau_actuel.dict_element["koopa"])!=-1 and self.invincible==False:   #S'il y a collsion avec "koopa"
            return "mort"                                               #On retourne "mort" vers le main.py
        if self.rect.collidelist(niveau_actuel.dict_element["pic"])!=-1 and self.invincible==False:
            return "mort"                                               #On retourne "mort" vers le main.py

        i=self.rect.collidelist(niveau_actuel.dict_element["pot"])      #On capture l'indice de l'objet en collision
        if i!=-1 and self.energie<15:                                   #S'il y a eu collision, et si l'énergie n'est pas déjà maximale
            if self.energie<=10:    self.energie+=5                     #On donne 5 points d'énergie
            else:                   self.energie=15                     #Pour éviter d'avoir plus que le maximum, on limite jusqu'a 15 points.
            niveau_actuel.dict_element["pot"].pop(i)                    #On peut ensuite supprimer l'objet de la liste des éléments

        i=self.rect.collidelist(niveau_actuel.dict_element["coeur"])    #Même raisonnement
        if i!=-1 and self.pv==1:
            self.pv=2                                                   #On remet le nombre de point de vie à 2
            niveau_actuel.dict_element["coeur"].pop(i)                  #On supprime l'obejt de la liste

        if self.rect.colliderect(niveau_actuel.dict_element["fin"][0].rect):    #On teste la collision avec le point de fin
            return "suivant"                                            #On retourne "suivant" vers le main si c'est le cas
        if self.pv==0:                                                  #Si personnage n'a plus de point de vie:
            return "mort"                                               #On retourne "mort" vers le main
        

        for i in niveau_actuel.dict_element["caisse"]:                  #On va lacher la caisse si elle est trop loin du personnage.
            if distance(i.rect.center,self.rect.center)>35:
                i.hold=None

#----------------------Elements du niveau---------------------

#La création des éléments se fait dans Niveau.creation()
#Toutes les autres classes se basent sur la même structure.


class Bloc():
    """ L'objet bloc est le bloc sur lequel le personnage de déplace. 
        La structure de cette classe est la structure par défaut de toutes les autres classes
    """
    def __init__(self,img,pos):
        """La création se fait avec l'image qui lui correspond et sa position, obtenue précédemment avec le fichier niveau
        """
        
        self.img=img
        self.rect=self.img.get_rect()               #Création du Rect à partir de l'image
        self.rect.topleft=pos                       #Positionnment du Rect grâce au paramètre position
    def update(self,perso,d_frame,niveau_actuel):
        """Tous les objet.update() des éléments du niveau prennent les mêmes paramètres pour simplifier le programme lors de l'appel de cette méthode (voir jeu() dans fonctions_jeu.py)
            L'objet personnage, la durée d'une frame, et l'objet Niveau
        """
        pass                                        #Pour le bloc, il n'y a pas d'interraction particulière (la collision est gérée dans la méthode update du personnage)

class Pot():
    """L'objet Pot est l'objet qui redonne de l'energie au personnage si il y a collision
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass                                        #Pour le pot d'encre, il n'y a pas d'interraction particulière (le gain d'énergie est géré dans jeu() )

class Coeur():
    """L'objet Coeur est l'objet qui redonne de la vie au personnage si il y a collision
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass                                        #Pour le coeur, il n'y a pas d'interraction particulière (le gain de points de vie est géré dans jeu() )

class Pic():
    """L'objet Pic est l'objet qui tue le personnage s'il y a collision
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass                                        #Pour les pics, il n'y a pas d'interraction particulière (la collision est gérée dans la méthode update du personnage)

class Bouton():
    """L'objet Bouton est un bloc qui ouvre les objets PorteBouton si tous les objet Boutons sont appuyés
    """
    def __init__(self,liste_img,pos):
        self.liste_img=liste_img                    #Ici, la paramètre image est une liste d'image: 0 pour l'image du bouton appuyé, et 1 pour l'image du bouton non appuyé
        self.img=self.liste_img[1]                  #On crée l'image à afficher (par défaut : non appuyé)
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.appuye=False                           #On donne l'attribut appuyé qui indique si le bouton est appuyé ou non

    def update(self,perso,d_frame,niveau_actuel):
        liste_collision=[]                              #La liste contient tous les Rect des objets qui peuvent appuyer sur le bouton
        liste_collision.append(perso.rect)              #On met le rect du personnage,
        for i in niveau_actuel.dict_element["goomba"]:  #les rects des goomba,
            liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["koopa"]:   #les rects des koopa,
            liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["caisse"]:  #les rects des caisses
            liste_collision.append(i.rect)

        self.appuye=False                           #On met par défaut appuyé=False (on va mettre True s'il y a collision)
        for rect in liste_collision:                #On travaille sur tous les rects de liste crée ci-dessus
            if rect.bottom==self.rect.top and self.rect.left<rect.centerx<self.rect.right:  #Si le bas de l'objet est au même niveau que le haut du bouton (donc si l'objet est sur le bouton), et que son centre se trouve bien entre les bords gauche et droits du bouton(il est bien juste au dessus)
                self.appuye=True                    #L'objet est bien sur le bouton, on met l'attribut appuyé à True


        if False not in [i.appuye for i in niveau_actuel.dict_element["bouton"]]:   #On prend la liste des attributs appuyé de tous les boutons du niveau, puis on vérifie s'il sont tous True (donc qu'il n'y a pas de False)
            for i in niveau_actuel.dict_element["porte bouton"]:                    #Donc, tous les boutons sont appuyés, on va interragir avec toutes les portes boutons 
                i.ouvert=True                                                       #On va les ouvrir.
        else:                                                                       #S'il y a au moins un False (si au moins un bouton n'est pas appuyé)
            for i in niveau_actuel.dict_element["porte bouton"]:                    #On va fermer les portes
                i.ouvert=False
    
        #On gère les images   
        if self.appuye: self.img=self.liste_img[0]                                  #On met l'image à afficher : 0 si appuyé
        else:           self.img=self.liste_img[1]                                  # 1 si non appuyé

class PorteBouton():
    """L'objet PorteBouton est le bloc qui doit s'ouvrir si tous les boutons sont appuyés.
    """
    def __init__(self,liste_img,pos):
        self.liste_img=liste_img                #On a une liste d'image à cause de l'animation
        self.img=liste_img[0]                   #On met par défaut l'image à afficher 0
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False                       #On a l'attribut ouvert
        self.animation=0                        

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation] #On change l'image en fonction de l'animation (voir les animations dans jeu() de fonctions_jeu.py)

class Fin():                    
    """L'objet fin est le point que le personnage doit atteindre
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
    def update(self,perso,d_frame,niveau_actuel):
        pass                                    #Pour la fin, il n'y a pas d'interraction particulière (la collision est gérée dans la méthode update du personnage)


class Teleport():
    """ L'objet Teleport est le bloc qui permet la téléportation
        Il a 4 états qui changent selon la distance.
    """
    def __init__(self,liste_img,pos):
        self.etat=4                             #On met l'état qui va changer selon la distance avec le personnage qui va déterminer l'énergie nécessaire
        self.liste_img=liste_img                #il y a ici une liste d'images
        self.img=self.liste_img[self.etat]      
        self.rect=self.img.get_rect()
        self.rect.topleft=pos

    def update(self,perso,d_frame,niveau_actuel):
        #Changement couleur
        
        d=distance(perso.rect.center,self.rect.center)  #On calcule grâce à notre fonction distance la distance entre le centre du Rect du personnage le centre du Rect du bloc de téléportation

        if d<100:       self.etat=0                     #On change l'état en fonction de cette distance
        elif d<200:     self.etat=1
        elif d<300:     self.etat=2
        elif d<400:     self.etat=3
        else:           self.etat=4

        self.img=self.liste_img[self.etat]              #On change l'image à afficher selon l'état

class BouleFeu():
    """L'objet BouleFeu est la boule de feu crée par le sort qui correspond (l'angle)
    """
    def __init__(self,dict_img,direction,perso):
        """La création se fait dans jeu() de fonctions_jeu.py. Elle nécessite une direction (choisie par la direction de l'angle : voir r_angle() dans fonctions() )
        """
        self.dict_img=dict_img                          #On a un dictionnaire dont les valeurs sont une liste d'image qui correspond à l'animation de la boule. Les clés du dictionnaire sont les 4 directions
        self.direction=direction                        #On met l'attribut direction
        self.img=self.dict_img[self.direction][0]       #On crée l'image à afficher

        self.rect=self.img.get_rect()
        self.rect.center=perso.rect.center      
        self.acceleration_x=0                           #Le système de mouvement est le même que pour le personnage (même s'il n'y a pas d'acceleration)
        self.acceleration_y=0

        if self.direction=="droite":                    #On donne une vitesse initiale selon la direction
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


        #-----------------Mouvement----------------- (voir Personnage.update() )

        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y
        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y)


        #------------------------Animation-------------------
        self.img=self.dict_img[self.direction][self.animation]  #Le dictionnaire est sous la forme : dict["direction"][numero de l'animation]

        #---------------Restraindre position dans la fenetre-----------
        if self.rect.left>fenetre_x or self.rect.bottom<0 or self.rect.right<0 or self.rect.top>fenetre_y:  #Voir Personnage.update()
            niveau_actuel.dict_element["boule feu"].remove(self)            #On retire l'objet de la liste des éléments du niveau       
            del self                                                        #On supprime l'objet en question
            return 0                                                        #On retourne une valeur pour quitter la méthode et éviter les erreurs suite à la suppression de l'objet

        #----------------------Collision-----------------------------

        liste_collision=[]                              #Liste des Rect des objets où la boule s'arrete sans effets lors d'une collision
        for i in niveau_actuel.dict_element["bloc"]:    
            liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["porte"]:   #On ajoute les rect des portes si elles ne sont pas ouvertes
            if i.ouvert==False:
                liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["porte interrupteur"]:
            if i.ouvert==False:
                liste_collision.append(i.rect)
        for i in niveau_actuel.dict_element["caisse"]:
            liste_collision.append(i.rect)

        i_collision_torche=self.rect.collidelist(niveau_actuel.dict_element["torche"])      #On calcule l'indice de la torche collisionnée dans le dict_element (-1 s'il n'y a pas collision)
        i_collision_goomba=self.rect.collidelist(niveau_actuel.dict_element["goomba"])      #On calcule l'indice du "goomba" collisionné dans le dict_element (-1 s'il n'y a pas collision)
    
        if i_collision_torche!=-1 and niveau_actuel.dict_element["torche"][i_collision_torche].enflamme==False: #Si il y a bien eu collision, et que la torche en question est bien éteinte.
            niveau_actuel.dict_element["torche"][i_collision_torche].enflamme=True          #On asigne True à l'attribut "enflammé" de cette torche
            niveau_actuel.dict_element["boule feu"].remove(self)                            #On enlève la boule de feu de la liste
            del self                                                                        #On la supprime 
            return 0                                                                        #On quitte la méthode

        elif self.rect.collidelist(liste_collision)!=-1:                                    #S'il y a collision avec : un bloc, une porte fermée, ou une caisse
            niveau_actuel.dict_element["boule feu"].remove(self)                            #On enlève la boule de la liste
            del self                                                                        #On la supprime
            return 0                                                                        #On quitte la méthode

        elif i_collision_goomba!=-1:                                                        #S'il y a collision avec un goomba
            niveau_actuel.dict_element["goomba"].pop(i_collision_goomba)                    #On retire le goomba de la liste
            niveau_actuel.dict_element["boule feu"].remove(self)                            #On retire la boule de feu de la liste
            del self                                                                        #On supprime la boule de feu
            return 0                                                                        #On quitte la méthode


        #---------------Eclairage---------------
        l=[o for o in niveau_actuel.liste_ombre if distance(self.rect.topleft,o)<=100]      #Il s'agit de la liste des ombres à supprimer : si la distance entre l'ombre et la boule est inférieure à 100 pixels
        for o in l:                                                                         #On va retire ces ombres avec un parcours de la liste des ombres à supprimer
            niveau_actuel.liste_ombre.remove(o)

class Torche():
    """L'objet Torche est la torche qui éclaire le niveau si elle est enflammée
    """
    def __init__(self,dict_img,pos):

        self.dict_img=dict_img
        self.img=dict_img["Arret"]          #voir init.py pour la structure du dictionnaire
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.enflamme=False                 #on crée l'attribut enflammé pour savoir quand il faut éclairer.
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        if self.enflamme==True:                                 #Si la torche est enflammée
            self.img=self.dict_img["Flamme"][self.animation]    #On met à jour l'image à afficher

            l=[o for o in niveau_actuel.liste_ombre if distance(self.rect.topleft,o)<=100]  #Création de la liste des ombres à supprimer (Voir BouleFeu.update() )
            for i in l: 
                niveau_actuel.liste_ombre.remove(i)             #Suppression des ombres (voir BouFeu.update())
        else:                                                   #Si la torche est éteinte
            self.img=self.dict_img["Arret"]                     #On met à jour l'image


class Porte():
    """L'objet porte est le bloc qui peut être cassé par le trait. Elle est similaire à la classe PorteBouton 
    """
    
    def __init__(self,liste_img,pos):
        self.liste_img=liste_img
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False
        self.animation=0

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation]         #La gestion du coupage se trouve dans jeu() de fonctions_jeu()


class Bulle():
    """L'objet Bulle est la bulle qui fait voler l'objet. Elle est crée dans jeu()
    """
    def __init__(self,img,obj):
        self.img=img
        self.obj=obj                    #Il s'agit de l'objet dans la bulle (voir jeu())
        self.rect=self.img.get_rect()
        self.rect.center=self.obj.rect.center

    def update(self,perso,d_frame,niveau_actuel):

        self.rect.center=self.obj.rect.center   #On bouge la bulle au même endroit que l'objet 
        self.obj.acceleration_y=-g/2            #On donne une acceleration y de -0.5g à l'objet pour le faire voler.
        if type(self.obj)==Goomba:                                      #Si la classe de l'objet est Goomba
            if self.obj not in niveau_actuel.dict_element["goomba"]:    #S'il n'y a plus cet objet dans la liste ( si le goomba est mort )
                niveau_actuel.dict_element["bulle"].remove(self)        #On supprime la bulle de la liste    
                del self                                                #On supprime la bulle
                return 0                                                #On quitte la méthode (inutile dans ce cas là)

class Interrupteur():
    """L'objet Interrupteur est l'interrupteur qui contrôle certains blocs et allumables par l'éclair
    """
    def __init__(self, dict_image, pos,car):
        self.car=car                        #On met le caractère utilisé dans le fichier pour relier les interrupteurs "a" aux portes "A", "b" à "B", etc...
        self.dict_image= dict_image
        self.img= dict_image["Ouvert"]      #Voir init.py
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=True                    #On met l'attribut qui indique si 'l'interrupteur est ouvert ou non (dans le sens électronique du terme)
        self.liste_porte=[]                 #Il s'agit de la liste des portes qu'elle contrôle. Elle se remmplit dans niveau.creation()

    def update(self,perso,d_frame,niveau_actuel):           #L'activation est gérée dan jeu()
        if self.ouvert==False:                              #Si l'interrupeur est activé
            self.img=self.dict_image["Ferme"]               #On met à jour l'image à afficher
            for i,porte in enumerate(niveau_actuel.dict_element["porte interrupteur"]):     #On travaille sur toutes les portes interrupteur
                if i in self.liste_porte:                                                   #Qui appartiennent à la liste des portes que l'interrupteur contrôle
                    porte.ouvert=True                                                       #On ouvre cette porte

        else:                                                                               #Inversement dans le cas contraire
            self.img=self.dict_image["Ouvert"]
            for i,porte in enumerate(niveau_actuel.dict_element["porte interrupteur"]):
                if i in self.liste_porte:
                    porte.ouvert=False

class Porte_interrupteur():
    """L'objet Porte_interrupteur est le bloc qui s'ouvre si l'interrupteur qui le controle est activé
    """ 
    def __init__(self,liste_img,pos,car):
        self.car=car.lower()                           #On met le caratère utilisé dans le fichier (voir  Interrupteur.__init__()) Si le caractère était "A", il devient "a"
        self.liste_img=liste_img                       #L'animation se fait de la même manière que les autres portes (voir PorteBouton)
        self.img=liste_img[0]
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ouvert=False                               #On met l'attribut qui indique si la porte esr ouverte
        self.animation=0    

    def update(self,perso,d_frame,niveau_actuel):
        self.img=self.liste_img[self.animation]

class Caisse(): 
    """L'objet Caisse est le bloc déplacable par le personnage. (voir Personnage.update() et jeu())
        Elle fonctionne grandement de la même manière que le personnage.
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.ancien=self.rect                   #Pour la collision (voir Personnage() )
        self.vitesse_x=0                        #Pour le mouvement
        self.vitesse_y=0
        self.acceleration_x=0
        self.acceleration_y=g
        self.hold=None                          #None si elle n'est n'est pas tenue, "droite" si le personnage est à droite de la caisse, "gauche" s'il est à gauche
    
    def update(self, perso, d_frame, niveau_actuel):
        #Liste des elements de collision    (voir Personnage)
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


        #-----------------Mouvement(voir Personnage)---------------
        self.ancien=deepcopy(self.rect)
        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y

        self.rect=self.rect.move(self.vitesse_x*d_frame,self.vitesse_y) #note : les vitesses_x seront toujours nulles
    
        #Mouvement par la poussée du personnage
        if self.hold=="gauche":                 #Si le personnage tient la caisse par la gauche
            self.rect.left=perso.rect.right     #Le bord gauche de la caisse se met sur la droite du personnage
        elif self.hold=="droite":               #Si le personnage tient la caisse par la droite
            self.rect.right=perso.rect.left     #Le bord droit de la caisse se met sur la gauche du personnage





        #---------------Restraindre position dans la fenetre(voir Personnage)---------------
        if self.rect.top>fenetre_y:                             #Si la caisse tombe hors de la fenetre
            niveau_actuel.dict_element["caisse"].remove(self)   #On retire la caisse de la liste des éléments du niveau
            del self                                            #On la supprime
            return 0                                            #On quitte la méthode
        if self.rect.top<0:
            self.rect.top=0
            self.vitesse_y=0
        if self.rect.right>=fenetre_x:
            self.rect.right=fenetre_x
            self.vitesse_x=-0
            if self.hold=="gauche":                             #Si on tient la caisse par la gauche et que la caisse sort vers la droite de l'écran
                perso.rect.right=self.rect.left                 #Le personnage ne peut plus avancer, on le remet à l'emplacement de la caisse
        elif self.rect.left<=0:
            self.rect.left=0
            self.vitesse_x=0
            if self.hold=="droite":                             #Même raisonnement
                perso.rect.left=self.rect.right
                
        #--------------------Collision------------------- (voir Personnage)
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
                self.vitesse_x=0
                if self.hold=="gauche":                         #Si la caisse a une collision vers la droite, et que le personnage la tient par la gauche
                    perso.rect.right=self.rect.left             #Le personnage n'avance plus


            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right
                self.vitesse_x=0
                if self.hold=="droite":                         #Même raisonnement
                    perso.rect.left=self.rect.right

class Tuto():
    """L'objet Tuto est le bloc qui lance le tutoriel quand on le touche. La collision est gérée dans Personnage.update et jeu()
    """
    def __init__(self,img,pos):
        self.img=img
        self.rect=self.img.get_rect()
        self.rect.topleft=pos
        self.toucher=False              #L'attribut montre si bloc a été touché. Il devient True quand le personnage le touche, et redevient False quand il quitte le bloc. Cela permet d'éviter de relancer le tutoriel quand on le quitte car le personnage serait encore sur le bloc

    def update(self,perso,d_frame,niveau_actuel):
        pass



class Goomba():
    """L'objet Goomba est l'ennemi basique lent. Il fonctionne presque de la même manière que Personnage
    """
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

    #----------------------Liste des elements de collision----------------------
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

        #---------------Mouvement---------------
        self.ancien=self.rect
        self.vitesse_x+=self.acceleration_x
        self.vitesse_y+=self.acceleration_y
        self.rect=self.rect.move(self.vitesse_x*d_frame*niveau_actuel.ralenti,self.vitesse_y)



        #-------------------Restraindre position dans la fenetre-----------------
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


        #--------------------Collision------------------
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
                self.vitesse_x=-50  #S'il y a collision par la droite, le goomba change de direction et se déplace de 50 pixels vers la gauche par seconde

            elif self.rect.left<=rect.right<=self.ancien.left:
                self.rect.left=rect.right
                self.vitesse_x=50   #S'il y a collision par la gauche, le goomba change de direction et se déplace de 50 pixels vers la droite par seconde


        #Animation
        self.img=self.liste_img[self.animation]

class Koopa():
    """L'objet Koopa est l'ennemi rapide. Il fonctionne exactement de la même manière que Goomba mais sa vitesse est 10 fois plus élevé (et il ne peut pas être détruit par le joueur)
    """
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

        self.rect=self.rect.move(self.vitesse_x*d_frame*niveau_actuel.ralenti,self.vitesse_y)



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













