# [Command to create .EXE with pyinstaller]
# pyinstaller Main.py --onefile --noconsole --add-data "Sound/music_main.mp3;Sound" --add-data "Sound/music_game.mp3;Sound" --add-data "Sound/button_click.mp3;Sound" --add-data "Sound/cell_click.mp3;Sound" --add-data "Sound/easter_egg.mp3;Sound" --add-data "Sound/explosion.mp3;Sound" --add-data "Sound/cell_flag.mp3;Sound" --add-data "Sound/win.mp3;Sound" --add-data "Easy.py;." --add-data "Medium.py;." --add-data "Hard.py;." --add-data "Achievements.py;." --add-data "Time.py;." --add-data "Image/english.png;Image" --add-data "Image/french.png;Image" --add-data "Image/img_sound_mute.png;Image" --add-data "Image/img_sound.png;Image" --add-data "Image/icon.ico;Image" --icon=Image/icon.ico
## ----- Import Modules ----- ##
from tkinter import *
from tkinter import Button, Label
import time
from pathlib import Path
import os
from pygame import mixer


## ----- Path ----- ##
# Search the APPDATA directory to store the information
appdata_path = Path(os.getenv('APPDATA')) / "Minesweeper"
if not appdata_path.exists():
    appdata_path.mkdir(parents=True, exist_ok=True)
path_a = appdata_path / "achievements.txt"
appdata_path.mkdir(parents=True, exist_ok=True)
# Ensure the existence of files
if not path_a.exists():
    with open(str(path_a), "w") as file:
        pass
path_e = appdata_path / "time_easy.txt"
if not path_e.exists():
    with open(str(path_e), "w") as file:
        pass
path_m = appdata_path / "time_medium.txt"
if not path_m.exists():
    with open(str(path_m), "w") as file:
        pass
path_h = appdata_path / "time_hard.txt"
if not path_h.exists():
    with open(str(path_h), "w") as file:
        pass

path_music = Path(__file__).parent / "Sound/music_main.mp3"
button_sound = Path(__file__).parent / "Sound/button_click.mp3"
icon = Path(__file__).parent / "Image/icon.ico"


## ----- Achievements ----- ##
def read_achievements():
    with open(str(path_a), "r") as file:
        lines = file.read().splitlines()
    return set(lines)


ACHIEVEMENT_UNLUCKY = "Unlucky"
ACHIEVEMENT_QUICK = "Quick"
ACHIEVEMENT_RECKLESS = "Reckless"
ACHIEVEMENT_CHAMPION = "Champion"
ACHIEVEMENT_LUCKY = "Lucky"
ACHIEVEMENT_COMPLEMENTIONIST = "Complementionist"
ACHIEVEMENT_COLLECTOR = "Collector"
unlucky = False
quick = False
reckless = False
champion = False
lucky = False
complementionist = False
# Check the achievements already unlocked in the APPDATA
unlucky = ACHIEVEMENT_UNLUCKY in read_achievements()
quick = ACHIEVEMENT_QUICK in read_achievements()
quick = ACHIEVEMENT_RECKLESS in read_achievements()
champion = ACHIEVEMENT_CHAMPION in read_achievements()
lucky = ACHIEVEMENT_LUCKY in read_achievements()
complementionist = ACHIEVEMENT_COMPLEMENTIONIST in read_achievements()


## ----- Initialize the mixer ----- ##
mixer.init()
music_playing = 0  # Used to avoid music reset problems
mute = False
img_music = None
img_music_mute = None


## ----- Main program ----- ##
language = 'french'


def menu(mute, language):
    ## ----- Music and sound ----- ##
    global music_playing
    if music_playing == 0:
        music_main = path_music
        mixer.music.load(str(music_main))
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)
    button_click = mixer.Sound(button_sound)
    button_click.set_volume(0.2)

# Allows to center the window for all screen dimensions
    def center_window(width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        window.geometry('%dx%d+%d+%d' % (width, height, x, y))

## ----- Creating the window ----- ##
    window = Tk()
    if language == 'french':
        window.title('Démineur')
    else:
        window.title('Minesweeper')
    center_window(464, 644)
    window.resizable(False, False)
    window.iconbitmap(icon)

    def easy_launch():
        global language
        global mute
        button_click.play()
        time.sleep(0.1)
        import Easy
        window.destroy()
        mixer.quit()
        Easy.easy_loop(mute, language)

    def medium_launch():
        global language
        global mute
        button_click.play()
        time.sleep(0.1)
        import Medium
        window.destroy()
        mixer.quit()
        Medium.medium_loop(mute, language)

    def hard_launch():
        global language
        global mute
        button_click.play()
        time.sleep(0.1)
        import Hard
        window.destroy()
        mixer.quit()
        Hard.hard_loop(mute, language)

    def time_launch():
        global language
        global mute
        button_click.play()
        import Time
        window.destroy()
        Time.time_loop(mute, language)

    def achievement_launch():
        global language
        global mute
        button_click.play()
        from Easy import e_win
        if e_win == True:
            from Medium import m_win
            if m_win == True:
                from Hard import h_win
                if h_win == True:
                    global complementionist
                    complementionist = True
        import Achievements
        window.destroy()
        Achievements.achievements_loop(mute, language, unlucky, reckless,
                                       quick, champion, lucky, complementionist)

    def toggle_mute():
        global mute
        button_click.play()
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
        button_click.play()
        if language == "french":
            language = "english"
            window.destroy()
            menu(mute, language)
        else:
            language = "french"
            window.destroy()
            menu(mute, language)

    def enter(name, size, event):  # Event come from the bind method
        name.configure(bg="#CAB7B9", font=("Small fonts", size+2))

    def exit(name, size, event):  # Event come from the bind method
        name.configure(bg="#E1CCCE", font=("Small fonts", size))

    menu_background = Canvas(window, width=460, height=640, bg='#a39193')
    menu_background.grid(row=0, column=0, rowspan=5, sticky=N)

    title = Label(window, text=" Démineur ")
    title.grid(row=0, column=0, columnspan=1, padx=0, pady=30, sticky=N)
    title.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    subtitle = Label(window, text=" Choix de la difficultée ")
    subtitle.grid(row=0, column=0, columnspan=1,
                  padx=0, pady=100, sticky=N)
    subtitle.config(font=("Small fonts", 25), bg='#E1CCCE', relief=RIDGE)

    btn_easy = Button(window, width=10, height=1, bg="#E1CCCE", text="FACILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#00AB14", command=easy_launch)
    btn_easy.grid(row=0, pady=190, sticky=N)
    btn_easy.config(activebackground="#CAB7B9")
    btn_easy.bind('<Enter>', lambda event,
                  btn=btn_easy: enter(btn, 18, event))
    btn_easy.bind('<Leave>', lambda event,
                  btn=btn_easy: exit(btn, 18, event))

    btn_medium = Button(window, width=10, height=1, bg="#E1CCCE", text="MOYEN", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#CE8700", command=medium_launch)
    btn_medium.grid(row=0, pady=260, sticky=N)
    btn_medium.config(activebackground="#CAB7B9")
    btn_medium.bind('<Enter>', lambda event,
                    btn=btn_medium: enter(btn, 18, event))
    btn_medium.bind('<Leave>', lambda event,
                    btn=btn_medium: exit(btn, 18, event))

    btn_hard = Button(window, width=10, height=1, bg="#E1CCCE", text="DIFFICILE", font=(
        "Small fonts", 18), relief=RAISED, borderwidth=3, foreground="#b22222", command=hard_launch)
    btn_hard.grid(row=0, pady=330, sticky=N)
    btn_hard.config(activebackground="#CAB7B9")
    btn_hard.bind('<Enter>', lambda event, btn=btn_hard: enter(btn, 18, event))
    btn_hard.bind('<Leave>', lambda event, btn=btn_hard: exit(btn, 18, event))

    btn_best_time = Button(window, width=18, height=1, bg="#E1CCCE", text="MEILLEURS TEMPS", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=time_launch)
    btn_best_time.grid(row=0, pady=435, sticky=N)
    btn_best_time.config(activebackground="#CAB7B9")
    btn_best_time.bind('<Enter>', lambda event,
                       btn=btn_best_time: enter(btn, 15, event))
    btn_best_time.bind('<Leave>', lambda event,
                       btn=btn_best_time: exit(btn, 15,  event))

    btn_achievement = Button(window, width=18, height=1, bg="#E1CCCE", text="SUCCES", font=(
        "Small fonts", 15), relief=RAISED, borderwidth=3, foreground="#68228b", command=achievement_launch)
    btn_achievement.grid(row=0, pady=495, sticky=N)
    btn_achievement.config(activebackground="#CAB7B9")
    btn_achievement.bind('<Enter>', lambda event,
                         btn=btn_achievement: enter(btn, 15, event))
    btn_achievement.bind('<Leave>', lambda event,
                         btn=btn_achievement: exit(btn, 15, event))

    btn_quit = Button(window, width=23, height=1, bg="#E1CCCE", text="QUITTER", font=(
        "Small fonts", 17), relief=RAISED, borderwidth=3, foreground="black")
    btn_quit.grid(row=0, pady=582, sticky=N)
    btn_quit.config(activebackground="#CAB7B9", command=window.destroy)
    btn_quit.bind('<Enter>', lambda event, btn=btn_quit: enter(btn, 17, event))
    btn_quit.bind('<Leave>', lambda event, btn=btn_quit: exit(btn, 17, event))

    if language == 'english':
        title.config(text='Minesweeper')
        subtitle .config(text=" Choice of the difficulty ")
        btn_easy.config(text="EASY")
        btn_medium.config(text="MEDIUM")
        btn_hard.config(text="HARD")
        btn_best_time.config(text="BEST TIME")
        btn_achievement.config(text="ACHIEVEMENTS")
        btn_quit.config(text="QUIT")

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
    btn_mute = Button(window, width=50, height=50, bg="#E1CCCE", image=img_music_btn, font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black", compound=BOTTOM)
    btn_mute.grid(row=0, padx=15, pady=15, sticky=NW)
    btn_mute.config(activebackground="#CAB7B9", command=toggle_mute)
    btn_mute.bind('<Enter>', lambda event, btn=btn_mute: enter(btn, 17, event))
    btn_mute.bind('<Leave>', lambda event, btn=btn_mute: exit(btn,  17, event))

    french_flag = PhotoImage(
        file=Path(__file__).parent / "Image/french.png")
    french_flag = french_flag.subsample(5, 5)
    english_flag = PhotoImage(
        file=Path(__file__).parent / "Image/english.png")
    english_flag = english_flag.subsample(5, 5)
    btn_language = Button(window, width=50, height=50, bg="#E1CCCE", text="", image=french_flag, font=(
        "Small fonts", 17, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_language.grid(row=0, padx=15, pady=15, sticky=NE)
    btn_language.config(activebackground="#CAB7B9",
                        command=switch_language)
    btn_language.bind('<Enter>', lambda event,
                      btn=btn_language: enter(btn, 17, event))
    btn_language.bind('<Leave>', lambda event,
                      btn=btn_language: exit(btn,  17, event))

    if mute:  # Check if muted
        mixer.music.pause()
    if language == 'english':  # Check language
        btn_language.config(image=english_flag)
    window.mainloop()


## ----- Game launcher -----##
if __name__ == "__main__":
    menu(False, "french")
