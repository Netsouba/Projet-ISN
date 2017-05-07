import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy


from constantes import *

#-----------------------------------Fontions maths--------------------------------
def moyenne(liste):
    """La fonction prend en paramètre une liste de réels et retourne sa moyenne.
    S'il la liste est vide, elle renvoie 0.
    """
    try:                                                                        
        return sum(liste)/len(liste)                                                #sum() est une fonction dans python qui fait la somme des termes d'une liste
    except ZeroDivisionError:
        return 0
    
def milieu(point_a,point_b):
    """La fonction prend en paramètres deux tuples qui sont sont les coordonnées de deux points. 
    On renvoie ainsi les coordonnées du milieu.
    """
    ax,ay=point_a           #On pose ax,ay,bx et by, les coordonnées des points.
    bx,by=point_b
    m=(ax+bx)/2,(ay+by)/2
    return m

def distance(point_a,point_b):
    """La fonction prend en paramètres deux tuples qui sont sont les coordonnées de deux points. 
    On renvoie ainsi la distance entre ces points."""

    return math.sqrt((point_b[0]-point_a[0])**2+(point_b[1]-point_a[1])**2)

def droite(point_a,point_b):
    """La fonction prend en paramètres deux tuples qui sont sont les coordonnées de deux points A et B. 
    Elle renvoie une liste de points qui appartiennent au segement [AB]:
    """
    
    if point_a[0]>point_b[0]:               #On va admettre que le point A est à gauche du point B.
        point_a,point_b=point_b,point_a     #Donc si ce n'est pas le cas, on échange les deux points
    ax,ay=point_a                           #On pose ax,ay,bx et by, les coordonnées des points.
    bx,by=point_b

    try:
        delta=(by-ay)/(bx-ax)                                       #delta est le taux d'accroissement de la droite (AB). Il s'agit de f'(x)
        liste_point=[(x,delta*(x-ax)+ay) for x in range(ax,bx)]     #on parcours chaque x entre ax et bx et 
                                                                    #on met dans la liste_point le point de coordonnées ( x; f'(x)(x-ax)+f(ax) )
    
    except ZeroDivisionError:                                       #Une ZeroDivisionError sera interceptée si la droite est vericale.

        liste_point=[(ax,y) for y in range(ay,by,3)]                #Si la droite est vericale, on fait la liste en parcourant les y entre ay et by avec un pas de 3 pour eviter qu'il y ait trop de termes.
                                                                    #Tous les points ont la meme abscisse que A et ont comme ordonnée y.
    return liste_point

def croissance(liste):
    """ La fonction prend en paramètres une liste. On considère qu'il s'agit d'une suite.
    Elle renvoie une liste_p qui possède les indices dans la liste des extremums locaux ainsi que les variations de cette liste dans liste_c.
    """

    liste_c=[]                          #Cette liste va avoir les variations de la liste. Croissant=True et décroissant=True
    liste_p=[]                          #Cette liste va avoir les indices des extremums locaux.
    croissant=None                      #croissant est une variable qui va indiquer True ou False.
                                        #Pour le premier terme, croissant = None        
    for i in range(len(liste)-1):       #On parcours la liste sans le dernier terme.
        
        if liste[i+1]>liste[i]:         #Si u(n+1)>u(n), la suite est croissante en i.
            if croissant==None:         #S'il s'agit du premier terme:
                liste_c.append(True)    #On peut ajouter True dans la liste_c
    
            elif croissant==False:      #Si la suite était décroissante en i-1, et qu'elle est croissante en i,
                liste_p.append(i)       #On pose i en tant qu'extremum
                liste_c.append(True)    #On peut ajouter True dans la liste_c
        
                                        #Si la suite était déjà croissante, on ne change rien
            
            croissant=True              #On change ici croissant

            
        elif liste[i+1]<liste[i]:       #Si u(n+1)<u(n), la suite est décroissante en i.
                                        #Il d'agit du même raisonnement que si la suite était croissante, mais nous avons changé les True en False
            if croissant==None:
                liste_c.append(False)
                
            elif croissant==True:
                liste_p.append(i)
                liste_c.append(False)

            croissant=False

    return liste_p,liste_c              #On peut retourner liste_p et liste_c

def calc_ecart_type(liste):
    """La fonction prend en paramètre une liste.
    Elle renvoie la valeur de l’écart type. 
    """
    moyenne_l=moyenne(liste)                        #On réutilise la fonction moyenne() pour trouver la moyenne de la liste
    l=[(i-moyenne_l)*(i-moyenne_l) for i in liste]  #On crée une liste qui possède le carrée de la différence entre le terme et la moyenne.
    return math.sqrt(sum(l))                        #sum(l) est donc la variance de la liste. Pour avoir l'écart type, on peut prendre la racine carrée.

def interdiagonalequadri(a,b,c,d):
    """La fonction prend en paramètres quatres tuples qui sont sont les coordonnées de quatres points A,B,C,D. 
    On renvoie ainsi les coordonnées de l’intersection I de la diagonale du quadrilatère ABCD.
    """
    v_ac=(c[0]-a[0],c[1]-a[1])                      #v_ac est le vecteur AC
    v_bd=(d[0]-b[0],d[1]-b[1])                      #b_bd est le vecteur BD
    
    try:  
        x=b[0]+v_bd[0]*(a[1]+(v_ac[1]*b[0]-v_ac[1]*a[0])/v_ac[0]-b[1])/(v_bd[1]-v_ac[1]*v_bd[0]/v_ac[0])    #Voir le dossier pour une explication approfondie de la formule
        y=b[1]+v_bd[1]*(a[1]+(v_ac[1]*b[0]-v_ac[1]*a[0])/v_ac[0]-b[1])/(v_bd[1]-v_ac[1]*v_bd[0]/v_ac[0])
        return int(x),int(y)
    
    except ZeroDivisionError:   #On renvoie "erreur" s'il y a une division erreur. 
        return 'Erreur'             #Puisque les points sont posés avec les souris, l'erreur est assez rare.


#--------------------------------Fonctions reconnaissance----------------------
def r_droite(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie un booléen indiquant s'il s'agissait à peu près d'une droite, et une liste de points qui relie le premier et le dernier point du dessin.
    Stratégie utilisée : capturer les taux d'accroissement à chaque point vérifier qu'il n'y a pas de grandes différences entre eux.
    """
    acroissement=[]                     #cette liste va avoir les taux d'accroissement à chaque points         
    for i in range(len(liste_pos)-1):   #On parcours la liste de points sans la derniere.
        try:                            #On ne travaille pas sur deux points successifs qui ont la même abscisse. 
            acroissement.append((liste_pos[i+1][1]-liste_pos[i][1])/(liste_pos[i+1][0]-liste_pos[i][0]))    # On utilise la formule (yb-ya)/(xb-xa)
        except ZeroDivisionError:       #Puisque le dessin est manuel, il est difficile de tracer verticalement. Ainsi, cette exception pose assez peu de problèmes. 
            pass

                                                            #On réutilise notre fonction de l'écart type.
    ecart_type=calc_ecart_type(acroissement)                #L'écart type est un bon indicateur de la dispersion et de l'homogénéité de la liste
                                                            #Plus l'écart type est petit, plus la liste est homogène.
    if ecart_type<=1.5:                                     #La valeur a été choisie arbitrairement après plusieurs tests.                
        return True,droite(liste_pos[0],liste_pos[-1])      #Si l'écart type est suffisament petit, on peut revoie True et on réutilise notre fonction droite pour avoir une liste de points qui relie le premier et le dernier point du dessin. 
    else:                                               
        return False,None

def r_point(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie un booléen indiquant s'il s'agissait à peu près d'un point, et la position de ce point.
    Stratégie utilisée : Vérifier si la distance entre le premier point et chaque autre point est très petite.
    """    
    liste_distance=[distance(liste_pos[0],point) for point in liste_pos]    #On parcours la liste des points et on réutilise notre fonction distance
    moy= moyenne(liste_distance)                                            #On réutilise notre fonction moyenne
    if moy<=1:                                                              #La valeur a été choisie arbitrairement après plusieurs tests.                                          
        return True,liste_pos[0]                                            #Si les points sont assez proches entre eux, on retourne True et le premier point du dessin 
    else:
        return False,None


def r_angle(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie "bas","droite",gauche" ou "haut" en fonction de la direction de l'angle, et la position du pic de l'angle
    Stratégie utilisée : Regarder les variations de x et y, puis réutiliser la fonction de reconnaissance r_droite pour vérifier si les traits sont droits
    """    
    liste_x=[i[0] for i in liste_pos]                                       #On parcours la liste pour avoir seulement les x et les y dans une liste
    liste_y=[i[1] for i in liste_pos]

    if liste_y==sorted(liste_y) or liste_y==reversed(sorted(liste_y)):      #Si la liste y est déjà triée de manière croissante ou décroissante:
                                                                            #L'utilisateur a dessiné de haut en bas ou de bas en haut.
        liste_pics,l_croissance=croissance(liste_x)                         #On reprend notre fonction croissance pour connaître les variations de la liste x
        nb_pics=len(liste_pics)                                             #liste_pics est la liste des indices des extremums, l_croissance est la liste des variations, nb_pics est le nombre d'extremums
        if nb_pics==1:                                                      #S'il y a un extremum dans la liste x, cela veut dire que l'utilisateur a changé de direction une seule fois.
            if r_droite(liste_pos[:liste_pics[0]])[0] and r_droite(liste_pos[liste_pics[0]:])[0]:   #On teste si les deux parties de part et d'autre du seul pic sont des traits avec notre fonction r_droite. Le [0] permet de ne prendre que le booléen renvoyé par la fonction.
                if l_croissance==[True,False]:                              #Si la liste des x est croissante puis décroissante:
                    return "droite",liste_pos[liste_pics[0]]                #L'utilisateur a fait des droites vers la droite/bas puis vers la gauche/bas : il s'agit bien d'un angle ves la droite : On renvoie "droite" puis l'extremum.
                elif l_croissance==[False,True]:                            #Si la liste des x est croissante puis décroissante:
                    return "gauche",liste_pos[liste_pics[0]]                #L'utilisateur a fait des droites vers la gauche/bas puis vers la droite/bas : il s'agit bien d'un angle ves la gauche : On renvoie "gauche" puis l'extremum.
    
                                
    if liste_x==sorted(liste_x) or liste_x==reversed(sorted(liste_x)):      #Pour le haut et le bas, il s'agit du même raisonnement mais les x et y ont été échangés.

        liste_pics,l_croissance=croissance(liste_y)
        nb_pics=len(liste_pics)

        if nb_pics==1:
            if r_droite(liste_pos[:liste_pics[0]])[0] and r_droite(liste_pos[liste_pics[0]:])[0]:
                if l_croissance==[True,False]:
                    return "bas",liste_pos[liste_pics[0]]
                elif l_croissance==[False,True]:
                    return "haut",liste_pos[liste_pics[0]]

    
    return False,None   #Si rien n'a été renvoyé, on peut revoyer False et None.



def r_eclair(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie un booléen s'il s'agit a peu près d'un eclair
    Stratégie utilisée : Regarder les variations de x et y, puis réutiliser la fonction de reconnaissance r_droite pour vérifier si les traits sont droits
    Il y a deux moyens de faire un éclair : descendre vers la gauche, monter vers la droite puis descendre vers la gauche, ou toujours descendre en faisant gauche/droite/gauche
    """    
    liste_x=[i[0] for i in liste_pos]                                       #On parcours la liste pour avoir seulement les x et les y dans une liste
    liste_y=[i[1] for i in liste_pos]

    liste_pics_x,l_croissance_x= croissance(liste_x)                        #On reprend notre fonction croissance pour connaître les variations de la liste x
    nb_pics_x= len(liste_pics_x)

    liste_pics_y,l_croissance_y= croissance(liste_y)                        #On reprend notre fonction croissance pour connaître les variations de la liste y
    nb_pics_y= len(liste_pics_y)



    if nb_pics_x==2:                                                        #L'eclair se fait en allant à gauche, puis à droite, puis à gauche : il y a 2 pics.
        if l_croissance_x==[False,True,False]:
            if r_droite(liste_pos[:liste_pics_x[0]])[0] and r_droite(liste_pos[liste_pics_x[0]:liste_pics_x[1]])[0] and r_droite(liste_pos[liste_pics_x[1]:])[0]:   #On sépare le dessin en 3 parties grâce aux extremums et on verifie si chaque partie est bien à peut près une droite de la même manière que pour l'angle
                if l_croissance_y==[True] or l_croissance_y==[True, False,True]:    #On teste maintenant les y : [True] montre que le trait ne fait que descendre, [True, False,True] montre que le trait a descendu puis monté puis redescendu
                    return True                                             #Si toutes ses conditions sont vérifiées, on retourne True

    return False                                                            #Si rien n'a été renvoyé, on peut revoyer False

def r_cercle(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie un booléen indiquant s'il s'agissait à peu près d'un cercle, et un tuple possèdant le centre et le rayon du cercle.
    Stratégie utilisée :  Capturer les distances de chaque point avec le centre et vérifier qu'il n'y a pas de grandes différences entre elles.
    """    
    liste_x=[i[0] for i in liste_pos]                                       #On parcours la liste pour avoir seulement les x et les y dans une liste
    liste_y=[i[1] for i in liste_pos]                                                                            
                                                                            
    for point in liste_pos:                                                 #On parcours la liste
            if point[0]==max(liste_x):                                      #Si l'abscisse du point est la maximale, il s'agit du point le plus à droite.
                a=point                                                     #On capture ce point dans la variable a
            if point[1]==min(liste_y):                                      #On fait cela pour les points les plus en haut, a gauche et en bas du dessin
                b=point                                                     #Voir 1) dans l'annexe pour un schéma de la construction
            if point[0]==min(liste_x):
                c=point
            if point[1]==max(liste_y):
                d=point
    centre=interdiagonalequadri(a,b,c,d)                                    #En trouvant les coordonnées de l'intersection des diagonales de abcd, on a une approximation du centre.

    if centre!="Erreur":                                                    #On ne travaille pas si le calcul précédent a intercepté une erreur
        liste_distance=[distance(point,centre) for point in liste_pos]      #La liste des distances se fait grâce à un parcours de la liste des points et la fonction distance
        
        if max(liste_distance)<=2*min(liste_distance):                      #La valeur du coefficient a été choisie arbitrairement après plusieurs tests.
            if distance(liste_pos[0],liste_pos[-1])<30:                     #On teste également si l'utilisateur a bien fermé le cercle en regardant la distance entre le premier et le dernier point. La valeur a également été choisie arbitrairement après plusieurs tests.
                return True,(centre,max(liste_distance))                    #On peut retourne True et les valeurs.

    return False,(None,None)                                                #Si rien n'a été renvoyé:
    
def r_ellipse(liste_pos):
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie un booléen indiquant s'il s'agissait à peu près d'une ellipse, et un tuple possèdant le centre et les grand et petit rayons de l'ellipse.
    Stratégie utilisée :  Capturer les sommes des distances entre chaque point et les foyers et vérifier qu'il n'y a pas de grandes différences entre elles.
    """    
    liste_x=[i[0] for i in liste_pos]                                       #On parcours la liste pour avoir seulement les x et les y dans une liste
    liste_y=[i[1] for i in liste_pos]

                                                                            #On trouve le centre de la même manière que le cercle
    for point in liste_pos:
            if point[0]==max(liste_x):
                a=point
            if point[1]==min(liste_y):
                b=point
            if point[0]==min(liste_x):
                c=point
            if point[1]==max(liste_y):
                d=point
    centre=interdiagonalequadri(a,b,c,d)

    if centre!='Erreur':

        axe_x=droite(a,c)                                                   #On crée le segement [AC] avec notre fonction droite

        d_a=distance(centre,a)                                              #On calcule les demi-axes de l'ellipse
        d_b=distance(centre,b)                                              
        if d_a<d_b:                                                         #Les calculs qui vont suivre ne fonctionnent que l'ellipse est allongée. Si ce n'est pas le cas, on échange les deux valeurs
            d_a,d_b=d_b,d_a

        d_c=math.sqrt(d_a**2-d_b**2)                                        #d_c représente la distance entre le centre et les foyers

        foyers=[i for i in axe_x if abs(distance(centre,i)-d_c)<3]          #foyers est la liste de chaque point qui appartiennent à [AC] et qui ont une distance avec le centre environ égale à d_c, à 3 pixels près
        try:
            f1,f2=foyers[0],foyers[-1]                                      #On selectionne le premier et le dernier point pour avoir les deux foyers
        except IndexError:                                                  #Si on n'a pas trouvé de foyer, on pose les foyers à (0,0)
            f1,f2=(0,0),(0,0)

        liste_d_somme=[distance(point,f1)+distance(point,f2) for point in liste_pos]    #Le raisonnement est le même que pour le cercle:
                                                                                        #Il faut que les sommes des distances entre chaque point et les foyers soient à peu près égales
        if max(liste_d_somme)<=2*min(liste_d_somme):
            if distance(liste_pos[0],liste_pos[-1])<30:
                return True,(centre,(d_a,d_b))

    return False,(None,(None,None))



def r_tp(liste_pos,rect_perso,liste_tp):
    
    """La fonction prend en paramètre la liste des points du dessin.
    Elle renvoie l'indice du rectangle de téléportation. Sinon, retourne -1.
    Stratégie utilisée : Verifier que le premier point du trait est dans le rectangle de teleportation, et que le dernier est dans le rectangle du personnage, ou vice versa.
    """

    deb=liste_pos[0]                        #On pose deb et fin pour le premier et le dernier point de la liste 
    fin=liste_pos[-1]

    if rect_perso.collidepoint(deb):        #On teste si le premier point collisionne avec le rectangle du personnage
        for i,rect in enumerate(liste_tp):  #On parcours la liste_tp avec les indices
            if rect.collidepoint(fin):      #On teste si le dernier point collisionne avec le rectangle de teleportation
                return i                    #On retourne l'indice de ce rectangle
                            
    elif rect_perso.collidepoint(fin):      #Même raisonnement en changeant deb et fin
        for i,rect in enumerate(liste_tp):
            if rect.collidepoint(deb):
                return i
            
    return -1                               #Si rien n'a été renvoyé, on retourne -1

#--------------------------------------------Autres fonctions-------------------------------------------------------
def musique(music):
    """La fonction prend en paramètre le chemin vers le fichier audio. Son intéret est d'arreter la musique actuelle et de lancer une nouvelle.
    """
    pygame.mixer.stop()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()

