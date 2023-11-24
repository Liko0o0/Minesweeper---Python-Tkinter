## ----- Importation des Modules ----- ##
from tkinter import *
from tkinter import Button, Label
import time
from pathlib import Path
import os
from pygame import mixer

language = 'french'
## ----- Succes ----- ##
repertoire_appdata = Path(os.getenv('APPDATA')) / "Minesweeper"
chemin_s = repertoire_appdata / "achievements.txt"
repertoire_appdata.mkdir(parents=True, exist_ok=True)
if not chemin_s.exists():
    with open(str(chemin_s), "w") as file:
        pass


def lire_succes():
    with open(str(chemin_s), "r") as file:
        lignes = file.read().splitlines()
    return set(lignes)


SUCCES_MALCHANCEUX = "Unlucky"
SUCCES_EXPEDITIF = "Quick"
SUCCES_TEMERAIRE = "Reckless"
SUCCES_CHAMPION = "Champion"
SUCCES_CHANCEUX = "Lucky"
SUCCES_COMPLETIONNISTE = "Complementionist"
SUCCES_COLLECTIONNEUR = "Collector"
malchanceux = False
expeditif = False
temeraire = False
champion = False
chanceux = False
completionniste = False
# Verifie les succes deja débloquer dans le APPDATA
malchanceux = SUCCES_MALCHANCEUX in lire_succes()
expeditif = SUCCES_EXPEDITIF in lire_succes()
temeraire = SUCCES_TEMERAIRE in lire_succes()
champion = SUCCES_CHAMPION in lire_succes()
chanceux = SUCCES_CHANCEUX in lire_succes()
completionniste = SUCCES_COMPLETIONNISTE in lire_succes()


## ----- Initialise le mixer ----- ##
mixer.init()
musique_en_cour = 0  # Sert a eviter les problemes de reset de la musique
mute = False
img_music = None
img_music_mute = None

## ----- Chemin ----- ##
# Cherche le repertoire APPDATA pour stocker les infos
repertoire_appdata = Path(os.getenv('APPDATA')) / "Minesweeper"
if not repertoire_appdata.exists():  # Assurer l'existence du répertoire
    repertoire_appdata.mkdir(parents=True, exist_ok=True)

# Assurer l'existence des fichiers
chemin_f = repertoire_appdata / "time_easy.txt"
if not chemin_f.exists():
    with open(str(chemin_f), "w") as file:
        pass
chemin_m = repertoire_appdata / "time_medium.txt"
if not chemin_m.exists():
    with open(str(chemin_m), "w") as file:
        pass
chemin_d = repertoire_appdata / "time_hard.txt"
if not chemin_d.exists():
    with open(str(chemin_d), "w") as file:
        pass

chemin_musique = Path(__file__).parent / "Sound/music_main.mp3"
son_bouton = Path(__file__).parent / "Sound/button_click.mp3"
icon = Path(__file__).parent / "Image/icon.ico"


## ----- Programme principal ----- ##


def menu(mute, language):
    ## ----- Musique et son ----- ##
    global musique_en_cour
    if musique_en_cour == 0:
        musique_menu = chemin_musique
        mixer.music.load(str(musique_menu))
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
    clique_bouton = mixer.Sound(son_bouton)
    clique_bouton.set_volume(0.2)

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
        fen.title('Démineur')
    else:
        fen.title('Minesweeper')
    centrer_fen(464, 644)
    fen.resizable(False, False)
    fen.iconbitmap(icon)

    def lancement_facile():
        global language
        global mute
        clique_bouton.play()
        time.sleep(0.1)
        import Loop_easy as loop_e
        fen.destroy()
        mixer.quit()
        loop_e.boucle_facile(mute, language)

    def lancement_moyen():
        global language
        global mute
        clique_bouton.play()
        time.sleep(0.1)
        import Loop_medium as loop_m
        fen.destroy()
        mixer.quit()
        loop_m.boucle_moyen(mute, language)

    def lancement_difficile():
        global language
        global mute
        clique_bouton.play()
        time.sleep(0.1)
        import Loop_hard as loop_h
        fen.destroy()
        mixer.quit()
        loop_h.boucle_difficile(mute, language)

    def lancement_temps():
        global language
        global mute
        clique_bouton.play()
        import Loop_time as loop_t
        fen.destroy()
        loop_t.boucle_temps(mute, language)

    def lancement_succes():
        global language
        global mute
        clique_bouton.play()
        from Loop_easy import gagner_f
        if gagner_f == True:
            from Loop_medium import gagner_m
            if gagner_m == True:
                from Loop_hard import gagner_d
                if gagner_d == True:
                    global completionniste
                    completionniste = True
        import Loop_achievements as loop_s
        fen.destroy()
        loop_s.boucle_succes(mute, language, malchanceux, temeraire,
                             expeditif, champion, chanceux, completionniste)

    def toggle_mute():
        global mute
        clique_bouton.play()
        if mixer.music.get_busy():
            mixer.music.pause()
            mute = True
            btn_mute.config(image=img_music_mute)
        else:
            mixer.music.unpause()
            mute = False
            btn_mute.config(image=img_music)

    def switch_language():
        global language
        global mute
        clique_bouton.play()
        if language == "french":
            language = "english"
            fen.destroy()
            menu(mute, language)
        else:
            language = "french"
            fen.destroy()
            menu(mute, language)

    fond_menu = Canvas(fen, width=460, height=640, bg='#a39193')
    fond_menu.grid(row=0, column=0, rowspan=5, sticky=N)

    titre = Label(fen, text=" Démineur ")
    titre.grid(row=0, column=0, columnspan=1, padx=0, pady=30, sticky=N)
    titre.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    sous_titre = Label(fen, text=" Choix de la difficultée ")
    sous_titre.grid(row=0, column=0, columnspan=1,
                    padx=0, pady=100, sticky=N)
    sous_titre.config(font=("Small fonts", 25), bg='#E1CCCE', relief=RIDGE)

    btn_facile = Button(fen, width=10, height=1, bg="#E1CCCE", text="FACILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#00AB14", command=lancement_facile)
    btn_facile.grid(row=0, pady=190, sticky=N)
    btn_facile.config(activebackground="#CAB7B9")
    btn_moyen = Button(fen, width=10, height=1, bg="#E1CCCE", text="MOYEN", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#CE8700", command=lancement_moyen)
    btn_moyen.grid(row=0, pady=260, sticky=N)
    btn_moyen.config(activebackground="#CAB7B9")
    btn_difficile = Button(fen, width=10, height=1, bg="#E1CCCE", text="DIFFICILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#b22222", command=lancement_difficile)
    btn_difficile.grid(row=0, pady=330, sticky=N)
    btn_difficile.config(activebackground="#CAB7B9")

    btn_scoreboard = Button(fen, width=18, height=1, bg="#E1CCCE", text="MEILLEURS TEMPS", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=lancement_temps)
    btn_scoreboard.grid(row=0, pady=435, sticky=N)
    btn_scoreboard.config(activebackground="#CAB7B9")
    btn_succes = Button(fen, width=18, height=1, bg="#E1CCCE", text="SUCCES", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=lancement_succes)
    btn_succes.grid(row=0, pady=495, sticky=N)
    btn_succes.config(activebackground="#CAB7B9")

    btn_quitter = Button(fen, width=25, height=1, bg="#E1CCCE", text="QUITTER", font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_quitter.grid(row=0, pady=582, sticky=N)
    btn_quitter.config(activebackground="#CAB7B9", command=fen.destroy)

    if language == 'english':
        titre.config(text='Minesweeper')
        sous_titre .config(text=" Choice of the difficulty ")
        btn_facile.config(text="EASY")
        btn_moyen.config(text="MEDIUM")
        btn_difficile.config(text="HARD")
        btn_scoreboard.config(text="BEST TIME")
        btn_succes.config(text="ACHIEVEMENTS")
        btn_quitter.config(text="QUIT")

    img_music_path = PhotoImage(
        file=Path(__file__).parent / "Image/img_sound.png")
    img_music = img_music_path.subsample(55, 55)
    img_music_mute_path = PhotoImage(
        file=Path(__file__).parent / "Image/img_sound_mute.png")
    img_music_mute = img_music_mute_path.subsample(4, 4)
    if mute:
        img_music_btn = img_music_mute
    else:
        img_music_btn = img_music
    btn_mute = Button(fen, width=50, height=50, bg="#E1CCCE", image=img_music_btn, font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black", compound=BOTTOM)
    btn_mute.grid(row=0, padx=15, pady=15, sticky=NW)
    btn_mute.config(activebackground="#CAB7B9", command=toggle_mute)

    french_flag = PhotoImage(
        file=Path(__file__).parent / "Image/french.png")
    french_flag = french_flag.subsample(5, 5)
    english_flag = PhotoImage(
        file=Path(__file__).parent / "Image/english.png")
    english_flag = english_flag.subsample(5, 5)
    btn_language = Button(fen, width=50, height=50, bg="#E1CCCE", image=french_flag, font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_language.grid(row=0, padx=15, pady=15, sticky=NE)
    btn_language.config(activebackground="#CAB7B9",
                        command=switch_language)

    if mute:  # Verifie si mute
        mixer.music.pause()
    if language == 'english':  # Verifie la langue
        btn_language.config(image=english_flag)
    fen.mainloop()


## ----- Lancement du jeu -----##
if __name__ == "__main__":
    menu(False, "french")

