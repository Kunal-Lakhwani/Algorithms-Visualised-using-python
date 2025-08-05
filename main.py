import tkinter as tk
from tkinter import ttk
from VacuumWorld.VacuumWorld import BFS, DFS, IDS
from GraphTraversal.GraphTraversal import GreedyBFS, AStar
from LocalSearch.HillClimbing import start_climbing
from LocalSearch.Evolutionary import Evolutionary
from AdversarialSearch.MinMax import start_game

Uninformed = [
    ("BFS", BFS),
    ("DFS", DFS),
    ("IDS", IDS),
]

Informed = [
    ("GreedyBFS", GreedyBFS),
    ("A*", AStar)
]

Local = [
    ("Hill Climbing", start_climbing),
    ("Evolutionary", Evolutionary)
]

AdversarialSearch = [
    ("Min-Max", start_game)
]

def add_to_menu(sidebar_frame:tk.Frame, title:str, Algorithms:list, change_program_callback):
    lbl = ttk.Label(sidebar_frame, text=title, font=("Arial", 16), anchor="center")
    lbl.pack(pady=5, fill="x")
    for algo in Algorithms:
        lbl, callback = algo
        newbtn = ttk.Button(sidebar_frame, text=lbl, command=lambda cb=callback: change_program_callback(cb))
        newbtn.pack(pady=5)

def create_sidebar(root:tk.Tk, change_program_callback):

    # Create a sidebar frame
    sidebar_frame = tk.Frame(root, width=200, bg="lightgray")
    sidebar_frame.pack(side="left", fill="y")

    # Search problems, Uninformed
    add_to_menu(sidebar_frame, "Uninformed\nSearch", Uninformed, change_program_callback)

    # Search problems, Informed
    add_to_menu(sidebar_frame, "Informed\nSearch", Informed, change_program_callback)
    
    # Local search problems
    add_to_menu(sidebar_frame, "Local\nSearch", Local, change_program_callback)

    # Adversarial search
    add_to_menu(sidebar_frame, "Adversarial\nSearch", AdversarialSearch, change_program_callback)

# Function to create the main display area (Frame)
def create_main_display(root):
    main_frame = tk.Frame(root, bg="black")
    main_frame.pack(side="right", expand=True, fill="both")
    return main_frame


def default(frame:ttk.Frame):
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack(expand=True, fill="both")

root = tk.Tk()
root.title("AI Algorithm Visualiser")
root.state("zoomed")

# Default active program Blank
active_program = default

def change_program(program):
    active_program = program
    active_program(frame)

create_sidebar(root, change_program)

frame = create_main_display(root)

active_program(frame)

root.protocol("WM_DELETE_WINDOW", lambda: exit(0))

root.mainloop()