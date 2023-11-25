## ----- Import Modules -----##
from tkinter import *
from tkinter import Button, Label
from pathlib import Path
import Main
from pygame import mixer
from Easy import e_path
from Medium import m_path
from Hard import h_path
from Main import icon

## ----- Linked files -----##
button_sound = Path(__file__).parent / "Sound/button_click.mp3"
button_click = mixer.Sound(button_sound)
button_click.set_volume(0.3)

## ----- Main program ----- ##


def time_loop(mute, language):

    # Allows to center the window for all screen dimensions
    def window_center(width, heigth):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (heigth/2)
        window.geometry('%dx%d+%d+%d' % (width, heigth, x, y))

## ----- Creation of the window ----- ##
    window = Tk()
    if language == 'french':
        window.title('Démineur - Meilleurs temps')
    else:
        window.title('Minesweeper - Best time')
    window_center(864, 744)
    window.resizable(False, False)
    window.iconbitmap(icon)

    def back():
        button_click.play()
        Main.music_playing += 1
        window.destroy()
        Main.menu(mute, language)

    def enter(name, size, event):  # Event come from the bind method
        name.configure(bg="#CAB7B9", font=("Small fonts", size+2))

    def exit(name, size, event):  # Event come from the bind method
        name.configure(bg="#E1CCCE", font=("Small fonts", size))

## ----- Canvas creation -----##
    main = Canvas(window, width=860, height=740, bg='#a39193')
    main.grid(row=0, column=0, rowspan=10, columnspan=2, sticky=NW)
    line1 = main.create_line(
        277, 180, 277, 685, width=4, fill="#726566")
    line2 = main.create_line(
        587, 180, 587, 685, width=4, fill="#726566")

    title = Label(window, text=" Démineur ")
    title.grid(row=0, column=0, columnspan=1, padx=319, pady=20, sticky=NW)
    title.config(font=("Small fonts", 35), bg='#E1CCCE', relief=RIDGE)

    subtitle = Label(window, text=" Meilleurs temps ")
    subtitle.grid(row=0, column=0, columnspan=1,
                  padx=288, pady=90, sticky=NW)
    subtitle.config(font=("Small fonts", 25, "bold"),
                    bg='#E1CCCE', relief=RIDGE, foreground="#68228b")

## ---- Information creation -----##
    tilte_easy = Label(window, text=" Classement facile ")
    tilte_easy.grid(row=0, column=0, columnspan=1,
                    padx=28, pady=180, sticky=NW)
    tilte_easy.config(font=("Small fonts", 17, "bold"),
                      bg='#E1CCCE', relief=RIDGE, foreground="#00AB14")
    # Finding times
    with open(str(e_path), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Sorts according to the best times
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Best times display
    if language == 'french':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {time_info[0]} minutes et {time_info[1]} secondes'if time_info[0] > 0 else f'{i}.)  {time_info[1]} secondes' for i, time_info in enumerate(l_score[:20], 1)]))
    elif language == 'english':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {time_info[0]} minutes and {time_info[1]} seconds'if time_info[0] > 0 else f'{i}.)  {time_info[1]} seconds' for i, time_info in enumerate(l_score[:20], 1)]))
    line_time.grid(row=0, column=0, columnspan=1,
                   pady=240, padx=13, sticky=NW)
    line_time.config(font=("Small fonts", 13, "bold"),
                     bg='#E1CCCE', relief=RIDGE)

    title_medium = Label(window, text=" Classement moyen ")
    title_medium.grid(row=0, column=0, columnspan=1,
                      padx=315, pady=180, sticky=NW)
    title_medium.config(font=("Small fonts", 17, "bold"),
                        bg='#E1CCCE', relief=RIDGE, foreground="#CE8700")
    # Finding times
    with open(str(m_path), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Sorts according to the best times
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Best times display
    if language == 'french':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {temps_info[0]} minutes et {temps_info[1]} secondes'if temps_info[0] > 0 else f'{i}.)  {temps_info[1]} secondes' for i, temps_info in enumerate(l_score[:20], 1)]))
    elif language == 'english':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {temps_info[0]} minutes and {temps_info[1]} seconds'if temps_info[0] > 0 else f'{i}.)  {temps_info[1]} seconds' for i, temps_info in enumerate(l_score[:20], 1)]))
    line_time.grid(row=0, column=0, columnspan=1,
                   pady=240, padx=310, sticky=NW)
    line_time.config(font=("Small fonts", 13, "bold"),
                     bg='#E1CCCE', relief=RIDGE)

    title_hard = Label(window, text=" Classement difficile ")
    title_hard.grid(row=0, column=0, columnspan=1,
                    padx=603, pady=180, sticky=NW)
    title_hard.config(font=("Small fonts", 17, "bold"),
                      bg='#E1CCCE', relief=RIDGE, foreground="#b22222")
    # Finding times
    with open(str(h_path), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Sorts according to the best times
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Best times display
    if language == 'french':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {temps_info[0]} minutes et {temps_info[1]} secondes'if temps_info[0] > 0 else f'{i}.)  {temps_info[1]} secondes' for i, temps_info in enumerate(l_score[:20], 1)]))
    elif language == 'english':
        line_time = Label(window, text='\n'.join(
            [f'{i}.)  {temps_info[0]} minutes and {temps_info[1]} seconds'if temps_info[0] > 0 else f'{i}.)  {temps_info[1]} seconds' for i, temps_info in enumerate(l_score[:20], 1)]))
    line_time.grid(row=0, column=0, columnspan=1,
                   pady=240, padx=605, sticky=NW)
    line_time.config(font=("Small fonts", 13, "bold"),
                     bg='#E1CCCE', relief=RIDGE)

    btn_back = Button(window, width=20, height=1, bg="#E1CCCE", text="RETOUR", font=(
        "Small fonts", 15, "bold"), relief=RAISED, borderwidth=3, foreground="black")
    btn_back.grid(row=0, pady=690, padx=297, sticky=NW)
    btn_back.config(activebackground="#CAB7B9", command=back)
    btn_back.bind('<Enter>', lambda event, btn=btn_back: enter(btn, 15, event))
    btn_back.bind('<Leave>', lambda event, btn=btn_back: exit(btn, 15, event))
    
    if language == 'english':
        title.config(text=' Minesweeper ')
        title.grid(row=0, column=0, columnspan=1, padx=273, pady=20, sticky=NW)
        subtitle.config(text=' Best time ')
        subtitle.grid(row=0, column=0, columnspan=1,
                      padx=320, pady=90, sticky=NW)
        tilte_easy.config(text=' Easy ranking ')
        title_medium.config(text=' Medium ranking ')
        title_hard.config(text=' Hard ranking ')
        btn_back.config(text="BACK")
