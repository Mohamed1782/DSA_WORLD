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

class DSAMenuScreen:
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
            command=self.go_to_mainMenu
        )
        self.canvas.create_window(60, 30, window=self.top_back_button)

    def create_buttons(self):
        button_font = ("Pixel", 20, "bold")

        # Buttons
        self.stack_button = tk.Button(
            self.master,
            text="Stack",
            font=button_font,
            bg="#FFD93D",
            fg="black",
            command=lambda: self.select_option("Stack")
        )

        self.queue_button = tk.Button(
            self.master,
            text="Queue",
            font=button_font,
            bg="#6BCB77",
            fg="black",
            command=lambda: self.select_option("Queue")
        )

        self.circular_queue_button = tk.Button(
            self.master,
            text="Circular Queue",
            font=button_font,
            bg="#4D96FF",
            fg="black",
            command=lambda: self.select_option("Circular Queue")
        )

        self.linked_list_button = tk.Button(
            self.master,
            text="Linked List",
            font=button_font,
            bg="#FF6B6B",
            fg="black",
            command=lambda: self.select_option("Linked List")
        )

        self.hanoi_button = tk.Button(
            self.master,
            text="Hanoi Tower",
            font=button_font,
            bg="#9D4EDD",
            fg="black",
            command=lambda: self.select_option("Hanoi Tower")
        )

        self.back_button = tk.Button(
            self.master,
            text="Back",
            font=button_font,
            bg="#333333",
            fg="white",
            command=self.go_to_mainMenu
        )

        center_x = 400
        start_y = 270

        self.canvas.create_window(center_x, start_y, window=self.stack_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 80, window=self.queue_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 160, window=self.circular_queue_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 240, window=self.linked_list_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 320, window=self.hanoi_button, width=200, height=50)
        self.canvas.create_window(center_x, start_y + 400, window=self.back_button, width=200, height=50)

    def play_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def select_option(self, option):
        self.play_sound()  # Play button sound when selecting an option

        if option == "Queue":
            spec = importlib.util.spec_from_file_location("queue_module", os.path.join("data_structure", "queue.py"))
            queue_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(queue_module)
            self.canvas.destroy()
            queue_module.QueueGame(self.master, go_back_callback=self.go_back_callback)
        elif option == "Stack":
            spec = importlib.util.spec_from_file_location("stack_module", os.path.join("data_structure", "stack.py"))
            stack_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(stack_module)
            self.canvas.destroy()
            stack_module.StackGame(self.master, go_back_callback=self.go_back_callback)
        elif option == "Linked List":
            spec = importlib.util.spec_from_file_location("linked_list_module", os.path.join("data_structure", "linkedlist.py"))
            linked_list_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(linked_list_module)
            self.canvas.destroy()
            linked_list_module.LinkedListGame(self.master, go_back_callback=self.go_back_callback)
        elif option == "Circular Queue":
            spec = importlib.util.spec_from_file_location("circular_queue_module", os.path.join("data_structure", "CircularQueue.py"))
            circular_queue_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(circular_queue_module)
            self.canvas.destroy()
            circular_queue_module.CircularQueue(self.master, go_back_callback=self.go_back_callback)
        elif option == "Hanoi Tower":
            spec = importlib.util.spec_from_file_location("hanoi_module", os.path.join("data_structure", "HanoiTower.py"))
            hanoi_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hanoi_module)
            self.canvas.destroy()
            hanoi_module.TowerOfHanoiApp(self.master, go_back_callback=self.go_back_callback)

    def go_to_mainMenu(self):
        self.play_sound()  # Play button sound when going back
        self.canvas.destroy()
        self.go_back_callback(self.master, self.__init__)