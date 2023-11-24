## ----- Importation des Modules -----##
from tkinter import *
from tkinter import Button, Label, messagebox
from pygame import mixer
from pathlib import Path
import os
from Main import icon

## ----- Constantes -----##
SUCCES_MALCHANCEUX = "Unlucky"
SUCCES_EXPEDITIF = "Quick"
SUCCES_TEMERAIRE = "Reckless"
SUCCES_CHAMPION = "Champion"
SUCCES_CHANCEUX = "Lucky"
SUCCES_COMPLETIONNISTE = "Complementionist"
SUCCES_COLLECTIONNEUR = "Collector"

## ----- Fichier liés -----##
# Cherche le repertoire APPDATA pour sotcker les infos
repertoire_appdata = Path(os.getenv('APPDATA')) / "Minesweeper"
chemin_s = repertoire_appdata / "achievements.txt"
son_bouton = Path(__file__).parent / "Sound/button_click.mp3"
son_secret = Path(__file__).parent / "Sound/easter_egg.mp3"

## ----- Musique et son ----- ##
clique_bouton = mixer.Sound(son_bouton)
clique_bouton.set_volume(0.3)
secret = mixer.Sound(son_secret)
secret.set_volume(0.3)


def lire_succes():
    with open(str(chemin_s), "r") as file:
        lignes = file.read().splitlines()
    return set(lignes)


def ecrire_succes(succes):
    with open(str(chemin_s), "a") as file:
        file.write(succes + "\n")

## ----- Programme principal ----- ##
def boucle_succes(mute, language, malchanceux, temeraire, expeditif, champion, chanceux, completionniste):
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
        fen.title('Démineur - Succes')
    else:
        fen.title('Démineur - Achievements')
    centrer_fen(844, 604)
    fen.resizable(False, False)
    fen.iconbitmap(icon)

    def retour():
        import Main
        global musique_en_cour
        clique_bouton.play()
        Main.musique_en_cour += 1
        fen.destroy()
        Main.menu(mute, language)

## ----- Création des canevas -----##
    fond_Main = Canvas(fen, width=840, height=600, bg='#a39193')
    fond_Main.grid(row=0, column=0, rowspan=10, sticky=NW)
    ligne_y1 = fond_Main.create_line(
        25, 175, 25, 525, width=4, fill="#726566")
    ligne_y2 = fond_Main.create_line(
        210, 175, 210, 525, width=4, fill="#726566")
    ligne_y3 = fond_Main.create_line(
        815, 175, 815, 525, width=4, fill="#726566")
    ligne_x1 = fond_Main.create_line(
        25, 175, 815, 175, width=4, fill="#726566")
    ligne_x2 = fond_Main.create_line(
        25, 225, 815, 225, width=4, fill="#726566")
    ligne_x3 = fond_Main.create_line(
        25, 275, 815, 275, width=4, fill="#726566")
    ligne_x4 = fond_Main.create_line(
        25, 325, 815, 325, width=4, fill="#726566")
    ligne_x5 = fond_Main.create_line(
        25, 375, 815, 375, width=4, fill="#726566")
    ligne_x6 = fond_Main.create_line(
        25, 425, 815, 425, width=4, fill="#726566")
    ligne_x7 = fond_Main.create_line(
        25, 475, 815, 475, width=4, fill="#726566")
    ligne_x8 = fond_Main.create_line(
        25, 525, 815, 525, width=4, fill="#726566")

    titre = Label(fen, text=" Démineur ")
    titre.grid(row=0, column=0, columnspan=1, padx=310, pady=25, sticky=NW)
    titre.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    sous_titre = Label(fen, text=" Succes ")
    sous_titre.grid(row=0, column=0, columnspan=1,
                    padx=350, pady=95, sticky=NW)
    sous_titre.config(font=("Small fonts", 25, "bold"),
                      bg='#E1CCCE', relief=RIDGE, foreground="#68228b")

## ---- Création des informations -----##
    # Perdre au 1er clique
    titre_malchanceux = Label(fen, text=" Malchanceux ")
    titre_malchanceux.grid(
        row=0, column=0, columnspan=1, pady=186, padx=48, sticky=NW)
    titre_malchanceux.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_malchanceux = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_malchanceux.grid(
        row=0, column=0, columnspan=1, pady=186, padx=240, sticky=NW)
    sous_titre_malchanceux.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Finir en - de 15sec en facile / 45sec en moyen / 1min10 en difficile
    titre_expeditif = Label(fen, text=" Expéditif ")
    titre_expeditif.grid(row=0, column=0, columnspan=1,
                         pady=236, padx=68, sticky=NW)
    titre_expeditif.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_expeditif = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_expeditif.grid(
        row=0, column=0, columnspan=1, pady=236, padx=240, sticky=NW)
    sous_titre_expeditif.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Perdre 10 fois de suite
    titre_temeraire = Label(fen, text=" Téméraire ")
    titre_temeraire.grid(row=0, column=0, columnspan=1,
                         pady=286, padx=61, sticky=NW)
    titre_temeraire.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_temeraire = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_temeraire.grid(
        row=0, column=0, columnspan=1, pady=286, padx=240, sticky=NW)
    sous_titre_temeraire.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Gagner 3 fois de suite
    titre_champion = Label(fen, text=" Champion ")
    titre_champion.grid(row=0, column=0, columnspan=1,
                        pady=336, padx=61, sticky=NW)
    titre_champion.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_champion = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_champion.grid(
        row=0, column=0, columnspan=1, pady=336, padx=240, sticky=NW)
    sous_titre_champion.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Decouvrir une case avec un nb >= 6
    titre_chanceux = Label(fen, text=" Chanceux ")
    titre_chanceux.grid(row=0, column=0, columnspan=1,
                        pady=386, padx=62, sticky=NW)
    titre_chanceux.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_chanceux = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_chanceux.grid(
        row=0, column=0, columnspan=1, pady=386, padx=240, sticky=NW)
    sous_titre_chanceux.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Gagner dans toutes les difficultés
    titre_completionniste = Label(fen, text=" Complétionniste ")
    titre_completionniste.grid(
        row=0, column=0, columnspan=1, pady=436, padx=33, sticky=NW)
    titre_completionniste.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_completionniste = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_completionniste.grid(
        row=0, column=0, columnspan=1, pady=436, padx=240, sticky=NW)
    sous_titre_completionniste.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    # Debloquer tout les succes
    titre_collectionneur = Label(fen, text=" Collectionneur ")
    titre_collectionneur.grid(
        row=0, column=0, columnspan=1, pady=486, padx=41, sticky=NW)
    titre_collectionneur.configure(
        font=("Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE)
    sous_titre_collectionneur = Label(
        fen, text="                                                  ?                                                  ")
    sous_titre_collectionneur.grid(
        row=0, column=0, columnspan=1, pady=486, padx=240, sticky=NW)
    sous_titre_collectionneur.configure(font=(
        "Small fonts", 14, "bold"), bg='#E1CCCE', relief=RIDGE, foreground="#766B65")

    btn_retour = Button(fen, width=20, height=1, bg="#E1CCCE", text="RETOUR", font=(
        "Small fonts", 15, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_retour.grid(row=0, pady=545, padx=290, sticky=NW)
    btn_retour.config(activebackground="#CAB7B9", command=retour)

    if language=='english':
        titre.config(text=' Minesweeper ')
        sous_titre.config(text=' Achievements')
        sous_titre.grid(padx=335)
        titre_malchanceux.config(text=' Unlucky ')
        titre_malchanceux.grid(padx=44)
        titre_temeraire.config(text=' Reckless ')
        titre_temeraire.grid(padx=40)
        titre_chanceux.config(text=' Lucky ')
        titre_completionniste.config(text=' Complementionist ', font=("Small fonts", 13, "bold"))
        titre_expeditif.config(text=' Quick ')
        titre_expeditif.grid(padx=44)
        titre_collectionneur.config(text=' Collector ')
        btn_retour.config(text="BACK")

    def mettre_a_jour_succes(succes, french, english):
        if succes not in lire_succes():
            ecrire_succes(succes)
            if language=='french':
                messagebox.showinfo("Succès débloqué",
                                f"Vous avez débloqué le succès : {french}")
            else:
                messagebox.showinfo("Achievements unlocked",
                                f"You unlocked the achievement : {english}")
            import Main
            setattr(Main, succes, True)

    def succes_malchanceux():
        if malchanceux:
            if language=='french':
                sous_titre_malchanceux.configure(
                    text=" Faire exploser une bombe au premier clique ", foreground="Black")
            else:
                sous_titre_malchanceux.configure(
                    text=" Detonate a bomb at the first click ", foreground="Black")
            mettre_a_jour_succes(SUCCES_MALCHANCEUX, "Malchanceux", "Unlucky")

    def succes_expeditif():
        if expeditif:
            if language=='french':
                sous_titre_expeditif.configure(
                    text=" Gagner en moins de (15s-Facile/45s-Moyen/1m-Difficile) ", foreground="Black")
            else:
                sous_titre_expeditif.configure(
                    text=" Win in less than (15s-Easy/45s-Medium/1m-Hard) ", foreground="Black")
            mettre_a_jour_succes(SUCCES_EXPEDITIF, "Expeditif", "Quick")

    def succes_temeraire():
        if temeraire:
            if language=='french':
                sous_titre_temeraire.configure(
                    text=" Perdre 10 fois d'affilée ", foreground="Black")
            else:
                sous_titre_temeraire.configure(
                    text=" Lose 10 times in a row ", foreground="Black")
            mettre_a_jour_succes(SUCCES_TEMERAIRE, "Temeraire", "Reckless")

    def succes_champion():
        if champion:
            if language=='french':
                sous_titre_champion.configure(
                    text=" Gagner 3 fois d'affilée ", foreground="Black")
            else:
                sous_titre_champion.configure(
                    text=" Win 3 times in a row ", foreground="Black")
            mettre_a_jour_succes(SUCCES_CHAMPION, "Champion", "Champion")

    def succes_chanceux():
        if chanceux:
            if language=='french':
                sous_titre_chanceux.configure(
                    text=" Découvrir une case avec 6 bombes ou plus autour ", foreground="Black")
            else:
                sous_titre_chanceux.configure(
                    text=" Discover a cell with 6 mines or more around ", foreground="Black")
            mettre_a_jour_succes(SUCCES_CHANCEUX, "Chanceux", "Lucky")

    def succes_completionniste():
        if completionniste:
            if language=='french':
                sous_titre_completionniste.configure(
                    text=" Gagner une partie dans chaque difficulté ", foreground="Black")
            else:
                sous_titre_completionniste.configure(
                    text=" Win a game in each difficulty ", foreground="Black")
            mettre_a_jour_succes(SUCCES_COMPLETIONNISTE, "Completionniste", "Complementionist")

    # ?
    def GG():
        import Main
        Main.mixer.music.pause()
        secret.play()

        def easter_egg(texte, couleurs, index, total_iterations):
            if index < total_iterations:
                couleur = couleurs[index % len(couleurs)]
                texte.configure(foreground=couleur)
                fen.after(150, easter_egg, texte, couleurs,
                          index + 1, total_iterations - 1)
            else:
                texte.configure(foreground='black')
                Main.mixer.music.unpause()

        sous_titre_a_clignoter = [sous_titre_malchanceux, sous_titre_expeditif, sous_titre_temeraire,
                                  sous_titre_champion, sous_titre_chanceux, sous_titre_completionniste,
                                  sous_titre_collectionneur]

        titre_a_clignoter = [titre_malchanceux, titre_expeditif, titre_temeraire,
                             titre_champion, titre_chanceux, titre_completionniste, titre_collectionneur]

        couleurs = [
            "#F94144", "#F3722C", "#F8961E", "#F9C74F", "#90BE6D",
            "#43AA8B", "#4D908E", "#577590", "#277DA1", "#577590",
            "#4D908E", "#43AA8B", "#90BE6D", "#F9C74F", "#F8961E",
            "#F3722C",
        ]

        for i, titre in enumerate(titre_a_clignoter):
            fen.after(0, easter_egg, titre, couleurs, i, 270)
        for i, sous_titre in enumerate(sous_titre_a_clignoter):
            fen.after(0, easter_egg, sous_titre, couleurs, i, 270)

    def succes_collectionneur():
        if completionniste and chanceux and champion and temeraire and expeditif and malchanceux:
            if language=='french':
                sous_titre_collectionneur.configure(
                    text=" Débloquer tous les succès ! ", foreground="Black")
            else:
                sous_titre_collectionneur.configure(
                    text=" Unlock all the achievements ! ", foreground="Black")
            mettre_a_jour_succes(SUCCES_COLLECTIONNEUR, "Collectionneur", "Collector")
            GG()

    succes_malchanceux()
    succes_expeditif()
    succes_temeraire()
    succes_champion()
    succes_chanceux()
    succes_completionniste()
    succes_collectionneur()

