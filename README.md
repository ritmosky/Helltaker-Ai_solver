# Helltaker-Ai_solver



**Description du sujet**

L’objectif de ce projet est de créer différentes IA capables de jouer à la partie puzzle du jeu Helltaker(jeu de la famille de Sokoban).
Pour ce faire, nous implémenterons différentes méthodes tout en les décrivant et en les comparant expérimentalement.




* PARTIE I : Représentation et modélisation du problème en STRIPS et en Prolog 

    - Mettre en exergue les principales différences avec Sokoban
    


* PARTIE II : Implémentation 

     - SATPLAN pout la réécriture en SAT du problème de planification
     - Python pour la recherche dans un espace d’état



NOTA BENE : 

Le format de réponse attendue pour le programme est le suivant : hhbgdbbgh
Ceci correspond à une simplification des actions (h = haut, b = bas, d = droite, g = gauche)



QUELQUES LIENS 

* Helltaker sur wikipedia : https://fr.wikipedia.org/wiki/Helltaker
* Helltaker sur steam: https://store.steampowered.com/app/1289310/Helltaker/
* Télécharger Helltaker sur le site du développeur sans avoir à installer steam : https://vanripper.itch.io/helltaker
* Description SATPLAN : https://en.wikipedia.org/wiki/Satplan

## Architecture de notre archive
Le rapport se trouve à la racine du projet.

Le dossier Modelisation contient deux fichiers markdown : l'un pour la modélisation complète en STRIPS et le second pour un récapitulatif des règles que nous avons déduites du jeu Helltaker.

Le dossier Implementation contient nos programmes pour les deux méthodes implémentées. Vous y trouverez trois sous-dossier : 
* levels, contient l'ensemble des cartes des niveaux de Helltaker et des cartes de tests
* ASP, contient l'implémentation en ASP ainsi que les scripts python pour exécuter la méthode
* Python, contient l'implémentation de la recherche dans un espace d'état

## Lancement du programme python

Pour effectuer une recherche d’états dans un labyrinthe :
- dans votre terminal, placez vous dans le dossier << Implementation/Python >> du projet
- exécuter >> python helltaker_plan.py level_txt_path <<


NB: les labyrinthes étant dans le dossier << Implementation/levels >> du projet, level_txt_path doit
commencer par : '../levels/'

*Exemple d’exécution:*

python helltaker_plan.py ../levels/level7.txt

python helltaker_plan.py ../levels/tests/traps1.txt

python helltaker_plan.py ../levels/tests/extras/trapsUUU.txt


Si il se trouve que l’algorithme ne trouve pas de plan alors qu’il y’en a un, le problème pourrait être
résolu en se rendant dans le programme << main >> du fichier helltaker_plan.py puis changer le dernier
argument << choice >> de la fonction < search >> pour le mettre à 1.

## Lancement du programme ASP

Il suffit d'executer le fichier "helltaker_plan.py" avec comme argument le nom du fichier du niveau souhaité.
Assurez vous d'avoir clingo dans votre environnement python.

