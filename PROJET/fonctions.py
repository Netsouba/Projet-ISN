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
    Elle renvoie une liste de points qui appartiennent à la droite (AB):
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
    except ZeroDivisionError:
        return 'Erreur'


#--------------------------------Fonctions reconnaissance----------------------
def r_droite(liste_pos):
    acroissement=[]
    for i in range(len(liste_pos)-1):
        try:
            acroissement.append((liste_pos[i+1][1]-liste_pos[i][1])/(liste_pos[i+1][0]-liste_pos[i][0]))
        except ZeroDivisionError:
            pass


    ecart_type=calc_ecart_type(acroissement)


    if ecart_type<=1.5:
        return True,droite(liste_pos[0],liste_pos[-1])
    else:
        return False,None

def r_point(liste_pos):
    liste_distance=[distance(liste_pos[0],point) for point in liste_pos]
    moy= moyenne(liste_distance)
    if moy<=1:
        return True,liste_pos[0]
    else:
        return False,None


def r_angle(liste_pos):

    liste_x=[i[0] for i in liste_pos]
    liste_y=[i[1] for i in liste_pos]

    if liste_y==sorted(liste_y) or liste_y==reversed(sorted(liste_y)):

        liste_pics,l_croissance=croissance(liste_x)
        nb_pics=len(liste_pics)

        if nb_pics==1:
            if r_droite(liste_pos[:liste_pics[0]])[0] and r_droite(liste_pos[liste_pics[0]:])[0]:
                if l_croissance==[True,False]:
                    return "droite",liste_pos[liste_pics[0]]
                elif l_croissance==[False,True]:
                    return "gauche",liste_pos[liste_pics[0]]

    if liste_x==sorted(liste_x) or liste_x==reversed(sorted(liste_x)):

        liste_pics,l_croissance=croissance(liste_y)
        nb_pics=len(liste_pics)

        if nb_pics==1:
            if r_droite(liste_pos[:liste_pics[0]])[0] and r_droite(liste_pos[liste_pics[0]:])[0]:
                if l_croissance==[True,False]:
                    return "bas",liste_pos[liste_pics[0]]
                elif l_croissance==[False,True]:
                    return "haut",liste_pos[liste_pics[0]]


    return False,None



def r_eclair(liste_pos):

    liste_x=[i[0] for i in liste_pos]
    liste_y=[i[1] for i in liste_pos]

    liste_pics_x,l_croissance_x= croissance(liste_x)
    nb_pics_x= len(liste_pics_x)

    liste_pics_y,l_croissance_y= croissance(liste_y)
    nb_pics_y= len(liste_pics_y)



    if nb_pics_x==2:

        if r_droite(liste_pos[:liste_pics_x[0]])[0] and r_droite(liste_pos[liste_pics_x[0]:liste_pics_x[1]])[0] and r_droite(liste_pos[liste_pics_x[1]:])[0]:
            if l_croissance_x==[False,True,False]:
                if (nb_pics_y==0 and l_croissance_y==[True]) or (nb_pics_y==2 and l_croissance_y==[True, False,True]):
                    return True

    return False

def r_cercle(liste_pos):
    liste_x=[i[0] for i in liste_pos]
    liste_y=[i[1] for i in liste_pos]

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

    if centre!="Erreur":
        liste_distance=[distance(point,centre) for point in liste_pos]
        if max(liste_distance)<=2*min(liste_distance):

            if distance(liste_pos[0],liste_pos[-1])<30:
                return True,(centre,max(liste_distance))

    return False,(None,None)

def r_ellipse(liste_pos):

    liste_x=[i[0] for i in liste_pos]
    liste_y=[i[1] for i in liste_pos]


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

        axe_x=droite(a,c)

        d_a=distance(centre,a)
        d_b=distance(centre,b)
        if d_a<d_b:
            d_a,d_b=d_b,d_a

        d_c=math.sqrt(d_a**2-d_b**2)

        foyers=[i for i in axe_x if abs(distance(centre,i)-d_c)<3]
        try:
            f1,f2=foyers[0],foyers[-1]
        except IndexError:
            f1,f2=(0,0),(0,0)

        liste_d_somme=[distance(point,f1)+distance(point,f2) for point in liste_pos]

        if max(liste_d_somme)<=2*min(liste_d_somme):

            if distance(liste_pos[0],liste_pos[-1])<30:
                return True,(centre,(d_a,d_b))

    return False,(None,(None,None))





def r_arc_cercle(liste_pos):

    liste_x=[i[0] for i in liste_pos]
    liste_y=[i[1] for i in liste_pos]

    if liste_y==sorted(liste_y) or liste_y==reversed(sorted(liste_y)):

        liste_pics,l_croissance=croissance(liste_x)
        nb_pics=len(liste_pics)

        if nb_pics==1:

            if l_croissance==[True,False]:
                return "droite"
            elif l_croissance==[False,True]:
                return "gauche"



    return False


def r_tp(liste_pos,rect_perso,liste_tp):

    """ La liste retourne l'indice du rectangle de téléportation. Sinon, retourne -1
    """

    deb=liste_pos[0]
    fin=liste_pos[-1]

    if rect_perso.collidepoint(deb):
        for i,rect in enumerate(liste_tp):
            if rect.collidepoint(fin):
                return i
    elif rect_perso.collidepoint(fin):
        for i,rect in enumerate(liste_tp):
            if rect.collidepoint(deb):
                return i
    return -1















