import tkinter as tk
from tkinter import messagebox, ttk
import math
import random
import time
import pygame
import os

class CircularQueue:
    def __init__(self, root, go_back_callback=None):
        self.root = root
        self.go_back_callback = go_back_callback
        
        # Initialize sound system
        pygame.mixer.init()
        self.push_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.menu_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        self.root.title("Circular Queue Visualizer")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Game-like colors
        self.colors = {
            "background": "#1e1e2e",
            "title": "#f9c846",
            "text": "#ffffff",
            "button": "#89b4fa",
            "button_hover": "#b4befe",
            "node_empty": "#313244",
            "node_filled": "#f38ba8",
            "node_front": "#a6e3a1",
            "node_rear": "#fab387",
            "node_text": "#11111b",
            "highlight": "#cba6f7"
        }
        
        # Queue properties
        self.max_size = 8
        self.queue = [None] * self.max_size
        self.front = -1
        self.rear = -1
        self.animation_speed = 0.5  # seconds
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        self.title_frame = tk.Frame(self.root, bg=self.colors["background"], pady=10)
        self.title_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.title_frame, 
            text="CIRCULAR QUEUE VISUALIZER", 
            font=("Orbitron", 28, "bold"),
            fg=self.colors["title"],
            bg=self.colors["background"],
            pady=10
        )
        self.title_label.pack()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.colors["background"])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas for queue visualization
        self.canvas_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            width=800, 
            height=400,
            bg=self.colors["background"],
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Info display
        self.info_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        self.info_frame.pack(fill=tk.X, pady=10)
        
        self.info_label = tk.Label(
            self.info_frame,
            text="Front: -1 | Rear: -1 | Status: Empty",
            font=("Consolas", 14),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        self.info_label.pack()
        
        # Input frame
        self.input_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Value entry
        self.value_label = tk.Label(
            self.input_frame,
            text="Value:",
            font=("Consolas", 12),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        self.value_label.pack(side=tk.LEFT, padx=5)
        
        self.value_entry = tk.Entry(
            self.input_frame,
            font=("Consolas", 12),
            width=10,
            bg="#313244",
            fg=self.colors["text"],
            insertbackground=self.colors["text"]
        )
        self.value_entry.pack(side=tk.LEFT, padx=5)
        
        # Speed control
        self.speed_label = tk.Label(
            self.input_frame,
            text="Speed:",
            font=("Consolas", 12),
            fg=self.colors["text"],
            bg=self.colors["background"]
        )
        self.speed_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.speed_scale = tk.Scale(
            self.input_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            length=150,
            bg=self.colors["background"],
            fg=self.colors["text"],
            highlightthickness=0,
            troughcolor="#313244",
            activebackground=self.colors["button_hover"],
            command=self.update_speed
        )
        self.speed_scale.set(0.5)
        self.speed_scale.pack(side=tk.LEFT)
        
        # Button frame
        self.button_frame = tk.Frame(self.content_frame, bg=self.colors["background"])
        self.button_frame.pack(fill=tk.X, pady=20)
        
        # Create custom style for buttons
        style = ttk.Style()
        style.configure(
            "Game.TButton",
            font=("Orbitron", 12, "bold"),
            background=self.colors["button"],
            foreground=self.colors["node_text"],
            borderwidth=0,
            focuscolor=self.colors["button_hover"],
            padding=10
        )
        
        # Operation buttons with sound
        buttons = [
            ("ENQUEUE", lambda: [self.push_sound.play(), self.enqueue()]),
            ("DEQUEUE", lambda: [self.push_sound.play(), self.dequeue()]),
            ("RESET", lambda: [self.push_sound.play(), self.reset()]),
            ("RANDOM FILL", lambda: [self.push_sound.play(), self.random_fill()])
        ]
        
        for text, command in buttons:
            btn = ttk.Button(
                self.button_frame,
                text=text,
                command=command,
                style="Game.TButton"
            )
            btn.pack(side=tk.LEFT, padx=10, expand=True)
            
        # Back button with menu sound
        self.back_button = tk.Button(
            self.content_frame,
            text="Back to Menu",
            font=("Courier", 14, "bold"),
            bg="#333333",
            fg="#ffffff",
            padx=20,
            pady=5,
            command=lambda: [self.menu_sound.play(), self.go_back()]
        )
        self.back_button.pack(pady=20)
        
        # Draw initial empty queue
        self.draw_queue()
        
    def update_speed(self, value):
        self.animation_speed = float(value)
        
    def draw_queue(self):
        self.canvas.delete("all")
        
        # Calculate dimensions
        center_x, center_y = 370, 200
        radius = 150
        node_radius = 30
        
        # Draw outer circle (queue boundary)
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline=self.colors["highlight"],
            width=2,
            dash=(3, 5)
        )
        
        # Draw nodes
        for i in range(self.max_size):
            angle = 2 * math.pi * i / self.max_size - math.pi/2
            node_x = center_x + (radius - node_radius) * math.cos(angle)
            node_y = center_y + (radius - node_radius) * math.sin(angle)
            
            # Determine node color
            if self.queue[i] is None:
                color = self.colors["node_empty"]
            else:
                color = self.colors["node_filled"]
                
            # Special coloring for front and rear
            if i == self.front and i == self.rear and self.front != -1:
                color = self.colors["highlight"]  # both front and rear
            elif i == self.front and self.front != -1:
                color = self.colors["node_front"]
            elif i == self.rear and self.rear != -1:
                color = self.colors["node_rear"]
            
            # Draw node circle
            self.canvas.create_oval(
                node_x - node_radius, node_y - node_radius,
                node_x + node_radius, node_y + node_radius,
                fill=color,
                outline="#000000",
                width=2
            )
            
            # Draw index
            self.canvas.create_text(
                node_x, node_y + node_radius + 15,
                text=f"[{i}]",
                fill=self.colors["text"],
                font=("Consolas", 12)
            )
            
            # Draw value if not None
            if self.queue[i] is not None:
                self.canvas.create_text(
                    node_x, node_y,
                    text=str(self.queue[i]),
                    fill=self.colors["node_text"],
                    font=("Consolas", 14, "bold")
                )
        
        # Draw front and rear indicators
        if self.front != -1:
            front_angle = 2 * math.pi * self.front / self.max_size - math.pi/2
            front_x = center_x + (radius + 20) * math.cos(front_angle)
            front_y = center_y + (radius + 20) * math.sin(front_angle)
            
            self.canvas.create_text(
                front_x, front_y,
                text="FRONT",
                fill=self.colors["node_front"],
                font=("Orbitron", 12, "bold")
            )
        
        if self.rear != -1:
            rear_angle = 2 * math.pi * self.rear / self.max_size - math.pi/2
            rear_x = center_x + (radius + 20) * math.cos(rear_angle)
            rear_y = center_y + (radius + 20) * math.sin(rear_angle)
            
            self.canvas.create_text(
                rear_x, rear_y,
                text="REAR",
                fill=self.colors["node_rear"],
                font=("Orbitron", 12, "bold")
            )
            
        # Update info label
        status = "Empty" if self.front == -1 else "Full" if (self.rear + 1) % self.max_size == self.front else "Available"
        self.info_label.config(text=f"Front: {self.front} | Rear: {self.rear} | Status: {status}")

    def is_empty(self):
        return self.front == -1
        
    def is_full(self):
        return (self.rear + 1) % self.max_size == self.front

    def enqueue(self):
        try:
            value = self.value_entry.get()
            if not value:
                messagebox.showwarning("Input Error", "Please enter a value")
                return
                
            if self.is_full():
                messagebox.showwarning("Queue Full", "Cannot enqueue: Queue is full")
                return
                
            # Enqueue operation
            if self.is_empty():
                self.front = 0
                self.rear = 0
            else:
                self.rear = (self.rear + 1) % self.max_size
                
            self.queue[self.rear] = value
            self.value_entry.delete(0, tk.END)
            
            # Animation effect
            self.highlight_operation("enqueue")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def dequeue(self):
        if self.is_empty():
            messagebox.showwarning("Queue Empty", "Cannot dequeue: Queue is empty")
            return
            
        # Save the dequeued value
        value = self.queue[self.front]
        
        # Dequeue operation
        if self.front == self.rear:  # Last element
            self.queue[self.front] = None
            self.front = -1
            self.rear = -1
        else:
            self.queue[self.front] = None
            self.front = (self.front + 1) % self.max_size
            
        messagebox.showinfo("Dequeue", f"Dequeued: {value}")
        
        # Animation effect
        self.highlight_operation("dequeue")

    def random_fill(self):
        self.reset()
        
        # Add random number of elements
        num_elements = random.randint(3, self.max_size - 1)
        
        self.front = 0
        self.rear = -1
        
        for _ in range(num_elements):
            self.rear = (self.rear + 1) % self.max_size
            self.queue[self.rear] = random.randint(1, 99)
            
        self.draw_queue()

    def reset(self):
        self.queue = [None] * self.max_size
        self.front = -1
        self.rear = -1
        self.draw_queue()

    def highlight_operation(self, operation):
        # Flash effect for operations
        original_color = self.canvas.cget("bg")
        
        if operation == "enqueue":
            highlight = self.colors["node_rear"]
        else:
            highlight = self.colors["node_front"]
            
        # Flash effect
        self.canvas.config(bg=highlight)
        self.canvas.update()
        time.sleep(self.animation_speed * 0.3)
        self.canvas.config(bg=original_color)
        
        # Redraw queue
        self.draw_queue()

    def go_back(self):
        # Clear the current screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Call the go_back_callback to return to menu
        if self.go_back_callback:
            from screens.DSAmenu import DSAMenuScreen
            DSAMenuScreen(self.root, self.go_back_callback)

def main():
    root = tk.Tk()
    app = CircularQueue(root)
    root.mainloop()

