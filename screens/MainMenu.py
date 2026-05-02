import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import importlib.util
import pygame

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import importlib.util
import pygame

from screens.DSAmenu import DSAMenuScreen
from screens.SortingMenu import SortingMenuScreen

class MainMenuScreen:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback
        self.master.title("DSA World - Menu")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        # Load background
        bg_path = os.path.join("assets", "background", "menu_bg.png")
        bg_image = Image.open(bg_path).resize((800, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Initialize button sound
        self.button_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        self.create_buttons()

        # Back to home button (top left)
        self.top_back_button = tk.Button(
            self.master,
            text="← Back",
            font=("Consolas", 12, "bold"),
            bg="#333333",
            fg="white",
            command=self.go_to_home
        )
        self.canvas.create_window(60, 30, window=self.top_back_button)

    def create_buttons(self):
        button_font = ("Pixel", 20, "bold")

        # Buttons
        self.sorting_button = tk.Button(
            self.master,
            text="Sorting Lab",
            font=button_font,
            bg="#FFD93D",
            fg="black",
            command=lambda: self.go_to_sorting_lab()
        )

        self.DSA_button = tk.Button(
            self.master,
            text="DSA Lab",
            font=button_font,
            bg="#9D4EDD",
            fg="black",
            command=lambda: self.go_to_DSA_lab()
        )

        self.back_button = tk.Button(
            self.master,
            text="Back",
            font=button_font,
            bg="#333333",
            fg="white",
            command=self.go_to_home
        )

        center_x = 400
        start_y = 270

        self.canvas.create_window(center_x, start_y + 50, window=self.sorting_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 150, window=self.DSA_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 250, window=self.back_button, width=200, height=50)

    def play_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def go_to_sorting_lab(self):
        self.play_sound()  # Play button sound when navigating
        self.canvas.destroy()
        self.sorting_button.destroy()
        self.DSA_button.destroy()
        self.back_button.destroy()
        SortingMenuScreen(self.master, self.__init__)

    def go_to_DSA_lab(self):
        self.play_sound()  # Play button sound when navigating
        self.canvas.destroy()
        self.sorting_button.destroy()
        self.DSA_button.destroy()
        self.back_button.destroy()
        DSAMenuScreen(self.master, self.__init__)

    def go_to_home(self):
        self.play_sound()  # Play button sound when going back
        self.canvas.destroy()
        self.go_back_callback(self.master)