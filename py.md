

Pour effectuer une recherche d’états dans un labyrinthe :
- dans votre terminal, placez vous dans le dossier << Implementation/Python >> du projet 
- exécuter >> python helltaker_plan.py level_txt_path <<


NB: les labyrinthes étant dans le dossier << Implementation/levels >> du projet, level_txt_path doit 
commencer par : '../levels/'

Exemple d’exécution:

python helltaker_plan.py ../levels/level7.txt
python helltaker_plan.py ../levels/tests/traps1.txt
python helltaker_plan.py ../levels/tests/extras/trapsUUU.txt


Si il se trouve que l’algorithme ne trouve pas de plan alors qu’il y’en a un, le problème pourrait être 
résolu en se rendant dans le programme << main >> du fichier helltaker_plan.py puis changer le dernier 
argument << choice >> de la fonction < search >> pour le mettre à 1.
