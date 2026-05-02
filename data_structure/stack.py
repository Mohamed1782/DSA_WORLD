import tkinter as tk
from tkinter import messagebox
import random
import time
import pygame
import os

class StackGame:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback

        # Initialize sound system with two different sounds
        pygame.mixer.init()
        self.button_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.back_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("DSA World - Stack")
        self.master.geometry("800x800")
        self.master.resizable(False, False)

        self.MAX_SIZE = 5
        self.stack = []
        self.colors = []

        self.COLORS = {
            "black": "#0D0D0D",
            "dark_blue": "#131B23",
            "blue": "#00498F",
            "light_blue": "#00A1DE",
            "cyan": "#00F0FF",
            "green": "#00FF9D",
            "yellow": "#FFCF00",
            "orange": "#FF8B00",
            "red": "#E72000",
            "purple": "#A91ED8",
            "white": "#FFFFFF"
        }

        self.create_ui()

    def play_button_sound(self):
        """Play the regular button click sound"""
        self.button_sound.play()

    def play_back_sound(self):
        """Play the special back button sound"""
        self.back_sound.play()

    def create_ui(self):
        self.main_frame = tk.Frame(self.master, bg=self.COLORS["black"])
        self.main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="STACK VISUALIZER",
            font=("Courier", 24, "bold"),
            bg=self.COLORS["black"],
            fg=self.COLORS["cyan"],
            pady=20
        )
        title_label.pack()

        self.canvas_frame = tk.Frame(
            self.main_frame,
            bg=self.COLORS["black"],
            bd=2,
            relief=tk.RIDGE
        )
        self.canvas_frame.pack(padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=600,
            height=400,
            bg=self.COLORS["black"],
            bd=0,
            highlightthickness=2,
            highlightbackground=self.COLORS["cyan"]
        )
        self.canvas.pack(padx=10, pady=10)

        input_frame = tk.Frame(self.main_frame, bg=self.COLORS["black"], pady=10)
        input_frame.pack()

        input_label = tk.Label(
            input_frame,
            text="Item:",
            font=("Courier", 14),
            bg=self.COLORS["black"],
            fg=self.COLORS["white"]
        )
        input_label.grid(row=0, column=0, padx=10)

        self.input_entry = tk.Entry(
            input_frame,
            font=("Courier", 14),
            width=15,
            bg=self.COLORS["dark_blue"],
            fg=self.COLORS["white"],
            insertbackground=self.COLORS["cyan"]
        )
        self.input_entry.grid(row=0, column=1, padx=10)

        button_frame = tk.Frame(self.main_frame, bg=self.COLORS["black"], pady=20)
        button_frame.pack()

        self.push_button = tk.Button(
            button_frame,
            text="PUSH",
            font=("Courier", 14, "bold"),
            bg=self.COLORS["blue"],
            fg=self.COLORS["white"],
            padx=20,
            pady=5,
            command=lambda: [self.play_button_sound(), self.push_item()]
        )
        self.push_button.grid(row=0, column=0, padx=10)

        self.pop_button = tk.Button(
            button_frame,
            text="POP",
            font=("Courier", 14, "bold"),
            bg=self.COLORS["red"],
            fg=self.COLORS["white"],
            padx=20,
            pady=5,
            command=lambda: [self.play_button_sound(), self.pop_item()]
        )
        self.pop_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(
            button_frame,
            text="RESET",
            font=("Courier", 14, "bold"),
            bg=self.COLORS["purple"],
            fg=self.COLORS["white"],
            padx=20,
            pady=5,
            command=lambda: [self.play_button_sound(), self.reset_stack()]
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        self.back_button = tk.Button(
            self.main_frame,
            text="Back to Menu",
            font=("Courier", 14, "bold"),
            bg=self.COLORS["dark_blue"],
            fg=self.COLORS["white"],
            padx=20,
            pady=5,
            command=lambda: [self.play_back_sound(), self.go_back()]
        )
        self.back_button.pack(pady=20)

        self.status_label = tk.Label(
            self.main_frame,
            text="Ready to use the stack",
            font=("Courier", 14),
            bg=self.COLORS["black"],
            fg=self.COLORS["green"],
            pady=10
        )
        self.status_label.pack()

        instruction_text = (
            "INSTRUCTIONS:\n"
            "1. Enter a value and click PUSH to add to stack\n"
            "2. Click POP to remove the top item\n"
            "3. Click RESET to clear the stack"
        )

        instructions_label = tk.Label(
            self.main_frame,
            text=instruction_text,
            font=("Courier", 12),
            bg=self.COLORS["black"],
            fg=self.COLORS["yellow"],
            justify="left",
            pady=10
        )
        instructions_label.pack()

        self.draw_stack()

    def get_random_color(self):
        return random.choice([
            self.COLORS["light_blue"],
            self.COLORS["green"],
            self.COLORS["yellow"],
            self.COLORS["orange"],
            self.COLORS["red"],
            self.COLORS["purple"]
        ])

    def draw_stack(self):
        self.canvas.delete("all")

        container_x = 200
        container_y = 50
        container_width = 200
        container_height = 300

        self.canvas.create_rectangle(
            container_x,
            container_y,
            container_x + container_width,
            container_y + container_height,
            fill=self.COLORS["dark_blue"],
            outline=self.COLORS["cyan"],
            width=3
        )

        self.canvas.create_text(
            container_x + container_width/2,
            container_y - 20,
            text="TOP",
            fill=self.COLORS["cyan"],
            font=("Courier", 16, "bold")
        )

        self.canvas.create_text(
            container_x + container_width/2,
            container_y + container_height + 20,
            text="BOTTOM",
            fill=self.COLORS["cyan"],
            font=("Courier", 16, "bold")
        )

        box_height = 40
        spacing = 10

        for i, item in enumerate(self.stack):
            y_pos = container_y + container_height - (i + 1) * (box_height + spacing)
            color = self.colors[i]

            self.canvas.create_rectangle(
                container_x + 20,
                y_pos,
                container_x + container_width - 20,
                y_pos + box_height,
                fill=color,
                outline=self.COLORS["white"],
                width=2
            )

            self.canvas.create_text(
                container_x + container_width/2,
                y_pos + box_height/2,
                text=item,
                fill=self.COLORS["white"],
                font=("Courier", 14, "bold")
            )

    def push_item(self):
        item = self.input_entry.get().strip()

        if not item:
            messagebox.showwarning("Input Error", "Please enter a value to push.")
            return

        if len(self.stack) >= self.MAX_SIZE:
            self.status_label.config(text="Stack Overflow! Cannot push more items.", fg=self.COLORS["red"])
            messagebox.showerror("Stack Overflow", "The stack is full! Cannot add more items.")
            return

        color = self.get_random_color()
        self.stack.append(item)
        self.colors.append(color)
        self.input_entry.delete(0, tk.END)
        self.animate_push(item, color)
        self.status_label.config(text=f"Pushed: {item}", fg=self.COLORS["green"])

    def pop_item(self):
        if not self.stack:
            self.status_label.config(text="Stack Underflow! Cannot pop from empty stack.", fg=self.COLORS["red"])
            messagebox.showinfo("Stack Underflow", "The stack is empty! Nothing to pop.")
            return

        removed = self.stack.pop()
        color = self.colors.pop()
        self.animate_pop()
        self.status_label.config(text=f"Popped: {removed}", fg=self.COLORS["yellow"])

    def reset_stack(self):
        self.stack.clear()
        self.colors.clear()
        self.status_label.config(text="Stack has been reset", fg=self.COLORS["cyan"])
        self.draw_stack()

    def animate_push(self, item, color):
        box_height = 40
        spacing = 10
        container_x = 200
        container_y = 50
        container_width = 200
        container_height = 300

        index = len(self.stack) - 1
        target_y = container_y + container_height - (index + 1) * (box_height + spacing)

        rect = self.canvas.create_rectangle(
            container_x + 20,
            0,
            container_x + container_width - 20,
            box_height,
            fill=color,
            outline=self.COLORS["white"],
            width=2
        )

        text = self.canvas.create_text(
            container_x + container_width / 2,
            box_height / 2,
            text=item,
            fill=self.COLORS["white"],
            font=("Courier", 14, "bold")
        )

        for y in range(0, target_y, 10):
            self.canvas.move(rect, 0, 10)
            self.canvas.move(text, 0, 10)
            self.canvas.update()
            time.sleep(0.01)

    def animate_pop(self):
        if not self.stack:
            self.draw_stack()
            return

        box_height = 40
        spacing = 10
        container_x = 200
        container_y = 50
        container_width = 200
        container_height = 300

        index = len(self.stack)
        start_y = container_y + container_height - (index + 1) * (box_height + spacing)

        rect = self.canvas.create_rectangle(
            container_x + 20,
            start_y,
            container_x + container_width - 20,
            start_y + box_height,
            fill=self.COLORS["black"],
            outline="",
            width=2
        )

        for _ in range(30):
            self.canvas.move(rect, 0, -10)
            self.canvas.update()
            time.sleep(0.01)

        self.draw_stack()

    def go_back(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Call the go_back_callback to return to menu
        if self.go_back_callback:
            from screens.DSAmenu import DSAMenuScreen
            DSAMenuScreen(self.master, self.go_back_callback)