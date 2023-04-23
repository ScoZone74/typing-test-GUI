import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import time
import random

from wordlist import super_list


class TyperTester(tk.Frame):
    """Pick up here: https://stackoverflow.com/questions/35667105/python-tkinter-append-list"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.num_wds = 10
        self.master_list = random.choices(super_list, k=self.num_wds)
        self.completed_list = []
        self.timer_on = False

        # Score calculation attributes
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None
        self.char_count = 0
        self.wrong_words = []

        #Initialize user interface
        self.initialize_gui()

    def initialize_gui(self):
        # Create window with tkinter
        self.parent.title("Typer Tester")
        self.parent.minsize(width=500, height=350)
        self.parent.config(padx=25, pady=25, bg="#F5F5B5")
        self.parent.bind("<Key>", self.clock_start)

        # Add ability for window to display selection of typing words
        self.label = tk.Label(self.parent, text=self.master_list)
        self.label.config(font=("Arial", 20), wraplength=750, justify="center")
        self.label.config(background="#F5F5B5")
        self.label.grid(row=0, column=0, columnspan=3)

        # Pressing help_btn opens a popup with help text.
        self.help_btn = tk.Button(self.parent, text="❓", command=self.info)
        self.help_btn.config(bg="#C4FAAD", fg="maroon", width=25)
        self.help_btn.config(border=10)
        self.help_btn.grid(row=2, column=1)

        # Create an entry box where user will type the test words.
        self.user_txt = ttk.Entry(self.parent, font=("Arial, 14"))
        self.user_txt.grid(row=1, column=0, columnspan=3)
        self.user_txt.focus_set()
        self.user_txt.bind("<space>", self.user_words)

    def info(self):
        help_txt = f"""Start typing the words on the screen. The timer starts when
        you start. That's it, really - type a word, hit SPACE, type the next word, 
        hit SPACE... When you've typed {self.num_wds} words, TyperTester
        stops, calculates your score and shows it to you so that you may revel in 
        your mastery, or wallow in your misery, as the case may be. Have fun! 😉"""
        helper = showinfo(title="Instructions", message=help_txt)
        return helper

    def clock_start(self, event=None):
        if not self.timer_on:
            self.start_time = time.time()
            self.timer_on = True

    def user_words(self, event=None):
        # Add user entries to completed_list
        u_wd = self.user_txt.get()
        self.completed_list.append(u_wd.strip())
        if len(self.completed_list) != len(self.master_list):
            self.user_txt.delete(0, "end")
        else:
            self.end_time = time.time()
            self.score_calc()

    def score_calc(self):
        # Calculate user typing speed.
        self.elapsed_time = self.end_time - self.start_time
        for word in self.completed_list:
            self.char_count += len(word)
        for i in range(len(self.master_list)):
            if self.completed_list[i] != self.master_list[i]:
                self.wrong_words.append(self.completed_list[i])
        cpm = self.char_count / self.elapsed_time * 60
        wpm = round((cpm / 5) - len(self.wrong_words))

        # Score display
        self.score_disp = tk.Toplevel(self.parent, background="#C4FAAD")
        self.score_disp.geometry(newGeometry="300x200")
        self.score_disp.focus_set()

        self.score = tk.Label(self.score_disp, text=f"Chars per minute: {wpm}")
        self.score.config(font=("Arial", 20), wraplength=750, justify="center")
        self.score.pack()
