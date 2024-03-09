import random
import tkinter as tk
from tkinter import messagebox

def jouer(ligne, colonne):
    # Gère le tour du joueur humain
    global joueur, tour
    if grille[ligne][colonne] == " ":
        grille[ligne][colonne] = joueur
        boutons[ligne][colonne].config(text=joueur)
        if verification(grille, joueur):
            messagebox.showinfo("Fin du jeu", "Le joueur {} a gagné !".format(joueur))
            fenetre.quit()
        elif tour == 8:
            messagebox.showinfo("Fin du jeu", "Match nul !")
            fenetre.quit()
        else:
            joueur = "O" if joueur == "X" else "X"
            tour += 1
            if joueur == "O":
                jouer_ordi()
    else:
        messagebox.showwarning("Case occupée", "Cette case est déjà occupée !")

def coup_ordinateur(grille, forme):
    # Cherche s'il y a une opportunité de gagner ou de bloquer le joueur si il a 2 formes côte à côte
    for i in range(3):
        if grille[i].count(forme) == 2 and grille[i].count(" ") == 1:
            return i, grille[i].index(" ")

        col = [grille[j][i] for j in range(3)]
        if col.count(forme) == 2 and col.count(" ") == 1:
            return col.index(" "), i
        
    # Cherche s'il y a une opportunité de gagner en diagonale
    if (grille[0][0] == grille[1][1] == forme and grille[2][2] == " ") or \
       (grille[0][2] == grille[1][1] == forme and grille[2][0] == " "):
        if grille[0][0] == " ":
            return 0, 0
        elif grille[0][2] == " ":
            return 0, 2
        elif grille[2][0] == " ":
            return 2, 0
        else:
            return 2, 2
        
    # Si aucune opportunité, effectue un coup aléatoiree
    return random.choice([(i, j) for i in range(3) for j in range(3) if grille[i][j] == " "])

def jouer_ordi():
    # Gère le tour de l'ordinateur
    ligne, colonne = coup_ordinateur(grille, "X")
    jouer(ligne, colonne)


def verification(grille, forme):
     # Vérification des lignes et des colonnes pour voir si un joueur a gagné
    for i in range(3):
        if all([case == forme for case in grille[i]]) or \
           all([grille[j][i] == forme for j in range(3)]):
            return True

    # Vérification des diagonales pour la victoire
    if (grille[0][0] == grille[1][1] == grille[2][2] == forme) or \
       (grille[0][2] == grille[1][1] == grille[2][0] == forme):
        return True

    return False

def morpion_gui():
    # Initialise l'interface graphique et la partie de morpion
    global fenetre, grille, joueur, tour, boutons
    fenetre = tk.Tk()
    fenetre.title("Morpion - Enzo Méresse")
    

    grille = [[" " for _ in range(3)] for _ in range(3)]
    joueur = "X"
    tour = 0

    boutons = [[None, None, None], [None, None, None], [None, None, None]]

    afficher_grille_gui()
    if joueur == "O":
        jouer_ordi()
    fenetre.mainloop()

def afficher_grille_gui():
     # Affiche la grille dans l'interface graphique
    for i in range(3):
        for j in range(3):
            bouton = tk.Button(fenetre, text=grille[i][j], font=('normal', 20), width=5, height=2,
                               command=lambda i=i, j=j: jouer(i, j))
            bouton.grid(row=i, column=j)
            boutons[i][j] = bouton


def morpion():
    # Gère le déroulement du jeu
    while True:
        morpion_gui()

        rejouer = messagebox.askquestion("Rejouer ?", "Voulez-vous rejouer ?")
        if rejouer.lower() != "yes":
            break

morpion()
