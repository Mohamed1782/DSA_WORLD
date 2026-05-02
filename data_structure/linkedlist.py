import tkinter as tk
from tkinter import messagebox
import pygame
import os


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node
    
    def delete(self, data):
        cur = self.head
        prev = None
        while cur:
            if cur.data == data:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True
            prev = cur
            cur = cur.next
        return False
    
    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result


class LinkedListGame:
    def __init__(self, root, go_back_callback=None):
        self.ll = LinkedList()
        self.root = root
        self.go_back_callback = go_back_callback
        
        # Initialize sound system
        pygame.mixer.init()
        self.insert_sound = pygame.mixer.Sound(os.path.join("assets", "music", "insert_button.mp3"))
        self.delete_sound = pygame.mixer.Sound(os.path.join("assets", "music", "push_button.mp3"))
        self.menu_sound = pygame.mixer.Sound(os.path.join("assets", "music", "menu_button.mp3"))

        self.root.title("Linked List Visualizer")
        self.root.geometry("800x800")
        self.root.configure(bg="#0a0a0a")

        title_label = tk.Label(root, text="LINKED LIST VISUALIZER",
                               font=("Impact", 28), fg="#00FFFF", bg="#0a0a0a")
        title_label.pack(pady=20)

        self.canvas = tk.Canvas(root, width=760, height=300,
                                bg="#101020", bd=0, highlightthickness=3,
                                highlightbackground="#00FFFF")
        self.canvas.pack(pady=10)

        # Entry and control buttons
        control_frame = tk.Frame(root, bg="#0a0a0a")
        control_frame.pack(pady=20)

        tk.Label(control_frame, text="NODE VALUE:", font=("Consolas", 14),
                 fg="#00FFFF", bg="#0a0a0a").grid(row=0, column=0, padx=10)

        self.entry = tk.Entry(control_frame, font=("Consolas", 14), width=10,
                              bg="#101020", fg="#FFFFFF", insertbackground="#00FFFF")
        self.entry.grid(row=0, column=1, padx=10)

        # Create buttons with sounds
        self.create_button("INSERT", self.insert, self.insert_sound, 0, control_frame)
        self.create_button("DELETE", self.delete, self.delete_sound, 1, control_frame)
        self.create_button("REFRESH", self.refresh, self.insert_sound, 2, control_frame)

        # Back button
        if self.go_back_callback:
            tk.Button(root, text="← BACK", 
                      command=lambda: [self.menu_sound.play(), self.go_back()],
                      font=("Consolas", 12), bg="#440000", fg="#FFFFFF",
                      activebackground="#FF0000", activeforeground="#FFFFFF",
                      relief=tk.RAISED, bd=2, width=8, cursor="hand2"
                      ).place(x=20, y=20)

        # Instructions
        instr_frame = tk.Frame(root, bg="#0a0a0a")
        instr_frame.pack(pady=10)
        instructions = tk.Label(instr_frame,
                                text="HOW TO USE:\n"
                                     "• Enter a value and click INSERT to add a node\n"
                                     "• Enter a value and click DELETE to remove it\n"
                                     "• Click REFRESH to redraw the visualization",
                                font=("Consolas", 10), fg="#00FFFF", bg="#0a0a0a",
                                justify=tk.LEFT)
        instructions.pack()

        # Initial draw
        self.draw()

    def create_button(self, text, command, sound, col, frame):
        tk.Button(frame, text=text, 
                 command=lambda: [sound.play(), command()],
                 font=("Consolas", 12, "bold"),
                 bg="#101020", fg="#00FFFF",
                 activebackground="#00FFFF", activeforeground="#000000",
                 width=10, height=1, bd=2, relief=tk.RAISED,
                 cursor="hand2").grid(row=1, column=col, padx=10, pady=10)

    def insert(self):
        data = self.entry.get()
        if data:
            self.ll.insert_end(data)
            self.entry.delete(0, tk.END)
            self.draw()
            self.animate_insert()

    def delete(self):
        data = self.entry.get()
        if self.ll.delete(data):
            self.entry.delete(0, tk.END)
            self.draw()
        else:
            messagebox.showinfo("Not Found", f"Value '{data}' not found in list.")

    def refresh(self):
        """Clears the linked list and redraws the canvas"""
        self.ll.head = None
        self.draw()

    def animate_insert(self):
        nodes = self.ll.to_list()
        if not nodes:
            return

        x = 20 + (len(nodes) - 1) * 100
        for _ in range(3):
            self.canvas.itemconfig("last_node", fill="#00FF00")
            self.canvas.update()
            self.root.after(100)
            self.canvas.itemconfig("last_node", fill="#4040FF")
            self.canvas.update()
            self.root.after(100)

    def draw(self):
        self.canvas.delete("all")
        nodes = self.ll.to_list()

        # Grid lines
        for i in range(0, 760, 20):
            self.canvas.create_line(i, 0, i, 300, fill="#1A1A3A", width=1)
        for i in range(0, 300, 20):
            self.canvas.create_line(0, i, 760, i, fill="#1A1A3A", width=1)

        if not nodes:
            self.canvas.create_text(380, 150, text="EMPTY LIST",
                                    font=("Impact", 24), fill="#444444")
            return

        x = 20
        for i, data in enumerate(nodes):
            tag = "last_node" if i == len(nodes) - 1 else f"node_{i}"
            self.canvas.create_rectangle(x, 100, x + 80, 180,
                                         fill="#4040FF", outline="#00FFFF", width=2,
                                         tags=tag)

            # 3D shading
            self.canvas.create_line(x+3, 177, x+77, 177, fill="#000080", width=3)
            self.canvas.create_line(x+77, 103, x+77, 177, fill="#000080", width=3)

            self.canvas.create_text(x + 40, 140, text=data,
                                    font=("Consolas", 16, "bold"), fill="#FFFFFF")

            if i < len(nodes) - 1:
                self.canvas.create_line(x + 80, 140, x + 100, 140,
                                        fill="#00FFFF", width=3)
                self.canvas.create_polygon(x + 95, 135, x + 100, 140, x + 95, 145,
                                           fill="#00FFFF", outline="#00FFFF")
            x += 100

    def go_back(self):
        # Clear the current screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Call the go_back_callback to return to menu
        if self.go_back_callback:
            from screens.DSAmenu import DSAMenuScreen
            DSAMenuScreen(self.root, self.go_back_callback)
