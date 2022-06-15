"""
Ce module contient différentes fonction permettant de lire des fichiers Helltaker au format défini pour le projet et de vérifier des plans.
"""

from fileinput import filename
from pprint import pprint
import sys
from typing import List



model = {
'H': 'hero',
'D': 'goals',
'L': 'lock',
'#': 'walls',
'B': 'rocks',
'M': 'skeletons',
'K': 'key',
'S': 'openTraps',
'T': 'slidingTrapsF',  #piege ferme
'U': 'slidingTrapsT',  #piege ouvert
'O': 'openTrapsrocks',
'P': 'slidingTrapsFrocks',  #piege ferme
'Q': 'slidingTrapsTrocks'  #piege ouvert
}



def complete(m: List[List[str]], n: int):
    for l in m:
        for _ in range(len(l), n):
            l.append(" ")
    return m



def convert(grid: List[List[str]], voc: dict):
    new_grid = []
    for line in grid:
        new_line = []
        for char in line:
            if char in voc:
                new_line.append(voc[char])
            else:
                new_line.append(char)
        new_grid.append(new_line)
    return new_grid



def set_s0(voc: dict, model: dict = model):
    d = {}
    for cle in model.values():
        d[cle] = []
    d['slidingTraps'] = []
    del d['slidingTrapsTrocks']
    del d['openTrapsrocks']
    del d['slidingTrapsT']
    del d['slidingTrapsF']
    del d['slidingTrapsFrocks']
    i = 0
    for line in voc.get('grid'):
        j = 0
        for elem in line:
            if elem in model.values():
                if elem == 'key' or elem == 'hero':
                    d[elem].append((i,j))
                    d[elem] = tuple(d[elem][0])
                #cas d'une roche posée sur un piège
                elif elem.find('rocks')>0 and elem != 'rocks':
                    d['rocks'].append((i,j))
                    if elem == 'openTrapsrocks':
                        d['openTraps'].append((i,j))
                    elif elem == 'slidingTrapsFrocks':
                        d['slidingTraps'].append((i,j,False))
                    elif elem == 'slidingTrapsTrocks':
                        d['slidingTraps'].append((i,j,True))
                elif elem == 'slidingTrapsF':
                    d['slidingTraps'].append((i,j,False))
                elif elem == 'slidingTrapsT':
                    d['slidingTraps'].append((i,j,True))
                else:
                    d[elem].append((i,j))
            j += 1
        i += 1
    # set representation de la clé = (int posx, int posy, bool recup?)
    if d.get('key') and d['hero'] != d.get('key'):
        d['lock'] = tuple([d['lock'][0][0], d['lock'][0][1], False])
    elif d.get('key') and d['hero'] == d.get('key'):
        d['lock'] = tuple([d['lock'][0][0], d['lock'][0][1], True])
    # compteur
    d['counter'] = voc['max_steps'] #tuple([voc['max_steps']])
    # taille du terrain de jeu (nLignes, nCol)
    d['dim'] = (voc['m'],voc['n'])
    # transformation de toutes les valeurs en format hashable
    for cle in ['walls','rocks','openTraps','slidingTraps','skeletons','goals']:
        d[cle] = set(d[cle])
    return d



def grid_from_file(filename: str, voc: dict = model):
    """
    Cette fonction lit un fichier et le convertit en une grille de Helltaker
    Retour:
    - un dictionnaire contenant:
        - la grille de jeu sous une forme d'une liste de liste de (chaînes de) caractères
        - le nombre de ligne m
        - le nombre de colonnes n
        - le titre de la grille
        - le nombre maximal de coups max_steps
    """
    grid = []
    m = 0  # nombre de lignes
    n = 0  # nombre de colonnes
    no = 0  # numéro de ligne du fichier
    title = ""
    max_steps = 0
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            no += 1
            l = line.rstrip()
            if no == 1:
                title = l
                continue
            if no == 2:
                max_steps = int(l)
                continue
            if len(l) > n:
                n = len(l)
                complete(grid, n)
            if l != "":
                grid.append(list(l))
    if voc:
        grid = convert(grid, voc)
    m = len(grid)
    #return {"grid": grid, "title": title, "m": m, "n": n, "max_steps": max_steps}
    dico = {"grid": grid, "title": title, "m": m, "n": n, "max_steps": max_steps}
    return set_s0(dico)



def check_plan(plan: str):
    """
    Cette fonction vérifie que le plan est valide/
    Argument: un plan sous forme de chaîne de caractères
    """
    for c in plan:
        if c not in "hbgd":
            return False
    return True



def test():
    if len(sys.argv) != 2:
        sys.exit(-1)

    filename = sys.argv[1]

    pprint(grid_from_file(filename, {"H": "@", "B": "$", "D": "."}))

    print(check_plan("erfre"))
    print(check_plan("hhbbggdd"))



if __name__ == "__main__":
    test()
