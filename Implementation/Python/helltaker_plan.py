########## BIBLIOTHEQUES ##########


import sys
import os
import time
import numpy as np

from helltaker_utils import grid_from_file, check_plan
from collections import namedtuple
from typing import Tuple, Optional, Dict, Set, Callable, List


########## INITIALISATION ##########


Action = namedtuple('action',('verb','direction'))
actions = {a: frozenset({Action("move",a),Action("push",a)}) for a in 'hbdg'}

State = namedtuple('state',('hero','rocks','skeletons','slidingTraps','lock','counter'))


def set_state(
    pos: Tuple[int,int],
    rocks: Set,
    counter: int,
    skels: Set,
    slidTraps: Set,
    lock: Tuple[int,int,bool]
) -> Optional[Dict]:
    """
    la fonction génère un état conforme à notre représentation
    """
    return {'hero':pos,'rocks':rocks,'skeletons':skels,'slidingTraps':slidTraps,'lock':lock,'counter':counter}


def init(voc: Dict) -> State:
    """
    la fonction initialise l'état initial et les non fluents
    """
    return set_state(voc['hero'],voc['rocks'],voc['counter'],voc['skeletons'],voc['slidingTraps'],voc['lock']), {'goals':voc['goals'],'walls':voc['walls'],'key':voc['key'],'openTraps':voc['openTraps'],'dim':voc['dim']}


########## FONCTIONS INTERMEDIAIRES ##########


def is_in_grid(
    position: Tuple[int,int],
    map_rules: Dict
) -> bool:
    """ la fonction vérifie que la position
    se trouve bien dans la grille """
    x, y = position
    xmax, ymax = map_rules['dim']
    if x<0 or y<0 or x>xmax or y>ymax:
        return False
    return True


def free(
    position: Tuple[int,int],
    map_rules: Dict
) -> bool:
    """ la fonction représente toutes les cases
    accessibles du plateau """
    return not(position in map_rules['walls'])


def is_trapped(
    pos: Tuple[int,int],
    compt: int,
    slidTraps: Set,
    map_rules: Dict
) -> int:
    """ la fonction décrémente le compteur du héros lorsque celui ci se
    trouve sur un piège """
    if pos in map_rules['openTraps'] or (pos[0],pos[1],True) in slidTraps:
        return compt - 1
    return compt


def traps_slider(slidTraps: Set) -> Set:
    """ la fonction permet de permuter l'état des slidingTraps
    (en ouvert ou fermé) à chaque déplacement du héros """
    straps = []
    for st in slidTraps:
        posx, posy, bool = st
        st = (posx, posy, not bool)
        straps.append(st)
    return set(straps)


def one_step(
    position: Tuple[int,int],
    direction: Action
) -> Tuple[int,int]:
    """ la fonction retourne la position suivant une direction donnée
    (h,b,g,d) """
    i, j = position
    return {'d': (i,j+1), 'g': (i,j-1), 'h': (i-1,j), 'b': (i+1,j)}[direction]


def do(
    action: Action,
    state: State,
    map_rules: Dict
) -> Optional[State]:
    """ la fonction renvoit l'état succédant à létat courant, en fonction
    de l'action en paramètre """
    X0, cpt, rocks = state.hero, state.counter, state.rocks
    skels, sTraps, lock = state.skeletons, state.slidingTraps, state.lock
    X1 = one_step(X0, action.direction)
    if X0 == map_rules['key']:
        lock = (lock[0],lock[1],True)
    if lock and X1 == lock[0:2] and lock == (lock[0],lock[1],False):
        return None
    if action.verb == 'move' and is_in_grid(X1,map_rules) :
        if free(X1,map_rules) and not (X1 in rocks) and not (X1 in skels):
            cpt -= 1
            sTraps = traps_slider(sTraps)
            cpt = is_trapped(X1,cpt,sTraps,map_rules)
            for sk in skels:
                if is_trapped(sk,0,sTraps,map_rules):
                    skels = skels - {sk}
            if cpt < -1:
                return None
            else:
                return State(**set_state(X1,rocks,cpt,skels,sTraps,lock))
        else:
            return None
    if action.verb == 'push':
        X2 = one_step(X1, action.direction)
        sTraps = traps_slider(sTraps)
        # pour pousser un squelette
        if X1 in skels and free(X2,map_rules) and not (X2 in rocks) and not (X2 in skels) and is_trapped(X2,0,sTraps,map_rules) == 0 and not (X2 in map_rules['goals']):
            new_skels = skels - {X1}
            new_skels.add(X2)
            cpt = is_trapped(X0,cpt,sTraps,map_rules)
            return State(**set_state(X0,rocks,cpt-1,new_skels,sTraps,lock))
        # pour pousser une roche
        elif X1 in rocks and free(X2,map_rules) and not (X2 in rocks) and not (X2 in skels) and not (X2 in map_rules['goals']):
            if lock and X2 != lock[0:2] or not lock:
                new_rocks = rocks - {X1}
                new_rocks.add(X2)
                cpt = is_trapped(X0,cpt,sTraps,map_rules)
                return State(**set_state(X0,new_rocks,cpt-1,skels,sTraps,lock))
        # pour exploser un squelette
        elif X1 in skels:
            if is_trapped(X2,0,sTraps,map_rules)<0 or not(free(X2,map_rules)) or (X2 in rocks):
                return State(**set_state(X0,rocks,cpt-1,skels-{X1},sTraps,lock))
        else :
            return None
    return None


def succ(
    state: State,
    map_rules: Dict
) -> List[Tuple[State,Action]]:
    """ la fonction retourne la liste des successeurs de l'état courant
    suivant toutes les actions possibles """
    l = [(do(act,state,map_rules),d) for d in actions for act in actions[d]]
    return [(e,act) for e,act in l if e]


def suc(state):
    def succ1(
        state: State,
        map_rules: Dict
    ) -> List[Tuple[State,Action]]:
        """ la fonction retourne la liste des successeurs de l'état courant
        suivant toutes les actions possibles """
        l = [(do(act,state,map_rules),d) for d in actions for act in actions[d]]
        return [(e,act) for e,act in l if e]
    return succ1(state,map_rules)


########## ALGORITHME DE RECHERCHE INFORMÉE + PARCOURS EN LARGEUR ##########


def is_visited(
    state: State,
    visitedStates: Dict,
    choice: int=0
) -> bool:
    """ la fonction permet de vérifier si un
    état à déjà été visité (si elle se trouve
    dans le dico en paramètre) ou pas. Le paramètre
    choice est utilisé pour changer la façon dont la
    comparaison est effectuée, il en faut une autre
    pour résoudre level2 """
    for elem in visitedStates.values():
        if choice > 0 and state == elem[0]:
            return True
        if choice == 0 and state[0:5] == elem[0][0:5]:
            return True
    return False


def insert(
    state: State,
    states: List[State]
) -> List[State]:
    """ permet d'insérer les états en queue de file """
    states.append(state)
    return states


def remove(states: List[State]) -> Tuple[State,List[State]]:
    """ permet de retirer les états en tête de file """
    return states.pop(0), states


def goals(
    state: State,
    map_rules: Dict
) -> bool:
    """ permet de vérifier si l'état cournt est un état but """
    for s,action in succ(state,map_rules):
        if s.hero in map_rules['goals'] and state.counter>=0:
            return True
    return False


global keyFound
keyFound=False
def distance_M(
    s: State,
    map_rules: Dict
) -> int:
    """ permet de calculer la distance de Manhattan entre l'état
    courant et l'état solution. Si il ya une clé, la fonction
    prendra la clé comme but principale puis une fois qu'elle est
    récupérée elle s'interessera au démones """
    global keyFound
    dd = 1000
    x, y = s.hero
    if s.lock and s.lock[2] == False:
        xx, yy = map_rules['key']
        dd = abs(x - xx) + abs(y - yy)
        keyFound = False
    else:
        for xx,yy in map_rules['goals']:
            d = abs(x - xx) + abs(y - yy)
            if d < dd:
                dd = d
    if keyFound==True:
        for xx,yy in map_rules['goals']:
            d = abs(x - xx) + abs(y - yy)
            if d < dd:
                dd = d
    elif s.lock and s.hero == map_rules['key'] and not keyFound:
        dd = 0
        keyFound = True
    return dd


def heuristique(
    states_succ: List[State],
    map_rules: Dict
) -> List[State]:
    """ la fonction renvoit l'état ainsi que l'action suivant
    l'heuristique de la distance de Manhattan + le nombre de pas restant
    en ne prenant que les successeurs pour lesquels le compteur >= nombre
    de cases pour atteindre le but """
    nbCasesRest = [distance_M(state,map_rules) for state,act in states_succ]
    counters = [s.counter for s,a in states_succ]
    h = np.array(nbCasesRest) + np.array(counters)
    new = [j for i,j in sorted(zip(h,states_succ)) if j[0].counter>=0]
    return  [elem for elem in new if elem[0].counter+1 >= distance_M(elem[0],map_rules)]


def planGagnant(
    un_plan: str,
    state: State,
    map_rules: Dict,
    affichage: bool=False
) -> bool:
    """ fonction vérifie si un plan conduit à un état but """
    if un_plan == -1:
        return None
    if not check_plan(un_plan):
        return None
    if affichage:
        print('\n\n## << {} >> est un plan gagnant ? '.format(un_plan))
        print(state)
    s1 = state
    for d1 in un_plan:
        isDo = False
        for d2 in actions[d1]:
            if not isDo:
                if do(d2,s1,map_rules) is None:
                    continue
                else:
                    s1 = do(d2,s1,map_rules)
                    if affichage:
                        print('{} -> {}'.format(d1,s1))
                    isDo = True
            if isDo:
                continue
    if goals(s1,map_rules):
        if affichage:
            print("\n\t\t ***** plan gagnant *****")
        return True
    if not goals(s1,map_rules) and affichage:
        print("\n\t\t ***** plan perdant *****")
    return False


def toChemin(
    s_end: State,
    save: Dict,
    affichage: bool=False
) -> str:
    """ permet de reconstruire le chemin pour mener à la
    solution """
    if affichage:
        print('\n\n## Reconstruction du chemin')
    if s_end == None:
        if affichage:
            print("\n /!\ pas de solution possible /!\ \n")
        return ''
    s = s_end
    l = [(s_end,None)]
    ch = []
    b = True
    while b:
        for cur,pere,act in save.values():
            if cur == s:
                if pere == None:
                    b = False
                    break
                else:
                    l.append((pere,act))
                    s=pere
    l.reverse()
    for s,act in l:
        if affichage:
            print(s)
        if act == None:
            break
        ch.append(act)
    return ''.join(ch)


def search(
    s0: State,
    goals: Callable[[State, Dict],bool],
    succ: Callable[[State],List[Tuple[State,Action]]],
    remove: Callable[[List[State]],Tuple[State,List[State]]],
    insert: Callable[[State],List[State]],
    map_rules: Dict,
    choice: int=0
) -> Tuple[Optional[State],Dict]:
    """ fonction implémentant la recherche informée en largeur utilisée.
    L'argument choice sera >0 pour permettre de trouver la solution pour
    le level2 ref fonction is_visited"""
    l = [s0]
    save = {0: (s0,None,None)} #(state,pere,action)
    i = 1
    while l:
        s, l = remove(l)
        for s2,a in heuristique(succ(s,map_rules),map_rules):
            if not is_visited(s2,save,choice):
                save[i] = (s2,s,a)
                i += 1
                if goals(s2,map_rules):
                    return s2, save
                insert(s2,l)
    return None, save



########## MAIN ##########


def main():
    start = time.time()

    global map_rules

    # récupération du nom du fichier depuis la ligne de commande
    #file = '../levels/level1.txt'
    file = sys.argv[1]
    print('\n\n### {} execute la map \'{}\' ###\n'.format(sys.argv[0],file))
    choice = 0
    if file.find('level2.') > 0:
        choice = 1
    # récupération de la grille et de toutes les infos
    s0, map_rules = init(grid_from_file(file))
    s0 = State(**s0)

    # calcul du plan
    # Rajouter un argument True toChemin et planGagnant pour afficher les 2tats
    s_end, save = search(s0,goals,succ,remove,insert,map_rules,choice)
    plan = toChemin(s_end,save)
    planGagnant(plan,s0,map_rules)

    # affichage du résultat
    if plan == '':
        print("\n----- [KO], aucun plan -----\n".format(plan))
    elif check_plan(plan):
        print("\n----- [OK], plan = {} -----\n".format(plan))
        endT = time.time()
        print("----- Temps de résolution : {} sec -----\n\n".format(endT-start))
    else:
        print("[Err]", plan, file=sys.stderr)
        #sys.exit(2)


if __name__ == "__main__":
    main()
