# Modélisation STRIPS

## Les Prédicats

| Prédicats      | Fluent ? |
|:---------------|:--------:|
| wall(X,Y)      |   Non    |
| helltaker(X,Y) | **Oui**  |
| demon(X,Y)     |   Non    |
| rock(X,Y)      | **Oui**  |
| skeleton(X,Y)  | **Oui**  |
| counter(X)     | **Oui**  |
| lock(X,Y,S)    | **Oui**  |
| key(X,Y)       |   Non    |
| openTrap(X,Y)  |   Non    |
| trap(X,Y,S)    | **Oui**  |
| plusOne(X,X')  |   Non    |

## Initialisation

Nous nous servirons du niveau 6 de Helltaker comme modèle pour l'initialisation du problème. Seul l'emplacement des objets sur la grille devrait changer d'un niveau à l'autre.
    
    Init(
        demon(6,1),
        helltaker(3,8),
        counter(43),
        lock(5,2,F),
        key(4,6),
        trap(2,5,F),trap(3,5,F),
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

Trente-deux actions sont à modéliser au total : quatre pour les déplacements de Helltaker, quatre pour pousser les rochers, quatre pour pousser les squelettes, quatre pour tuer les squelettes, quatre pour obtenir une clef, quatre pour ouvrir un cadenas, quatre pour passer sur un piège à ours ouvert et (quatre autres pour passer sur un piège à ours fermé = pousser objet sur trap).

### Les déplacements simples :
    goUp(X,Y,C)
        Precondition : helltaker(X,Y), counter(C), plusOne(Y,Y'),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',F),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',O), -counter(-1)
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C)
    
    goDown(X,Y,C)
        Precondition : helltaker(X,Y), counter(C), plusOne(Y',Y),-wall(X,Y'),-demon(X,Y'),-rock(X,Y'),-skeleton(X,Y'),-lock(X,Y',F),-key(X,Y'),-openTrap(X,Y'),-trap(X,Y',O), -counter(-1)
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C)

    goLeft(X,Y,C)
        Precondition : helltaker(X,Y), counter(C), plusOne(X',X),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,F),-key(X',Y),-openTrap(X',Y),-trap(X',Y,O), -counter(-1)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C)

    goRight(X,Y,C)
        Precondition : helltaker(X,Y), counter(C), plusOne(X,X'),-wall(X',Y),-demon(X',Y),-rock(X',Y),-skeleton(X',Y),-lock(X',Y,F),-key(X',Y),-openTrap(X',Y),-trap(X',Y,O), -counter(-1)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), counter(C'), -counter(C)

### Les déplacements d'objets :
    pushRockUp(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    pushRockDown(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), counter(C'), -counter(C)
    
    pushRockLeft(X,Y,C) 
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C)
    
    pushRockRight(X,Y,C) 
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), counter(C'), -counter(C)



    pushSkeletonUp(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    pushSkeletonDown(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)
    
    pushSkeletonLeft(X,Y,C) 
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)
    
    pushSkeletonRight(X,Y,C) 
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)

### L'élimination des squelettes :
    wallKillUp(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    rockKillUp(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    wallKillDown(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    rockKillDown(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), counter(C'), -counter(C)

    wallKillLeft(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)

    rockKillLeft(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)

    wallKillRight(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)

    rockKillRight(X,Y,C)
        Precondition : helltaker(X,Y), -openTrap(X,Y), -trap(X,Y,F), counter(C), -counter(-1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), counter(C'), -counter(C)

### La gestion de la clef et du cadenas :
    obtainKeyUp(X,Y,A,B,C)
        Precondition : helltaker(X,Y), lock(A,B,F), counter(C), -counter(-1), plusOne(Y,Y'), key(X,Y')
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,O), -lock(A,B,F), plusOne(C',C), counter(C'), -counter(C)
    
    obtainKeyDown(X,Y,A,B,C)
        Precondition : helltaker(X,Y), lock(A,B,F), counter(C), -counter(-1), plusOne(Y',Y), key(X,Y')
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), lock(A,B,O), -lock(A,B,F), plusOne(C',C), counter(C'), -counter(C)

    obtainKeyLeft(X,Y,A,B,C)
        Precondition : helltaker(X,Y), lock(A,B,F), counter(C), -counter(-1), plusOne(X',X), key(X',Y)
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), lock(A,B,O), -lock(A,B,F), plusOne(C',C), counter(C'), -counter(C)

    obtainKeyRight(X,Y,A,B,C)
        Precondition : helltaker(X,Y), lock(A,B,F), counter(C), -counter(-1), plusOne(X,X'), key(X',Y)
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), lock(A,B,O), -lock(A,B,F), plusOne(C',C), counter(C'), -counter(C)

### Les pièges à ours :
Déplacements sur trap ouvert

    goUpOnOpenTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    goDownOnOpenTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), -rock(X,Y'), -skeleton(X,Y'), openTrap(X,Y')        
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    goLeftOnOpenTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    goRightOnOpenTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), -rock(X',Y), -skeleton(X',Y), openTrap(X',Y)        
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)


    goUpOnTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), -rock(X,Y'), -skeleton(X,Y'), trap(X,Y',F)        
        Effect : plusOne(Y,Y'), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y',O), -trap(X,Y',F)
    
    goDownOnTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), -rock(X,Y'), -skeleton(X,Y'), trap(X,Y',F)        
        Effect : plusOne(Y',Y), helltaker(X,Y'), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y',O), -trap(X,Y',F) 
    
    goLeftOnTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), -rock(X',Y), -skeleton(X',Y), trap(X',Y,F)        
        Effect : plusOne(X',X), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X',Y,O), -trap(X',Y,F)
    
    goRightOnTrap(X,Y,C)
        Precondition :  helltaker(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), -rock(X',Y), -skeleton(X',Y), trap(X',Y,F)        
        Effect : plusOne(X,X'), helltaker(X',Y), -helltaker(X,Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X',Y,O), -trap(X',Y,F)  


Pousser/Rester sur un piège qui s'ouvre/se ferme

    pushRockUpWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    pushRockDownWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    pushRockLeftWhileOnOpenTrap(X,Y,C) 
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    pushRockRightWhileOnOpenTrap(X,Y,C) 
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    pushSkeletonUpWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    pushSkeletonDownWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    pushSkeletonLeftWhileOnOpenTrap(X,Y,C) 
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)
    
    pushSkeletonRightWhileOnOpenTrap(X,Y,C) 
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    wallKillUpWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y),  counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    rockKillUpWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    wallKillDownWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    rockKillDownWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    wallKillLeftWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    rockKillLeftWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    wallKillRightWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)

    rockKillRightWhileOnOpenTrap(X,Y,C)
        Precondition : helltaker(X,Y), openTrap(X,Y), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C)


    pushRockUpWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), rock(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    pushRockDownWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), rock(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), rock(X,Y''), -rock(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)
    
    pushRockLeftWhileOnTrap(X,Y,C) 
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), rock(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)
    
    pushRockRightWhileOnTrap(X,Y,C) 
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), rock(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), rock(X'',Y), -rock(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    pushSkeletonUpWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y,Y'), plusOne(Y',Y''), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    pushSkeletonDownWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), -wall(X,Y''), -demon(X,Y''), -rock(X,Y''), -skeleton(X,Y''), -lock(X,Y'',O), -lock(X,Y'',F)
        Effect : plusOne(Y',Y), plusOne(Y'',Y'), skeleton(X,Y''), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)
    
    pushSkeletonLeftWhileOnTrap(X,Y,C) 
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X',X), plusOne(X'',X'), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)
    
    pushSkeletonRightWhileOnTrap(X,Y,C) 
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), -wall(X'',Y), -demon(X'',Y), -rock(X'',Y), -skeleton(X'',Y), -lock(X'',Y,O), -lock(X'',Y,F)
        Effect : plusOne(X,X'), plusOne(X',X''), skeleton(X'',Y), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    wallKillUpWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F),  counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), wall(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    rockKillUpWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y,Y'), skeleton(X,Y'), plusOne(Y',Y''), rock(X,Y'')
        Effect : plusOne(Y,Y'), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    wallKillDownWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), wall(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    rockKillDownWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(Y',Y), skeleton(X,Y'), plusOne(Y'',Y'), rock(X,Y'')
        Effect : plusOne(Y',Y), -skeleton(X,Y'), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    wallKillLeftWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), wall(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    rockKillLeftWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X',X), skeleton(X',Y), plusOne(X'',X'), rock(X'',Y)
        Effect : plusOne(X',X), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    wallKillRightWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), wall(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)

    rockKillRightWhileOnTrap(X,Y,C)
        Precondition : helltaker(X,Y), trap(X,Y,F), counter(C), -counter(-1), -counter(0), -counter(1), plusOne(X,X'), skeleton(X',Y), plusOne(X',X''), rock(X'',Y)
        Effect : plusOne(X,X'), -skeleton(X',Y), plusOne(C',C), plusOne(C'',C'), counter(C''), -counter(C), trap(X,Y,O)