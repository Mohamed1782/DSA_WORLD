import tkinter as tk
import time
import pygame
import os

class QueueGame:
    def __init__(self, root, go_back_callback=None):
        self.root = root
        self.master = root
        self.go_back_callback = go_back_callback
        
        # Initialize sound system
        pygame.mixer.init()
        self.push_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.menu_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        self.root.title("Queue Game")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=800, bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.back_button = tk.Button(root, text="← Back", font=('Consolas', 12, "bold"),
                                     bg="#313244", fg="white", 
                                     command=lambda: [self.menu_sound.play(), self.back_to_menu()])
        self.canvas.create_window(60, 30, window=self.back_button)

        self.queue = []
        self.box_size = 60
        self.gap = 15
        self.y = 280

        self.entry = tk.Entry(root, font=('Consolas', 14), width=10, bg="#cdd6f4", fg="black", justify='center')
        self.canvas.create_window(270, 600, window=self.entry)

        self.enqueue_button = tk.Button(root, text="Enqueue", font=('Consolas', 12, "bold"),
                                        bg="#89b4fa", fg="black", 
                                        command=lambda: [self.push_sound.play(), self.enqueue()])
        self.canvas.create_window(430, 600, window=self.enqueue_button)

        self.dequeue_button = tk.Button(root, text="Dequeue", font=('Consolas', 12, "bold"),
                                        bg="#f38ba8", fg="black", 
                                        command=lambda: [self.push_sound.play(), self.dequeue()], 
                                        state=tk.DISABLED)
        self.canvas.create_window(530, 600, window=self.dequeue_button)

        self.title_text = self.canvas.create_text(400, 80, text="QUEUE VISUALIZER",
                                                  font=("Consolas", 28, "bold"),
                                                  fill="#cba6f7")

    def draw_queue(self):
        self.canvas.delete("queue")
        total_width = len(self.queue) * (self.box_size + self.gap) - self.gap
        start_x = (800 - total_width) // 2

        for i, value in enumerate(self.queue):
            x = start_x + i * (self.box_size + self.gap)
            self.canvas.create_rectangle(x, self.y, x + self.box_size, self.y + self.box_size,
                                         fill="#a6e3a1", outline="#94e2d5", width=4, tags="queue")
            self.canvas.create_text(x + self.box_size / 2, self.y + self.box_size / 2,
                                    text=value, font=('Consolas', 16, "bold"), fill="black", tags="queue")

            if i == 0:
                self.canvas.create_text(x + self.box_size / 2, self.y - 30,
                                        text="FRONT", fill="#f38ba8",
                                        font=("Consolas", 12, "bold"), tags="queue")
                self.canvas.create_polygon(
                    x + self.box_size / 2 - 5, self.y - 15,
                    x + self.box_size / 2 + 5, self.y - 15,
                    x + self.box_size / 2, self.y - 5,
                    fill="#f38ba8", tags="queue"
                )

            if i == len(self.queue) - 1:
                self.canvas.create_text(x + self.box_size / 2, self.y + self.box_size + 30,
                                        text="REAR", fill="#89b4fa",
                                        font=("Consolas", 12, "bold"), tags="queue")
                self.canvas.create_polygon(
                    x + self.box_size / 2 - 5, self.y + self.box_size + 15,
                    x + self.box_size / 2 + 5, self.y + self.box_size + 15,
                    x + self.box_size / 2, self.y + self.box_size + 5,
                    fill="#89b4fa", tags="queue"
                )

    def animate_enqueue(self, value, target_index):
        total_width = (target_index + 1) * (self.box_size + self.gap) - self.gap
        target_x = (800 - total_width) // 2 + target_index * (self.box_size + self.gap)
        x = 10
        y = self.y
        box = self.canvas.create_rectangle(x, y, x + self.box_size, y + self.box_size,
                                           fill="#fab387", outline="#f9e2af", width=4, tags="queue")
        text = self.canvas.create_text(x + self.box_size / 2, y + self.box_size / 2,
                                       text=value, font=('Consolas', 16, "bold"), fill="black", tags="queue")

        while x < target_x:
            self.canvas.move(box, 5, 0)
            self.canvas.move(text, 5, 0)
            self.canvas.update()
            x += 5
            time.sleep(0.008)

    def enqueue(self):
        value = self.entry.get().strip()
        if not value:
            return
        self.entry.delete(0, tk.END)
        self.animate_enqueue(value, len(self.queue))
        self.queue.append(value)
        self.draw_queue()
        self.update_buttons()

    def dequeue(self):
        if not self.queue:
            return
        self.draw_queue()
        total_width = len(self.queue) * (self.box_size + self.gap) - self.gap
        start_x = (800 - total_width) // 2
        x = start_x
        y = self.y

        box = self.canvas.create_rectangle(x, y, x + self.box_size, y + self.box_size,
                                           fill="#f38ba8", outline="#eba0ac", width=4, tags="queue")
        text = self.canvas.create_text(x + self.box_size / 2, y + self.box_size / 2,
                                       text=self.queue[0], font=('Consolas', 16, "bold"), fill="black", tags="queue")

        for _ in range(20):
            self.canvas.move(box, -5, 0)
            self.canvas.move(text, -5, 0)
            self.canvas.update()
            time.sleep(0.008)

        self.queue.pop(0)
        self.draw_queue()
        self.update_buttons()

    def update_buttons(self):
        self.dequeue_button.config(state=tk.NORMAL if self.queue else tk.DISABLED)

    def back_to_menu(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Return to menu
        if self.go_back_callback:
            from screens.DSAmenu import DSAMenuScreen
            DSAMenuScreen(self.master, self.go_back_callback)