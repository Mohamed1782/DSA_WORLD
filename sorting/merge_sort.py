import tkinter as tk
from tkinter import messagebox
import random
import time
import pygame
import os
from sorting.timer import SortingTimer

class MergeSortGame:
    def __init__(self, master, go_back_callback):
        self.master = master
        self.go_back_callback = go_back_callback

        # Initialize sound system
        pygame.mixer.init()
        self.button_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.back_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        # Destroy previous widgets
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.title("DSA World - Merge Sort")
        self.master.geometry("800x900")
        self.master.resizable(False, False)

        # Color palette
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

        # Sorting state
        self.array = []
        self.array_colors = []
        self.sorting = False
        self.sorted_indices = set()
        self.timer = SortingTimer()

        self.create_ui()
        self.generate_random_array()

    def play_button_sound(self):
        """Play the regular button click sound"""
        self.button_sound.play()

    def play_back_sound(self):
        """Play the special back button sound"""
        self.back_sound.play()

    def create_ui(self):
        """Create the user interface"""
        self.main_frame = tk.Frame(self.master, bg=self.COLORS["black"])
        self.main_frame.pack(fill="both", expand=True)

        # Title
        title_label = tk.Label(
            self.main_frame,
            text="MERGE SORT VISUALIZER",
            font=("Courier", 24, "bold"),
            bg=self.COLORS["black"],
            fg=self.COLORS["cyan"],
            pady=20
        )
        title_label.pack()

        # Canvas for visualization
        self.canvas_frame = tk.Frame(
            self.main_frame,
            bg=self.COLORS["black"],
            bd=2,
            relief=tk.RIDGE
        )
        self.canvas_frame.pack(padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=700,
            height=300,
            bg=self.COLORS["black"],
            bd=0,
            highlightthickness=2,
            highlightbackground=self.COLORS["cyan"]
        )
        self.canvas.pack(padx=10, pady=10)

        # Timer display
        self.timer_label = tk.Label(
            self.main_frame,
            text="Time: 00:00.00",
            font=("Courier", 16, "bold"),
            bg=self.COLORS["black"],
            fg=self.COLORS["yellow"],
            pady=5
        )
        self.timer_label.pack()

        # Custom input frame
        input_frame = tk.Frame(self.main_frame, bg=self.COLORS["black"], pady=10)
        input_frame.pack()

        input_label = tk.Label(
            input_frame,
            text="Enter array (comma-separated):",
            font=("Courier", 10),
            bg=self.COLORS["black"],
            fg=self.COLORS["white"]
        )
        input_label.grid(row=0, column=0, padx=10)

        self.array_input = tk.Entry(
            input_frame,
            font=("Courier", 10),
            width=30,
            bg=self.COLORS["dark_blue"],
            fg=self.COLORS["white"],
            insertbackground=self.COLORS["cyan"]
        )
        self.array_input.grid(row=0, column=1, padx=10)
        self.array_input.insert(0, "50, 30, 70, 20, 80")

        self.load_array_button = tk.Button(
            input_frame,
            text="LOAD",
            font=("Courier", 10, "bold"),
            bg=self.COLORS["blue"],
            fg=self.COLORS["white"],
            padx=10,
            pady=3,
            command=lambda: [self.play_button_sound(), self.load_custom_array()]
        )
        self.load_array_button.grid(row=0, column=2, padx=10)

        # Control buttons frame
        button_frame = tk.Frame(self.main_frame, bg=self.COLORS["black"], pady=15)
        button_frame.pack()

        self.generate_button = tk.Button(
            button_frame,
            text="GENERATE",
            font=("Courier", 12, "bold"),
            bg=self.COLORS["blue"],
            fg=self.COLORS["white"],
            padx=15,
            pady=5,
            command=lambda: [self.play_button_sound(), self.generate_random_array()]
        )
        self.generate_button.grid(row=0, column=0, padx=8)

        self.sort_button = tk.Button(
            button_frame,
            text="SORT",
            font=("Courier", 12, "bold"),
            bg=self.COLORS["green"],
            fg=self.COLORS["black"],
            padx=15,
            pady=5,
            command=lambda: [self.play_button_sound(), self.start_sort()]
        )
        self.sort_button.grid(row=0, column=1, padx=8)

        self.reset_button = tk.Button(
            button_frame,
            text="RESET",
            font=("Courier", 12, "bold"),
            bg=self.COLORS["purple"],
            fg=self.COLORS["white"],
            padx=15,
            pady=5,
            command=lambda: [self.play_button_sound(), self.reset()]
        )
        self.reset_button.grid(row=0, column=2, padx=8)

        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="Ready to sort",
            font=("Courier", 12),
            bg=self.COLORS["black"],
            fg=self.COLORS["green"],
            pady=10
        )
        self.status_label.pack()

        # Instructions
        instruction_text = (
            "INSTRUCTIONS:\n"
            "1. Click GENERATE to create a random array\n"
            "2. Click SORT to start the merge sort visualization\n"
            "3. Watch the divide-and-conquer process in action"
        )

        instructions_label = tk.Label(
            self.main_frame,
            text=instruction_text,
            font=("Courier", 10),
            bg=self.COLORS["black"],
            fg=self.COLORS["yellow"],
            justify="left",
            pady=10
        )
        instructions_label.pack()

        # Back button
        self.back_button = tk.Button(
            self.main_frame,
            text="Back to Menu",
            font=("Courier", 12, "bold"),
            bg=self.COLORS["dark_blue"],
            fg=self.COLORS["white"],
            padx=20,
            pady=5,
            command=lambda: [self.play_back_sound(), self.go_back()]
        )
        self.back_button.pack(pady=15)

    def update_timer_display(self):
        """Update the timer display during sorting"""
        if self.timer.is_running:
            elapsed = self.timer.get_elapsed()
            formatted_time = self.timer.format_time(elapsed)
            self.timer_label.config(text=f"Time: {formatted_time}")
            self.master.update()

    def generate_random_array(self):
        """Generate a random array for sorting"""
        if self.sorting:
            messagebox.showwarning("Busy", "Wait for the current sort to finish!")
            return
        
        self.array = [random.randint(10, 100) for _ in range(20)]
        self.array_colors = [self.COLORS["light_blue"] for _ in self.array]
        self.sorted_indices = set()
        self.timer.reset()
        self.timer_label.config(text="Time: 00:00.00")
        self.status_label.config(text="Array generated! Ready to sort.", fg=self.COLORS["green"])
        self.draw_array()

    def load_custom_array(self):
        """Load a custom array from user input"""
        if self.sorting:
            messagebox.showwarning("Busy", "Wait for the current sort to finish!")
            return
        
        input_text = self.array_input.get().strip()
        
        if not input_text:
            messagebox.showwarning("Input Error", "Please enter array values!")
            return
        
        try:
            # Parse comma-separated values
            self.array = [int(x.strip()) for x in input_text.split(",")]
            
            if len(self.array) == 0:
                messagebox.showwarning("Input Error", "Please enter at least one value!")
                return
            
            # Validate array values are positive
            if any(x < 0 for x in self.array):
                messagebox.showwarning("Input Error", "Please use positive numbers only!")
                return
            
            self.array_colors = [self.COLORS["light_blue"] for _ in self.array]
            self.sorted_indices = set()
            self.timer.reset()
            self.timer_label.config(text="Time: 00:00.00")
            self.status_label.config(text=f"Custom array loaded! {len(self.array)} elements. Ready to sort.", fg=self.COLORS["green"])
            self.draw_array()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers separated by commas!\nExample: 50, 30, 70, 20, 80")

    def draw_array(self):
        """Draw the current state of the array"""
        self.canvas.delete("all")

        if not self.array:
            return

        canvas_width = 700
        canvas_height = 300
        bar_width = canvas_width / len(self.array)
        max_value = max(self.array) if self.array else 1

        for i, value in enumerate(self.array):
            x1 = i * bar_width
            x2 = (i + 1) * bar_width
            bar_height = (value / max_value) * (canvas_height - 40)
            y1 = canvas_height - bar_height
            y2 = canvas_height

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=self.array_colors[i],
                outline=self.COLORS["white"],
                width=1
            )

            # Draw value text for small arrays
            if len(self.array) <= 20:
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    y2 + 15,
                    text=str(value),
                    fill=self.COLORS["white"],
                    font=("Courier", 8)
                )

        self.master.update()

    def start_sort(self):
        """Start the merge sort animation"""
        if not self.array:
            messagebox.showwarning("Empty Array", "Please generate an array first!")
            return

        if self.sorting:
            messagebox.showwarning("Busy", "Sort is already in progress!")
            return

        self.sorting = True
        self.sort_button.config(state="disabled")
        self.generate_button.config(state="disabled")
        self.reset_button.config(state="disabled")

        self.status_label.config(text="Sorting in progress...", fg=self.COLORS["yellow"])
        
        # Start timer
        self.timer.reset()
        self.timer.start()
        
        # Make a copy for sorting and track indices
        self.array_copy = self.array.copy()
        self.merge_sort_animate(0, len(self.array_copy) - 1, "Dividing...")

        # Stop timer
        self.timer.stop()

        # Mark all as sorted
        self.array_colors = [self.COLORS["green"] for _ in self.array_colors]
        self.draw_array()

        total_time = self.timer.format_time(self.timer.get_total_time())
        self.timer_label.config(text=f"Time: {total_time}")
        self.status_label.config(text=f"Sorting complete! Total time: {total_time}", fg=self.COLORS["green"])
        self.sorting = False
        self.sort_button.config(state="normal")
        self.generate_button.config(state="normal")
        self.reset_button.config(state="normal")

    def merge_sort_animate(self, left, right, phase):
        """Recursive merge sort with animation"""
        if left < right:
            mid = (left + right) // 2

            # Highlight dividing range
            self.highlight_range(left, right, self.COLORS["orange"])
            self.status_label.config(text=f"Dividing: [{left}, {right}]", fg=self.COLORS["orange"])
            self.update_timer_display()
            time.sleep(0.2)

            # Recursively sort left half
            self.merge_sort_animate(left, mid, "Left")

            # Recursively sort right half
            self.merge_sort_animate(mid + 1, right, "Right")

            # Merge the two halves
            self.merge_animate(left, mid, right)

    def merge_animate(self, left, mid, right):
        """Merge two sorted subarrays with animation"""
        left_arr = self.array_copy[left:mid+1]
        right_arr = self.array_copy[mid+1:right+1]

        i = j = 0
        k = left

        # Highlight merging range
        self.highlight_range(left, right, self.COLORS["purple"])
        self.status_label.config(text=f"Merging: [{left}, {mid}] + [{mid+1}, {right}]", fg=self.COLORS["purple"])
        self.update_timer_display()
        time.sleep(0.1)

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                self.array_copy[k] = left_arr[i]
                i += 1
            else:
                self.array_copy[k] = right_arr[j]
                j += 1
            k += 1

            # Update visualization
            self.array = self.array_copy.copy()
            self.highlight_range(left, right, self.COLORS["cyan"])
            self.draw_array()
            self.update_timer_display()
            time.sleep(0.05)

        while i < len(left_arr):
            self.array_copy[k] = left_arr[i]
            self.array = self.array_copy.copy()
            self.highlight_range(left, right, self.COLORS["cyan"])
            self.draw_array()
            self.update_timer_display()
            i += 1
            k += 1
            time.sleep(0.05)

        while j < len(right_arr):
            self.array_copy[k] = right_arr[j]
            self.array = self.array_copy.copy()
            self.highlight_range(left, right, self.COLORS["cyan"])
            self.draw_array()
            self.update_timer_display()
            j += 1
            k += 1
            time.sleep(0.05)

    def highlight_range(self, left, right, color):
        """Highlight a range of array elements"""
        for i in range(len(self.array_colors)):
            if left <= i <= right:
                self.array_colors[i] = color
            elif i not in self.sorted_indices:
                self.array_colors[i] = self.COLORS["light_blue"]

    def reset(self):
        """Reset the visualizer"""
        if self.sorting:
            messagebox.showwarning("Busy", "Wait for the current sort to finish!")
            return

        self.array = []
        self.array_colors = []
        self.sorted_indices = set()
        self.timer.reset()
        self.timer_label.config(text="Time: 00:00.00")
        self.status_label.config(text="Reset complete. Generate a new array.", fg=self.COLORS["cyan"])
        self.draw_array()

    def go_back(self):
        """Go back to the previous menu"""
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()
        
        # Call the go_back_callback to return to menu
        if self.go_back_callback:
            from screens.SortingMenu import SortingMenuScreen
            SortingMenuScreen(self.master, self.go_back_callback)
