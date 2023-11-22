## ----- Importation des Modules -----##
from tkinter import *
from tkinter import Button, Label
from pathlib import Path
import Main
from pygame import mixer
from Loop_easy import chemin_f
from Loop_medium import chemin_m
from Loop_hard import chemin_d
from Main import icon

## ----- Fichiers liés -----##
# Adapte le chemin d'acces en fonction de ceux du systeme
son_bouton = Path(__file__).parent / "Sound/button_click.mp3"
clique_bouton = mixer.Sound(son_bouton)
clique_bouton.set_volume(0.3)


def boucle_temps(mute, language):
    # Permet de centrer la fenetre pour toutes les dimensions d'ecran

    def centrer_fen(largeur, hauteur):
        ecran_largeur = fen.winfo_screenwidth()
        ecran_hauteur = fen.winfo_screenheight()
        x = (ecran_largeur/2) - (largeur/2)
        y = (ecran_hauteur/2) - (hauteur/2)
        fen.geometry('%dx%d+%d+%d' % (largeur, hauteur, x, y))

## ----- Creation de la fenetre ----- ##
    fen = Tk()
    if language == 'french':
        fen.title('Démineur - Meilleurs temps')
    else:
        fen.title('Minesweeper - Best time')
    centrer_fen(864, 744)
    fen.resizable(False, False)
    fen.iconbitmap(icon)

    def retour():
        clique_bouton.play()
        Main.musique_en_cour += 1
        fen.destroy()
        Main.menu(mute, language)

## ----- Création des canevas -----##
    fond_Main = Canvas(fen, width=860, height=740, bg='#a39193')
    fond_Main.grid(row=0, column=0, rowspan=10, columnspan=2, sticky=NW)
    ligne1 = fond_Main.create_line(
        277, 180, 277, 685, width=4, fill="#726566")
    ligne2 = fond_Main.create_line(
        587, 180, 587, 685, width=4, fill="#726566")

    titre = Label(fen, text=" Démineur ")
    titre.grid(row=0, column=0, columnspan=1, padx=319, pady=20, sticky=NW)
    titre.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    sous_titre = Label(fen, text=" Meilleurs temps ")
    sous_titre.grid(row=0, column=0, columnspan=1,
                    padx=288, pady=90, sticky=NW)
    sous_titre.config(font=("Small fonts", 25, "bold"),
                      bg='#E1CCCE', relief=RIDGE, foreground="#68228b")

    titre_facile = Label(fen, text=" Classement facile ")
    titre_facile.grid(row=0, column=0, columnspan=1,
                      padx=28, pady=180, sticky=NW)
    titre_facile.config(font=("Small fonts", 17, "bold"),
                        bg='#E1CCCE', relief=RIDGE, foreground="#00AB14")

## ---- Création des informations -----##
    # Recherche des temps
    with open(str(chemin_f), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Tri en fonction du temps
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Affichage des temps triés
    ligne_temps = Label(fen, text='\n'.join(
        [f'{i}.)  {temps_info[0]} minutes et {temps_info[1]} secondes' for i, temps_info in enumerate(l_score[:20], 1)]))
    ligne_temps.grid(row=0, column=0, columnspan=1,
                     pady=240, padx=13, sticky=NW)
    ligne_temps.config(font=("Small fonts", 13, "bold"),
                       bg='#E1CCCE', relief=RIDGE)

    titre_moyen = Label(fen, text=" Classement moyen ")
    titre_moyen.grid(row=0, column=0, columnspan=1,
                     padx=315, pady=180, sticky=NW)
    titre_moyen.config(font=("Small fonts", 17, "bold"),
                       bg='#E1CCCE', relief=RIDGE, foreground="#CE8700")

    # Recherche des temps
    with open(str(chemin_m), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]

    # Tri en fonction du temps
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Affichage des temps triés
    ligne_temps = Label(fen, text='\n'.join(
        [f'{i}.)  {temps_info[0]} minutes et {temps_info[1]} secondes' for i, temps_info in enumerate(l_score[:20], 1)]))
    ligne_temps.grid(row=0, column=0, columnspan=1,
                     pady=240, padx=310, sticky=NW)
    ligne_temps.config(font=("Small fonts", 13, "bold"),
                       bg='#E1CCCE', relief=RIDGE)

    titre_difficile = Label(fen, text=" Classement difficile ")
    titre_difficile.grid(row=0, column=0, columnspan=1,
                         padx=603, pady=180, sticky=NW)
    titre_difficile.config(font=("Small fonts", 17, "bold"),
                           bg='#E1CCCE', relief=RIDGE, foreground="#b22222")

    # Recherche des temps
    with open(str(chemin_d), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Tri en fonction du temps
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Affichage des temps triés
    ligne_temps = Label(fen, text='\n'.join(
        [f'{i}.)  {temps_info[0]} minutes et {temps_info[1]} secondes' for i, temps_info in enumerate(l_score[:20], 1)]))
    ligne_temps.grid(row=0, column=0, columnspan=1,
                     pady=240, padx=605, sticky=NW)
    ligne_temps.config(font=("Small fonts", 13, "bold"),
                       bg='#E1CCCE', relief=RIDGE)

    btn_retour = Button(fen, width=20, height=1, bg="#E1CCCE", text="RETOUR", font=(
        "Small fonts", 15, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_retour.grid(row=0, pady=690, padx=297, sticky=NW)
    btn_retour.config(activebackground="#CAB7B9", command=retour)
