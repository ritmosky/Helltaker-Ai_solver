# Modélisation STRIPS

## Les Prédicats

| Prédicats             | Fluent ? |
|:----------------------|:--------:|
| wall(X,Y)             |   Non    |
| helltaker(X,Y)        | **Oui**  |
| demon(X,Y)            |   Non    |
| rock(X,Y)             | **Oui**  |
| skeleton(X,Y)         | **Oui**  |
| counter(X)            | **Oui**  |
| lock(X,Y,S)           | **Oui**  |
| key(X,Y)              |   Non    |
| openTrap(X,Y)         |   Non    |
| trap(X,Y,S)           | **Oui**  |
| plusOne(X,X')         |   Non    |

## Initialisation

Nous nous servirons du niveau 6 de Helltaker comme modèle pour l'initialisation du problème. Seul l'emplacement des objets sur la grille devrait changer d'un niveau à l'autre.
    
    Init(
        demon(6,1),
        helltaker(3,8),
        counter(43),
        lock(5,2,0),
        key(4,6),
        trap(2,5,0),trap(3,5,0),
        skeleton(2,4), skeleton(6,3),
        rock(6,2), rock(4,3), rock(4,4), rock(5,4), rock(3,5), rock(2,7), rock(3,7), rock(4,7),
        wall(5,0), wall(6,0), wall(4,1), wall(7,1), wall(1,2), wall(2,2), wall(3,2), wall(4,2), wall(8,2), wall(1,3), wall(7,3), wall(1,4), wall(3,4), wall(8,4), 
        wall(1,5), wall(6,5), wall(7,5), wall(0,6), wall(5,6), wall(6,6), wall(1,7), wall(5,7), wall(1,8), wall(5,8), wall(2,9), wall(3,9), wall(4,9),
        plusOne(-1,0), 
        plusOne(0,1), plusOne(1,2), plusOne(2,3), plusOne(3,4), plusOne(4,5), plusOne(5,6), plusOne(6,7), plusOne(7,8), plusOne(8,9), plusOne(9,10), 
        plusOne(10,11), plusOne(11,12), plusOne(12,13), plusOne(13,14), plusOne(14,15), plusOne(15,16), plusOne(16,17), plusOne(17,18), plusOne(18,19), plusOne(19,20), 
        plusOne(20,21), plusOne(21,22), plusOne(22,23), plusOne(23,24), plusOne(24,25), plusOne(25,26), plusOne(26,27), plusOne(27,28), plusOne(28,29), plusOne(29,30), 
        plusOne(30,31), plusOne(31,32), plusOne(32,33), plusOne(33,34), plusOne(34,35), plusOne(35,36), plusOne(36,37), plusOne(37,38), plusOne(38,39), plusOne(39,40), 
        plusOne(40,41), plusOne(41,42), plusOne(42,43)
    )

## But

Le but est d'atteindre une case adjacente à la case démone. Nous pouvons le modéliser comme ceci :

    But(
        demon(X,Y),
        plusOne(Y,H), plusOne(B,Y), plusOne(X,D), plusOne(G,X),
        (helltaker(X,H) | helltaker(X,B) | helltaker(D,Y) | helltaker(G,Y))
    )
    
## Actions

Beaucoup d'actions ont dû être modélisées. En effet, comme il est impossible d'utiliser le "ou" logique en STRIPS, nous avons modélisé des actions similaires dont une précondition change et implique un effet légèrement différent.

Pour le moment, le changement d'état des pièges à ours qui s'ouvrent et se ferment au fil des actions réalisées par le joueur n'a pas été modélisé dans les actions suivantes.

### Les déplacements simples :
Tout d'abord, nous modéliserons les actions de déplacement de Helltaker. En effet, le personnage peut se déplacer sur une case vide ou un piège non actif de manière horizontal et vertical. Le compteur sera alors décrémenté d'un point.

    goUp(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,0),trap(UX,UY,0), plusOne(Y,Y'),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',0),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',0), -counter(-1)
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goDown(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,0),trap(UX,UY,0), plusOne(Y',Y),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',0),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',0), -counter(-1)
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    goLeft(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,0),trap(UX,UY,0), plusOne(X',X),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,0),-key(X',Y),-openTrap(X',Y),-trap(X',Y,0), -counter(-1)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    goRight(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,0),trap(UX,UY,0), plusOne(X,X'),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,0),-key(X',Y),-openTrap(X',Y),-trap(X',Y,0), -counter(-1)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

### Les déplacements d'objets :
Ensuite nous modélisons le déplacement des objets, c'est-à-dire des rochers et des squelettes. Ainsi il faut vérifier que la case adjacente à Helltaker correspond bien à un objet et que la case suivante à l'objet ne soit ni un autre objet ni un mur. Le personnage ne bouge pas lors de ce type d'actions.

    pushRockUp(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushRockDown(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockLeft(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockRight(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)



    pushSkeletonUp(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushSkeletonDown(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonLeft(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonRight(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

### L'élimination des squelettes :
Les actions qui suivent modélisent l'élimination des ennemis : il s'agit également de pousser un squelette, mais cette fois ci un mur ou un rocher est adjacent au squelette ce qui aura pour effet de le faire disparaitre et non pas de le déplacer.

    wallKillUp(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillUp(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillDown(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillDown(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillLeft(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillLeft(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillRight(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillRight(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

### La gestion de la clef et du cadenas :
Pour la gestion des clefs et des cadenas, nous avons considéré qu'une seule clef et qu'un seul cadenas au maximum ne pouvait exister par niveau. Helltaker doit utiliser ces actions pour passer sur une case clef, ce qui fera passer le cadenas de l'état fermé (0) à ouvert (1).

    obtainKeyUp(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), lock(A,B,0), counter(C), -counter(-1), plusOne(Y,Y'), key(X,Y')
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    obtainKeyDown(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), lock(A,B,0), counter(C), -counter(-1), plusOne(Y',Y), key(X,Y')
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    obtainKeyLeft(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), lock(A,B,0), counter(C), -counter(-1), plusOne(X',X), key(X',Y)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    obtainKeyRight(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), lock(A,B,0), counter(C), -counter(-1), plusOne(X,X'), key(X',Y)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

### Les pièges à ours :
Nous devons ensuite modéliser les déplacements sur les pièges à ours, ceux qui restent ouverts tout au long du niveau et ceux qui sont ouverts à l'instant ou Helltaker se déplace sur eux. Le compteur se décrémente ici de deux.

    goUpOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goDownOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goLeftOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goRightOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)


    goUpOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), -rock(X,Y'), -skeleton(X,Y'), trap(X,Y',0)        
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goDownOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), -rock(X,Y'), -skeleton(X,Y'), trap(X,Y',0)        
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goLeftOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), -rock(X',Y), -skeleton(X',Y), trap(X',Y,0)        
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    goRightOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), -rock(X',Y), -skeleton(X',Y), trap(X',Y,0)        
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

De plus, lorsque Helltaker est sur un piège à ours actif et qu'il pousse un objet ou tue un ennemi, il restera sur cette case. Le compteur devra donc décrémenter de deux points en conséquence.

    pushRockUpWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushRockDownWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockLeftWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockRightWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushSkeletonUpWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushSkeletonDownWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonLeftWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonRightWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillUpWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y),  counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillUpWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillDownWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillDownWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillLeftWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillLeftWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillRightWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillRightWhileOnOpenTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)


    pushRockUpWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushRockDownWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockLeftWhileOnTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushRockRightWhileOnTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushSkeletonUpWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    pushSkeletonDownWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonLeftWhileOnTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)
    
    pushSkeletonRightWhileOnTrap(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillUpWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0),  counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillUpWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillDownWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillDownWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillLeftWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillLeftWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    wallKillRightWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

    rockKillRightWhileOnTrap(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,0),trap(UX,UY,0), trap(X,Y,0), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,0), -trap(UX,UY,0), trap(TX,TY,1), trap(UX,UY,1)

Pour terminer la gestion des pièges qui s'ouvrent et se ferment, il a fallu intégrer une nouvelle précondition pour pouvoir ajouter aux effets le bon changement d'état. C'est pourquoi il a fallu le double d'actions : une action à réaliser lorsque les pièges sont ouverts pour pouvoir les fermer dans les effets, et une autre à réaliser lorsqu'ils sont fermés pour pouvoir ensuite les ouvrir.

Les seules actions que nous n'avons pas besoin de modéliser deux fois pour changer l'état des pièges sont celles qui impliquent de rester sur un piège qui va s'ouvrir. En effet, ces actions ne s'appliquent uniquement lorsque Helltaker est déjà sur un piège fermé et qui s'ouvrira donc à sa prochaine action. Cette condition rend inutile la modélisation des deux cas d'état des pièges.

    goUpWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,1),trap(UX,UY,1), plusOne(Y,Y'),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',0),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',0), -counter(-1)
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    goDownWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,1),trap(UX,UY,1), plusOne(Y',Y),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',0),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',0), -counter(-1)
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    goLeftWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,1),trap(UX,UY,1), plusOne(X',X),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,0),-key(X',Y),-openTrap(X',Y),-trap(X',Y,0), -counter(-1)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    goRightWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y), counter(C),trap(TX,TY,1),trap(UX,UY,1), plusOne(X,X'),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,0),-key(X',Y),-openTrap(X',Y),-trap(X',Y,0), -counter(-1)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushRockUpWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushRockDownWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushRockLeftWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushRockRightWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushSkeletonUpWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushSkeletonDownWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushSkeletonLeftWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushSkeletonRightWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillUpWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillUpWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillDownWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillDownWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillLeftWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillLeftWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillRightWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillRightWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), -openTrap(X,Y), -trap(X,Y,0), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    obtainKeyUpWithChangingTrapOpen(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), lock(A,B,0), counter(C), -counter(-1), plusOne(Y,Y'), key(X,Y')
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    obtainKeyDownWithChangingTrapOpen(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), lock(A,B,0), counter(C), -counter(-1), plusOne(Y',Y), key(X,Y')
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    obtainKeyLeftWithChangingTrapOpen(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), lock(A,B,0), counter(C), -counter(-1), plusOne(X',X), key(X',Y)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    obtainKeyRightWithChangingTrapOpen(X,Y,A,B,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), lock(A,B,0), counter(C), -counter(-1), plusOne(X,X'), key(X',Y)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), lock(A,B,1), -lock(A,B,0), plusOne(C',C), counter(C'), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    goUpOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    goDownOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    goLeftOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    goRightOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition :  helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushRockUpWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushRockDownWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushRockLeftWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushRockRightWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushSkeletonUpWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    pushSkeletonDownWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',1), -lock(X,Y'',0)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushSkeletonLeftWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)
    
    pushSkeletonRightWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY) 
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,1), -lock(X'',Y,0)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillUpWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y),  counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillUpWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillDownWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillDownWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillLeftWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillLeftWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    wallKillRightWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)

    rockKillRightWhileOnOpenTrapWithChangingTrapOpen(X,Y,C,TX,TY,UX,UY)
        Precondition : helltaker(X,Y),trap(TX,TY,1),trap(UX,UY,1), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), -trap(TX,TY,1), -trap(UX,UY,1), trap(TX,TY,0), trap(UX,UY,0)