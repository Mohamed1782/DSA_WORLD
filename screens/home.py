import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from screens.MainMenu import MainMenuScreen
import pygame  # For button sounds

class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("DSA World")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        # Load background
        bg_path = os.path.join("assets", "background", "home_bg.png")
        bg_image = Image.open(bg_path).resize((800, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(self.master, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Initialize pygame mixer and load button sound
        pygame.mixer.init()
        self.button_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        self.create_buttons()

    def play_sound(self):
        """Play the button click sound"""
        if self.button_sound:
            self.button_sound.play()

    def create_buttons(self):
        button_font = ("Pixel", 20, "bold")

        # Modified buttons to play sound when clicked
        self.start_button = tk.Button(
            self.master, 
            text="Start", 
            font=button_font, 
            bg="#FFD93D", 
            fg="black", 
            command=lambda: [self.play_sound(), self.start_game()]
        )
        
        self.about_button = tk.Button(
            self.master, 
            text="About", 
            font=button_font, 
            bg="#6BCB77", 
            fg="black", 
            command=lambda: [self.play_sound(), self.show_about()]
        )
        
        self.exit_button = tk.Button(
            self.master, 
            text="Exit", 
            font=button_font, 
            bg="#FF6B6B", 
            fg="black", 
            command=lambda: [self.play_sound(), self.master.quit()]
        )

        center_x = 400
        start_y = 300

        self.canvas.create_window(center_x, start_y, window=self.start_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 80, window=self.about_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 160, window=self.exit_button, width=200, height=50)

    def start_game(self):
        self.canvas.destroy()
        self.start_button.destroy()
        self.about_button.destroy()
        self.exit_button.destroy()
        MainMenuScreen(self.master, self.__init__)

    def show_about(self):
        about_win = tk.Toplevel(self.master)
        about_win.title("About DSA World")
        about_win.geometry("600x400")
        about_win.resizable(False, False)

        canvas = tk.Canvas(about_win, width=600, height=400, bg="#F0F0F0")
        canvas.pack(fill="both", expand=True)

        about_text = (
            "DSA World\n"
            "Created by:\n"
            " - Mohamed Zaghloul\n"
            " - Youssef Mohamed \n"
            " - Ahmed Emad\n"
            " - Mohamed Mahmoud\n"
            " - Mazen Mamdouh\n"
            "An interactive way to learn Data Structures"
        )
        canvas.create_text(
            300, 150,
            text=about_text,
            font=("Pixel", 18, "bold"),
            fill="#333333",
            justify="center"
        )

        button_font = ("Pixel", 16, "bold")
        close_btn = tk.Button(
            about_win, 
            text="Close", 
            font=button_font, 
            bg="#FF6B6B", 
            fg="white", 
            command=lambda: [self.play_sound(), about_win.destroy()]
        )
        canvas.create_window(300, 320, window=close_btn, width=120, height=40)