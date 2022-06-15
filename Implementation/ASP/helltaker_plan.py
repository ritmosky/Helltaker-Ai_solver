# -*- coding: utf-8 -*-
import clingo
import sys
from helltaker_utils import grid_from_file, check_plan, affichage2#, affichage
import time


def monsuperplanificateur(infos):
    
    n = infos["m"]
    m = infos["n"]
    h = infos["max_steps"]
    
    pb = "#const n=" + str(n) + "." + "#const m=" + str(m) + "." + "#const horizon=" + str(h) + "."
    
    g = infos["grid"]
    for i in range(len(g)):
        for j in range(len(g[i])):
            p = g[i][j]
            
            if p == "#":
                pb += "wall(" + str(n-i-1) + "," + str(j) + ")."
                
            if p == "H":
                pb += "init(at(" + str(n-i-1) + "," + str(j) + "))."
                
            if p == "D":
                pb += "demon(" + str(n-i-1) + "," + str(j) + ")."
                
            if p == "B":
                pb += "init(box(" + str(n-i-1) + "," + str(j) + "))."
                
            if p == "K":
                pb += "key(" + str(n-i-1) + "," + str(j) + ")."
                
            if p == "L":
                pb += "init(lock(" + str(n-i-1) + "," + str(j) + "))."
                
            if p == "M":
                pb += "init(mob(" + str(n-i-1) + "," + str(j) + "))."
                
            if p == "S":
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",0))."
                
            if p == "T":
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",-1))."
                
            if p == "U":
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",1))."
                
            if p == "O":
                pb += "init(box(" + str(n-i-1) + "," + str(j) + "))."
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",0))."
                
            if p == "P":
                pb += "init(box(" + str(n-i-1) + "," + str(j) + "))."
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",-1))."
                
            if p == "Q":
                pb += "init(box(" + str(n-i-1) + "," + str(j) + "))."
                pb += "init(trap(" + str(n-i-1) + "," + str(j) + ",1))."
                
            if "key" not in pb:
                pb += "key(-1,-1)."
                
    

    with open("asp.txt", "r", encoding="utf-8") as f:
        pb += f.read()

    ctl = clingo.Control(["-n 0"])
    ctl.add("base", [], pb)
    ctl.ground([("base", [])])
    with ctl.solve(yield_=True) as handle:
        for m in handle: sol = "Answer: {}".format(m)
        handle.get()

    solution = affichage2(sol, h)
    return solution


def main():
    
    start = time.time()
    
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de al grille et de toutes les infos
    infos = grid_from_file(filename)
    

    # calcul du plan
    plan = monsuperplanificateur(infos)
    
    

    # affichage du résultat
    if check_plan(plan):
        print("[OK]", plan)
    else:
        print("[Err]", plan, file=sys.stderr)
        sys.exit(2)
        
    endT = time.time()
    print("Temps de résolution : {} sec".format(endT-start))
        

if __name__ == "__main__":
    main()

