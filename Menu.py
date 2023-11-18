# Ajouter option de choix de langue
# Ajouter option de mute musiques et sons

# pyinstaller Menu.py --onefile --noconsole --add-data "musique_menu.mp3;." --add-data "Musique.mp3;." --add-data "bouton_clique.mp3;." --add-data "clique_case.mp3;." --add-data "easter_egg.mp3;." --add-data "explosion.mp3;." --add-data "marque_case.mp3;." --add-data "win.mp3;." --add-data "Boucle_facile.py;." --add-data "Boucle_moyen.py;." --add-data "Boucle_difficile.py;." --add-data "Boucle_succes.py;." --add-data "Boucle_temps.py;." --icon=icon.ico

## ----- Importation des Modules ----- ##
from tkinter import *
from tkinter import Button, Label
from pygame import mixer
import time
from pathlib import Path

## ----- Succes ----- ##
malchanceux = False
expeditif = False
temeraire = False
champion = False
chanceux = False
completionniste = False

mixer.init()

# Sert a eviter les problemes de reset de la musique
musique_en_cour = 0
# chemin_temporaire = Path(sys._MEIPASS)
# chemin_musique = chemin_temporaire / "musique_menu.mp3"
chemin_musique = Path(__file__).parent / "musique_menu.mp3"
son_bouton = Path(__file__).parent / "bouton_clique.mp3"


def main():
    global musique_en_cour
    ## ----- Musique ----- ##
    if musique_en_cour == 0:
        musique_menu = chemin_musique
        mixer.music.load(str(musique_menu))
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)
    clique_bouton = mixer.Sound(son_bouton)
    clique_bouton.set_volume(0.2)

    def centrer_fen(largeur, hauteur):
        ecran_largeur = menu.winfo_screenwidth()
        ecran_hauteur = menu.winfo_screenheight()
        x = (ecran_largeur/2) - (largeur/2)
        y = (ecran_hauteur/2) - (hauteur/2)
        menu.geometry('%dx%d+%d+%d' % (largeur, hauteur, x, y))

    menu = Tk()
    menu.title('Démineur')
    centrer_fen(464, 644)

    def lancement_facile():
        clique_bouton.play()
        time.sleep(0.1)
        import Boucle_facile as boucle_f
        menu.destroy()
        mixer.quit()
        boucle_f.lancer_boucle_facile()

    def lancement_moyen():
        clique_bouton.play()
        time.sleep(0.1)
        import Boucle_moyen as boucle_m
        menu.destroy()
        mixer.quit()
        boucle_m.boucle_moyen()

    def lancement_difficile():
        clique_bouton.play()
        time.sleep(0.1)
        import Boucle_difficile as boucle_d
        menu.destroy()
        mixer.quit()
        boucle_d.boucle_difficile()

    def lancement_temps():
        clique_bouton.play()
        import Boucle_temps as boucle_t
        menu.destroy()
        boucle_t.boucle_temps()

    def lancement_succes():
        clique_bouton.play()
        from Boucle_facile import gagner_f
        if gagner_f == True:
            from Boucle_moyen import gagner_m
            if gagner_m == True:
                from Boucle_difficile import gagner_d
                if gagner_d == True:
                    global completionniste
                    completionniste = True
        import Boucle_succes as boucle_s
        menu.destroy()
        boucle_s.boucle_succes()

    fond_menu = Canvas(menu, width=460, height=640, bg='#a39193')
    fond_menu.grid(row=0, column=0, rowspan=5, sticky=N)

    titre = Label(menu, text=" Démineur ")
    titre.grid(row=0, column=0, columnspan=1, padx=0, pady=30, sticky=N)
    titre.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    sous_titre = Label(menu, text=" Choix de la difficultée ")
    sous_titre.grid(row=0, column=0, columnspan=1, padx=0, pady=100, sticky=N)
    sous_titre.config(font=("Small fonts", 25), bg='#E1CCCE', relief=RIDGE)

    btn_facile = Button(menu, width=10, height=1, bg="#E1CCCE", text="FACILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#00AB14", command=lancement_facile)
    btn_facile.grid(row=0, pady=190, sticky=N)
    btn_facile.config(activebackground="#CAB7B9")
    btn_moyen = Button(menu, width=10, height=1, bg="#E1CCCE", text="MOYEN", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#CE8700", command=lancement_moyen)
    btn_moyen.grid(row=0, pady=260, sticky=N)
    btn_moyen.config(activebackground="#CAB7B9")
    btn_difficile = Button(menu, width=10, height=1, bg="#E1CCCE", text="DIFFICILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#b22222", command=lancement_difficile)
    btn_difficile.grid(row=0, pady=330, sticky=N)
    btn_difficile.config(activebackground="#CAB7B9")

    btn_scoreboard = Button(menu, width=18, height=1, bg="#E1CCCE", text="MEILLEURS TEMPS", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=lancement_temps)
    btn_scoreboard.grid(row=0, pady=435, sticky=N)
    btn_scoreboard.config(activebackground="#CAB7B9")
    btn_succes = Button(menu, width=18, height=1, bg="#E1CCCE", text="SUCCES", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=lancement_succes)
    btn_succes.grid(row=0, pady=495, sticky=N)
    btn_succes.config(activebackground="#CAB7B9")

    btn_quitter = Button(menu, width=25, height=1, bg="#E1CCCE", text="QUITTER", font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_quitter.grid(row=0, pady=582, sticky=N)
    btn_quitter.config(activebackground="#CAB7B9", command=menu.destroy)

    menu.mainloop()


## ----- Lancement du jeu -----##
if __name__ == "__main__":
    main()
