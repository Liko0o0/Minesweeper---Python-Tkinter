## ----- Import Modules -----##
from tkinter import *
import time
import random
from tkinter import Button, Label, messagebox
from pathlib import Path
from pygame import mixer
import os
from Main import icon


## ----- Linked files -----##
appdata_path = Path(os.getenv('APPDATA')) / "Minesweeper"
e_path = appdata_path / "time_easy.txt"
music_path = Path(__file__).parent / "Sound/music_game.mp3"
cell_sound = Path(__file__).parent / "Sound/cell_click.mp3"
flag_sound = Path(__file__).parent / "Sound/cell_flag.mp3"
explosion_sound = Path(__file__).parent / "Sound/explosion.mp3"
win_sound = Path(__file__).parent / "Sound/win.mp3"


## ----- Variable initialization -----##
global lost_in_a_row
global win_in_a_row
global e_win
lost_in_a_row = 0
win_in_a_row = 0
e_win = False

## ----- Main program ----- ##


def easy_loop(mute, language):

    ## ----- Music and sound ----- ##
    mixer.init()
    game_music = music_path
    mixer.music.load(game_music)
    mixer.music.set_volume(0.2)
    mixer.music.play(-1)
    cell_click = mixer.Sound(cell_sound)
    cell_click.set_volume(0.2)
    cell_flag = mixer.Sound(flag_sound)
    cell_flag.set_volume(0.4)
    explosion = mixer.Sound(explosion_sound)
    explosion.set_volume(0.15)
    win = mixer.Sound(win_sound)
    win.set_volume(0.25)
    if mute:
        mixer.music.set_volume(0)

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
        window.title('Démineur (Facile)')
    else:
        window.title('Minesweeper (Easy)')
    window_center(710, 480)
    window.resizable(False, False)
    window.iconbitmap(icon)

## ----- Variable initialization -----##
    timer_start = time.time()
    global game_over
    global first_click
    game_over = False
    first_click = True

## ----- Class to create the cell ----- ##
    class Cell_e:
        total = []
        cell_nb = 52

        def __init__(self, x, y):
            self.is_mine = False
            self.is_discovered = False
            self.flag = False
            self.btn_cell = None
            self.x = x
            self.y = y
            Cell_e.total.append(self)

        def create_cell_btn(self):
            btn = Button(grid, width=3, height=1, bg="#aa6f73",
                         text='', font=("Small fonts", 15, "bold"))
            btn.bind('<Button-1>', self.left_click)
            btn.bind('<Button-3>', self.right_click)
            btn.bind('<Enter>', self.enter)
            btn.bind('<Leave>', self.exit)
            btn.configure(activebackground="#D69881",
                          activeforeground="#D69881", cursor="dotbox")
            self.btn_cell = btn

        def enter(self, event):  # Event come from the bind method
            global game_over
            if not self.is_discovered and not self.flag and not game_over:
                self.btn_cell.configure(bg="#996367")

        def exit(self, event):  # Event come from the bind method
            global game_over
            if not self.is_discovered and not self.flag and not game_over:
                self.btn_cell.configure(bg="#aa6f73")

        def left_click(self, event):  # Event come from the bind method
            if not self.flag:
                global first_click
                if self.is_mine:
                    mixer.music.stop()
                    self.show_mine()
                    first_click = False
                else:
                    cell_click.play()
                    self.show_cell()
                    first_click = False
                    if Cell_e.cell_nb == 0:
                        global game_over
                        global first_loop
                        global result
                        global timer
                        global lost_in_a_row
                        global win_in_a_row
                        global e_win
                        mixer.music.stop()
                        win.play()
                        e_win = True
                        game_over = True
                        first_loop = False
                        lost_in_a_row = 0
                        win_in_a_row += 1
                        if win_in_a_row == 3:
                            import Main
                            Main.champion = True
                        time = result_f()
                        # Data recording
                        score = open(str(e_path), "a+")
                        score.write(str(time)+"\n")
                        score.close()
                        if timer <= 15:
                            import Main
                            Main.quick = True
                        if language == 'french':
                            messagebox.showinfo(
                                title="Bravo", message=f"Vous avez gagner en {result} !")
                            play_again = messagebox.askyesno(
                                title="Rejouer", message="Voulez vous rejouer ?")
                        elif language == 'english':
                            messagebox.showinfo(
                                title="GG", message=f"You have won in {result} !")
                            play_again = messagebox.askyesno(
                                title="Play again", message="Do you want to play again ?")
                        if play_again == True:
                            window.destroy()
                            easy_loop(mute, language)
                        elif play_again == False:
                            import Main
                            Main.music_playing = 0
                            window.destroy()
                            Main.menu(mute, language)

        def collect_cell_coordinate(self, x, y):
            for cell in Cell_e.total:
                if cell.x == x and cell.y == y:
                    return cell

        def cell_around(self):
            cell_around = [
                self.collect_cell_coordinate(self.x - 1, self.y - 1),
                self.collect_cell_coordinate(self.x - 1, self.y),
                self.collect_cell_coordinate(self.x - 1, self.y + 1),
                self.collect_cell_coordinate(self.x, self.y - 1),
                self.collect_cell_coordinate(self.x + 1, self.y - 1),
                self.collect_cell_coordinate(self.x + 1, self.y),
                self.collect_cell_coordinate(self.x + 1, self.y + 1),
                self.collect_cell_coordinate(self.x, self.y + 1)
            ]
            cell_around = [
                Cell for Cell in cell_around if Cell is not None]
            return cell_around

        def show_cell(self):
            if not self.is_discovered:
                nb = self.mine_around()
                self.btn_cell.configure(text=nb)
                if nb == 0:
                    # Used to temporarily store a box and therefore avoid recursion limit problems
                    L = [self]
                    while L:     # Pile=False if empty so stop the loop
                        current_cell = L[0]
                        L.pop(0)
                        current_cell.is_discovered = True
                        current_cell.btn_cell.configure(
                            text=" ", bg='#eea990')
                        for cell in current_cell.cell_around():
                            if not cell.is_discovered:
                                cell.show_cell()
                                if cell.mine_around() == 0:
                                    L.append(cell)
                elif nb == 1:
                    self.btn_cell.configure(fg="#6688c3", bg='#d3927b')
                elif nb == 2:
                    self.btn_cell.configure(fg="#00ab66", bg='#d3927b')
                elif nb == 3:
                    self.btn_cell.configure(fg="#C35214", bg='#d3927b')
                elif nb == 4:
                    self.btn_cell.configure(fg="#ce4a4a", bg='#d3927b')
                elif nb == 5:
                    self.btn_cell.configure(fg="#b25da6", bg='#d3927b')
                elif nb >= 6:
                    self.btn_cell.configure(bg='#d3927b')
                    import Main
                    Main.lucky = True

                Cell_e.cell_nb -= 1
                if language == 'french':
                    nb_remaining_cell.configure(
                        text=f" Cases restantes : {Cell_e.cell_nb} ")
                else:
                    nb_remaining_cell.configure(
                        text=f" Cell left : {Cell_e.cell_nb} ")
            self.is_discovered = True

        def mine_around(self):
            i = 0
            for cell in self.cell_around():
                if cell.is_mine:
                    i += 1
            return i

        def show_mine(self):
            self.btn_cell.configure(bg='#cc0000', text="✴")
            global first_click
            global lost_in_a_row
            global win_in_a_row
            global game_over
            explosion.play()
            if first_click == True:
                import Main
                Main.unlucky = True
            lost_in_a_row += 1
            win_in_a_row = 0
            if lost_in_a_row == 10:
                import Main
                Main.reckless = True
            game_over = True
            if language == 'french':
                messagebox.showwarning(
                    title="Game Over", message="Vous avez cliquer sur une bombe !")
                play_again = messagebox.askyesno(
                    title="Rejouer", message="Voulez vous rejouer ?")
            elif language == 'english':
                messagebox.showwarning(
                    title="Game Over", message="You clicked on a mine !")
                play_again = messagebox.askyesno(
                    title="Play again", message="Do you want to play again ?")
            if play_again == True:
                window.destroy()
                easy_loop(mute, language)
            else:
                import Main
                Main.music_playing = 0
                window.destroy()
                Main.menu(mute, language)

        def mine_number(self):
            i = 12
            for cell in Cell_e.total:
                if cell.flag:
                    i -= 1
            if language == 'french':
                mine_nb.configure(text=f" Bombes : {i} ")
            else:
                mine_nb.configure(text=f" Mines : {i} ")

        def right_click(self, event):
            cell_flag.play()
            if self.is_discovered == False:
                if not self.flag:
                    self.btn_cell.configure(bg='#66545e', text="?")
                    self.flag = True
                else:
                    self.btn_cell.configure(bg="#aa6f73", text="")
                    self.flag = False
            self.mine_number()

    def random_mine():
        chosen_mine = random.sample(Cell_e.total, 12)
        for cell in chosen_mine:
            cell.is_mine = True

    def update_time():
        global timer
        global game_over
        if not game_over == True:
            timer = int(time.time() - timer_start)
            chronometre.config(text=f" {timer} ")
            window.after(1000, update_time)

    def result_f():
        global timer
        global result
        m = 0
        s = timer
        while s >= 60:
            s -= 60
            m += 1
        if m == 0:
            result = f"{s} secondes"
        else:
            result = f"{m} minutes et {s} secondes"
        if language == 'english':
            if m == 0:
                result = f"{s} seconds"
            else:
                result = f"{m} minutes and {s} seconds"
        return f"{m},{s}"


## ----- Canvas creation -----##
    main = Canvas(window, width=700, height=470, bg='#a39193')
    main.grid(row=0, column=0, columnspan=1, padx=3, pady=3)

    border = Frame(window, bg='#f6e0b5', width=416, height=356)
    border.place(x=145, y=100)

    grid = Frame(window)
    grid.place(x=157, y=110)

## ---- Information creation -----##
    title = Label(window, text=" - FACILE - ")
    title.grid(row=0, column=0, columnspan=2, padx=0, pady=20, sticky=N)
    title.config(font=("Small fonts", 25, "bold"),
                 bg='#E1CCCE', relief=RIDGE, foreground="#009912")
    chronometre = Label(window, text=" ")
    chronometre.grid(row=0, column=0, columnspan=2,
                     padx=40, pady=80, sticky=NE)
    chronometre.config(font=("Small fonts", 20), bg='#E1CCCE', relief=RIDGE)
    # Finding times
    with open(str(e_path), "r") as file:
        l_score = [tuple(map(int, line.strip().split(',')))
                   for line in file if line.strip()]
    # Sorts according to the best times
    l_score.sort(key=lambda x: x[0] * 60 + x[1])
    # Record display
    record = Label(window, text='\n'.join(
        [f' Record: {temps_info[0]} min et {temps_info[1]} sec ' if temps_info[0] > 0 else f' Record: {temps_info[1]} sec ' for i, temps_info in enumerate(l_score[:1], 1)]))
    record.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky=NE)
    record.config(font=("Small fonts", 17), bg='#E1CCCE', relief=RIDGE)

    mine_nb = Label(window, text=" Bombes : 12 ")
    mine_nb.grid(row=0, column=0, columnspan=2,
                 padx=15, pady=15, sticky=NW)
    mine_nb.config(font=("Small fonts", 14), bg='#E1CCCE', relief=RIDGE)

    nb_remaining_cell = Label(window, text=" Cases restantes : 52 ")
    nb_remaining_cell.grid(
        row=0, column=0, columnspan=2, padx=15, pady=50, sticky=NW)
    nb_remaining_cell.config(
        font=("Small fonts", 15), bg='#E1CCCE', relief=RIDGE)

    if language == 'english':
        title.config(text=' - EASY - ')
        mine_nb.config(text=' Mines : 12 ')
        nb_remaining_cell.config(text=' Cell left : 52 ')

## ----- Launcher -----##
    for x in range(8):
        for y in range(8):
            c = Cell_e(x, y)
            c.create_cell_btn()
            c.btn_cell.grid(column=x, row=y)  # Grid Creation
    random_mine()
    update_time()
    window.mainloop()
