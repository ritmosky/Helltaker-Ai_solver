# Modélisation STRIPS

## Les Prédicats

Prédicats | Fluent ?
 :--- | :---: 
wall(X,Y) | Non
helltaker(X,Y) | **Oui**
demon(X,Y) | Non
rock(X,Y) | **Oui**
skeleton(X,Y) | **Oui**
counter(X,Y) | **Oui**
lock(X,Y) | 
key(X,Y) | 
trap(X,Y,S) | **Oui**
up(X,Y) | Non
down(X,Y) | Non
right(X,Y) | Non
left(X,Y) | Non

## Initialisation

Nous nous servirons du niveau ... de Helltaker comme modèle pour l'initialisation du problème. Seul l'emplacement des objets sur la grille devrait changer d'un niveau à l'autre.

## But

Le but est d'atteindre une case adjacente à la case démone. Nous pouvons le modéliser comme ceci :

    But(
        demon(X,Y),
        up(Y,H), down(Y,B), right(X,D),left(X,G),
        (helltaker(X,H) | helltaker(X,B) | helltaker(D,Y) | helltaker(G,Y))
    )


## Actions

Quinze actions sont à modéliser au total : quatre pour les déplacements de Helltaker, quatre pour pousser les rochers, quatre pour pousser les squelettes, une pour obtenir une clef, une pour ouvrir un cadenas et une autre pour passer sur un piège à ours.