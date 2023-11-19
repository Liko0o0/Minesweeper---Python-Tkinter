## ----- Importation des Modules -----##
from tkinter import *
import time
import random
from tkinter import Button, Label, messagebox
from pathlib import Path
from pygame import mixer
import os
from Menu import icon

## ----- Fichiers liés -----##
# Adapte le chemin d'acces en fonction de ceux du systeme
repertoire_appdata = Path(os.getenv('APPDATA')) / "Minesweeper"
chemin_d = repertoire_appdata / "temps_difficile.txt"
chemin_musique = Path(__file__).parent / "musique.mp3"
son_case = Path(__file__).parent / "clique_case.mp3"
son_marque = Path(__file__).parent / "marque_case.mp3"
son_explosion = Path(__file__).parent / "explosion.mp3"
son_win = Path(__file__).parent / "win.mp3"


## ----- Initialisation de variable -----##
global perdu_de_suite
global gagner_de_suite
global gagner_d
perdu_de_suite = 0
gagner_de_suite = 0
gagner_d = False


def boucle_difficile():
    ## ----- Son ----- ##
    mixer.init()
    musique_jeu = chemin_musique
    mixer.music.load(musique_jeu)
    mixer.music.set_volume(0.03)
    mixer.music.play(-1)
    clique_case = mixer.Sound(son_case)
    clique_case.set_volume(0.1)
    marque_case = mixer.Sound(son_marque)
    marque_case.set_volume(0.4)
    explosion = mixer.Sound(son_explosion)
    explosion.set_volume(0.07)
    win = mixer.Sound(son_win)
    win.set_volume(0.2)

# Permet de centrer la fenetre pour toutes les dimensions d'ecran
    def centrer_fen(largeur, hauteur):
        ecran_largeur = fen.winfo_screenwidth()
        ecran_hauteur = fen.winfo_screenheight()
        x = (ecran_largeur/2) - (largeur/2)
        y = (ecran_hauteur/2) - (hauteur/2)
        fen.geometry('%dx%d+%d+%d' % (largeur, hauteur, x, y))

## ----- Creation de la fenetre ----- ##
    fen = Tk()
    fen.title('Démineur (Difficile)')
    centrer_fen(1120, 750)
    fen.iconbitmap(icon)


## ----- Constante globale -----##
    debut_timer = time.time()  # Initialisation du timer
    global game_over
    global premier_clique
    game_over = False
    premier_clique = True

## ----- Classe pour creer les cases ----- ##
    class Case_d:
        total = []
        nb_case_d = 79

        def __init__(self, x, y):
            self.est_bombe = False
            self.est_decouvert = False
            self.marquer = False
            self.case_btn = None
            self.x = x
            self.y = y
            Case_d.total.append(self)

        def cree_btn_case(self):
            btn = Button(grille, width=9, height=3, bg="#aa6f73")
            btn.bind('<Button-1>', self.clique_gauche)
            btn.bind('<Button-3>', self.clique_droit)
            btn.bind('<Enter>', self.entree)
            btn.bind('<Leave>', self.sortie)
            btn.configure(activebackground="#D69881",
                          activeforeground="#D69881", cursor="dotbox")
            self.case_btn = btn

        def entree(self, event):
            global game_over
            if not self.est_decouvert and not self.marquer and not game_over:
                self.case_btn.configure(bg="#996367")

        def sortie(self, event):
            global game_over
            if not self.est_decouvert and not self.marquer and not game_over:
                self.case_btn.configure(bg="#aa6f73")

        def clique_gauche(self, event):  # Event provient de la methode bind
            global premier_clique
            if self.est_bombe:
                mixer.music.stop()
                self.montre_bombe()
                premier_clique = False
            else:
                clique_case.play()
                self.montre_case()
                premier_clique = False
                if Case_d.nb_case_d == 0:
                    global game_over
                    global premiere_boucle
                    global timer
                    global perdu_de_suite
                    global gagner_de_suite
                    global gagner_d
                    mixer.music.stop()
                    win.play()
                    gagner_d = True
                    game_over = True
                    premiere_boucle = False
                    perdu_de_suite = 0
                    gagner_de_suite += 1
                    if gagner_de_suite == 3:
                        import Menu
                        Menu.champion = True
                    game_over = True
                    premiere_boucle = False
                    temps = resultat_d()
                    ## Enregistrement des données ##
                    score = open(str(chemin_d), "a")
                    score.write(str(temps)+"\n")
                    score.close()
                    if timer <= 70:
                        import Menu
                        Menu.expeditif = True
                    messagebox.showinfo(
                        title="Bravo", message=f"Vous avez gagner en {result} !")
                    rejouer = messagebox.askyesno(
                        title="Rejouer", message="Voulez vous rejouer ?")
                    if rejouer == True:
                        fen.destroy()
                        boucle_difficile()
                    else:
                        import Menu
                        Menu.musique_en_cour = 0
                        fen.destroy()
                        Menu.main()

        def recuperer_coord_case(self, x, y):
            for case in Case_d.total:
                if case.x == x and case.y == y:
                    return case

        def cases_autour(self):
            cases_autour = [
                self.recuperer_coord_case(self.x - 1, self.y - 1),
                self.recuperer_coord_case(self.x - 1, self.y),
                self.recuperer_coord_case(self.x - 1, self.y + 1),
                self.recuperer_coord_case(self.x, self.y - 1),
                self.recuperer_coord_case(self.x + 1, self.y - 1),
                self.recuperer_coord_case(self.x + 1, self.y),
                self.recuperer_coord_case(self.x + 1, self.y + 1),
                self.recuperer_coord_case(self.x, self.y + 1)
            ]
            cases_autour = [
                Case for Case in cases_autour if Case is not None]
            return cases_autour

        def montre_case(self):
            if not self.est_decouvert:
                nb = self.bombe_autour()
                self.case_btn.configure(text=nb)
                if nb == 0:
                    # Sert a stocker temporairement une case et donc eviter les problemes de limite de recursivité
                    pile = [self]
                    while pile:     # Pile = False si elle est vide et donc stop la boucle
                        case_actuelle = pile[0]
                        pile.pop(0)
                        case_actuelle.est_decouvert = True
                        case_actuelle.case_btn.configure(
                            text=" ", bg='#eea990')
                        for case in case_actuelle.cases_autour():
                            if not case.est_decouvert:
                                case.montre_case()
                                if case.bombe_autour() == 0:
                                    pile.append(case)
                elif nb == 1:
                    self.case_btn.configure(fg="#0037ff", bg='#d3927b')
                elif nb == 2:
                    self.case_btn.configure(fg="#119b00", bg='#d3927b')
                elif nb == 3:
                    self.case_btn.configure(fg="#ac5a00", bg='#d3927b')
                elif nb == 4:
                    self.case_btn.configure(fg="#d41a00", bg='#d3927b')
                elif nb == 5:
                    self.case_btn.configure(fg="#bb00bb", bg='#d3927b')
                elif nb >= 6:
                    self.case_btn.configure(bg='#d3927b')
                    import Menu
                    Menu.chanceux = True

                Case_d.nb_case_d -= 1
                nb_case_restantes.configure(
                    text=f" Cases restantes : {Case_d.nb_case_d} ")
            self.est_decouvert = True

        def bombe_autour(self):
            i = 0
            for case in self.cases_autour():
                if case.est_bombe:
                    i += 1
            return i

        def montre_bombe(self):
            self.case_btn.configure(bg='#cc0000', text="✴")
            global premier_clique
            global perdu_de_suite
            global gagner_de_suite
            global game_over
            explosion.play()
            if premier_clique == True:
                import Menu
                Menu.malchanceux = True
            perdu_de_suite += 1
            gagner_de_suite = 0
            if perdu_de_suite == 10:
                import Menu
                Menu.temeraire = True
            game_over = True
            messagebox.showwarning(
                title="Game Over", message="Vous avez cliquer sur une bombe !")
            rejouer = messagebox.askyesno(
                title="Rejouer", message="Voulez vous rejouer ?")
            if rejouer == True:
                fen.destroy()
                boucle_difficile()
            else:
                import Menu
                Menu.musique_en_cour = 0
                fen.destroy()
                Menu.main()

        def nombre_bombe(self):
            i = 21
            for case in Case_d.total:
                if case.marquer:
                    i -= 1
            nb_bombe.configure(text=f" Bombes : {i} ")

        def clique_droit(self, event):
            marque_case.play()
            if self.est_decouvert == False:
                if not self.marquer:                 # Marque une case comme potentielle bombe
                    self.case_btn.configure(bg='#66545e', text="?")
                    self.marquer = True
                else:                                # Annule le marquage
                    self.case_btn.configure(bg="#aa6f73", text="")
                    self.marquer = False
            self.nombre_bombe()

    def random_bombes():
        bombes_choisi = random.sample(Case_d.total, 21)
        for case in bombes_choisi:
            case.est_bombe = True

    def update_time():      # Timer
        global timer
        global game_over
        if not game_over == True:
            timer = int(time.time() - debut_timer)
            temps.config(text=f" {timer} ")
            fen.after(1000, update_time)

    def resultat_d():
        global timer
        global result
        m = 0
        while timer >= 60:
            timer -= 60
            m += 1
        s = timer
        result = f"{m} minutes et {s} secondes"
        return f"{m},{s}"

## ----- Création des canevas -----##
    # Fond
    menu = Canvas(fen, width=1110, height=740, bg='#a39193')
    menu.grid(row=0, column=0, columnspan=1, padx=3, pady=3)

    bordure = Frame(fen, bg='#f6e0b5', width=757, height=585)
    bordure.place(x=177, y=125)

    grille = Frame(fen)
    grille.place(x=190, y=138)

## ---- Création des informations -----##
    # Titre
    titre = Label(fen, text=" - DIFFICILE - ")
    titre.grid(row=0, column=0, columnspan=2, padx=0, pady=20, sticky=N)
    titre.config(font=("Small fonts", 25, "bold"),
                 bg='#E1CCCE', relief=RIDGE, foreground="#b22222")
    # Temps écoulé
    temps = Label(fen, text=" ")
    temps.grid(row=0, column=0, columnspan=2, padx=80, pady=60, sticky=NE)
    temps.config(font=("Small fonts", 20), bg='#E1CCCE', relief=RIDGE)

    # Recherche des temps
    with open(str(chemin_d), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Trie en fonction du temps
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Affichage du record
    record = Label(fen, text='\n'.join(
        [f' Record: {temps_info[0]} min et {temps_info[1]} sec ' if temps_info[0] > 0 else f' Record: {temps_info[1]} sec ' for i, temps_info in enumerate(l_score[:1], 1)]))

    record.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NE)
    record.config(font=("Small fonts", 15), bg='#E1CCCE', relief=RIDGE)

    nb_bombe = Label(fen, text=" Bombes : 21 ")
    nb_bombe.grid(row=0, column=0, columnspan=2,
                  padx=15, pady=15, sticky=NW)
    nb_bombe.config(font=("Small fonts", 15), bg='#E1CCCE', relief=RIDGE)

    nb_case_restantes = Label(fen, text=" Cases restantes : 79 ")
    nb_case_restantes.grid(
        row=0, column=0, columnspan=2, padx=15, pady=50, sticky=NW)
    nb_case_restantes.config(
        font=("Small fonts", 15), bg='#E1CCCE', relief=RIDGE)

## ----- Lancement -----##
    for x in range(10):
        for y in range(10):
            c = Case_d(x, y)
            c.cree_btn_case()
            c.case_btn.grid(column=x, row=y)  # Creation de la grille
    random_bombes()
    update_time()
    fen.mainloop()
