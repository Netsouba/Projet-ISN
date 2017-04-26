import os
import pygame
from pygame.locals import *
import math
from copy import deepcopy
from constantes import *

#-----------------------------------Fontions maths--------------------------------
def moyenne(liste):
    try:
        return sum(liste)/len(liste)
    except:
        return 0
def milieu(point_a,point_b):
    ax,ay=point_a
    bx,by=point_b
    m=(ax+bx)/2,(ay+by)/2
    return m

def distance(point_a,point_b):
    return math.sqrt((point_b[0]-point_a[0])**2+(point_b[1]-point_a[1])**2)

def droite(point_a,point_b):
    if point_a[0]>point_b[0]:
        point_a,point_b=point_b,point_a
    ax,ay=point_a
    bx,by=point_b

    try:
        delta=(by-ay)/(bx-ax)
        liste_point=[(x,delta*(x-ax)+ay) for x in range(ax,bx)]

    except ZeroDivisionError:

        liste_point=[(ax,y) for y in range(ay,by,3)]

    return liste_point

def croissance(liste):
    """ Retourne les variations d'une liste (Minima+Maxima, Indices)"""

    liste_c=[]
    liste_p=[]
    croissant=None

    for i in range(len(liste)-1):
        if liste[i+1]>liste[i]:

            if croissant==None:
                liste_c.append(True)

            elif croissant==False:
                liste_p.append(i)

                liste_c.append(True)

            croissant=True

        elif liste[i+1]<liste[i]:

            if croissant==None:
                liste_c.append(False)
            elif croissant==True:
                liste_p.append(i)

                liste_c.append(False)

            croissant=False

    return liste_p,liste_c

def calc_ecart_type(liste):
    moyenne_l=moyenne(liste)
    l=[(i-moyenne_l)*(i-moyenne_l) for i in liste]
    return math.sqrt(sum(l))

def interdiagonalequadri(a,b,c,d):
    v_ac=(c[0]-a[0],c[1]-a[1])
    v_bd=(d[0]-b[0],d[1]-b[1])

##    eq_a={a[0]+v_ac[0]*t,
##          a[1]+v_ac[1]*t}
##    eq_b={b[0]+v_bd[0]*t,
##          b[1]+v_bd[1]*t}
##
##    a[0]+v_ac[0]*t=b[0]+v_bd[0]*k,
##    a[1]+v_ac[1]*t=b[1]+v_bd[1]*k
##
##    t=(b[0]+v_bd[0]*k-a[0])/v_ac[0],
##    a[1]+v_ac[1]*(b[0]+v_bd[0]*k-a[0])/v_ac[0]=b[1]+v_bd[1]*k
##
##    t=(b[0]+v_bd[0]*k-a[0])/v_ac[0],
##    a[1]+(v_ac[1]*b[0]-v_ac[1]*a[0])/v_ac[0]-b[1]=v_bd[1]*k-v_ac[1]*v_bd[0]*k/v_ac[0]
##
##    t=(b[0]+v_bd[0]*k-a[0])/v_ac[0],
##    k=(a[1]+(v_ac[1]*b[0]-v_ac[1]*a[0])/v_ac[0]-b[1])/(v_bd[1]-v_ac[1]*v_bd[0]/v_ac[0])

    try:
        x=b[0]+v_bd[0]*(a[1]+(v_ac[1]*b[0]-v_ac[1]*a[0])/v_ac[0]-b[1])/(v_bd[1]-v_ac[1]*v_bd[0]/v_ac[0])
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




#----------------------------Fonctions jeu--------------------------------------------























