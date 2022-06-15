"""
Version: 1.1.1
Auteur : Sylvain Lagrue <sylvain.lagrue@hds.utc.fr>

Ce module contient différentes fonction permettant de lire des fichiers Helltaker au format défini pour le projet et de vérifier des plans.
"""

from fileinput import filename
from pprint import pprint
import sys
from typing import List


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


def grid_from_file(filename: str, voc: dict = {}):
    """
    Cette fonction lit un fichier et le convertit en une grille de Helltaker

    Arguments:
    - filename: fichier contenant la description de la grille
    - voc: argument facultatif permettant de convertir chaque case de la grille en votre propre vocabulaire

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

    return {"grid": grid, "title": title, "m": m, "n": n, "max_steps": max_steps}


def check_plan(plan: str):
    """
    Cette fonction vérifie que votre plan est valide/

    Argument: un plan sous forme de chaîne de caractères
    Retour  : True si le plan est valide, False sinon
    """
    valid = "hbgd"
    for c in plan:
        if c not in valid:
            return False
    return True

def affichage(s):
    f = ""

    for i in range(len(s)-3):

        if s[i] == "d" and s[i+1] == "o":
            action = ""
            j = i+2
            while s[j] != "d" and j < len(s)-1:
                action += s[j]
                j += 1
            if "left" in action:
                f += "g"
            if "right" in action:
                f += "d"
            if "top" in action:
                f += "h"
            if "bot" in action:
                f += "b"
                
    return f

def affichage2(s, max_steps):
    f = ""
    for i in range(max_steps):

        for j in range(len(s)):
            
            if i < 10:

            
                if s[j] == str(i) and s[j+1] == ")" and s[j-1] == ",":
                    
                
                    if s[j-5] == "l":
                        f += "g"
                    if s[j-6] == "r":
                        f += "d"
                    if s[j-4] == "t":
                        f += "h"
                    if s[j-4] == "b":
                        f += "b"
                        
            if i >= 10:
                
                
                if s[j] == str(i)[0] and s[j+1] == str(i)[1]:
                
                    if s[j-5] == "l":
                        f += "g"
                    if s[j-6] == "r":
                        f += "d"
                    if s[j-4] == "t":
                        f += "h"
                    if s[j-4] == "b":
                        f += "b"
                
    return f
            


def test():
    if len(sys.argv) != 2:
        sys.exit(-1)

    filename = sys.argv[1]

    pprint(grid_from_file(filename, {"H": "@", "B": "$", "D": "."}))

    print(check_plan("erfre"))
    print(check_plan("hhbbggdd"))


if __name__ == "__main__":
    test()
