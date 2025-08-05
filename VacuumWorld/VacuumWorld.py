import tkinter as tk
from tkinter import ttk, font
from VacuumWorld.worldDS import world

# Settings for node appearance
BUTTON_HALF_WIDTH = 10
CANVAS_PADDING = 50

def create_title_label(canvas:tk.Canvas, title:str):
    canvas.update_idletasks()
    titleFont = font.Font(family="Arial", size=20)
    lbl = tk.Label(canvas, text=title, font=titleFont)
    xVal = (canvas.winfo_width() - titleFont.measure(title)) * 0.5
    lbl.place(x=xVal, y=10)

def create_button_node(canvas:tk.Canvas, state_data:world, node, x, y, bgcolor, forecolor="black"):
    button = tk.Button(canvas, text=str(node), bg=bgcolor, foreground=forecolor, command=lambda: show_actions(state_data))
    button.place(x=x - BUTTON_HALF_WIDTH, y=y - BUTTON_HALF_WIDTH, width=BUTTON_HALF_WIDTH * 2, height=BUTTON_HALF_WIDTH * 2)

def expand_world(node:world, max_width:int) -> list[world]:
    avail_dirs = node.get_moves()
    col_width = max_width // len(avail_dirs)
    children = []
    for dir in avail_dirs:
        col_start = node.col_start + ((col_width * len(children)) if len(children) > 0 else 0)
        nodeX = col_start + col_width // 2
        nodeY = node.y + 50
        children.append(node.simulate_move_and_clean(dir, nodeX, nodeY, col_start, col_width))
    
    return children

def show_actions(node:world):
    states = [node]
    actions = [node.previous_act]
    prev = node.parent
    while prev:
        states.append(prev)
        actions.append(prev.previous_act)
        prev = prev.parent

    actions.pop()
    states.reverse()
    actions.reverse()
    new_window = tk.Tk() 
    tile_size = 40   
    world_height = tile_size * node.height
    # Height = (Height of 1 world state + padding) * number of actions
    height = (world_height + 50) * len(states)
    width = tile_size * node.width
    new_window.geometry(f"{width}x{height}+0+0")
    canvas = tk.Canvas(new_window, width=width, height=height, bg="white")
    canvas.pack(fill="both", expand=True)
    yVal = 20
    for idx, state in enumerate(states):
        state.draw_world(canvas, tile_size, 0, yVal)
        if idx < len(actions):
            lbl = tk.Label(canvas, text=f"Move {actions[idx]}")
            lbl.place(x=0, y=yVal+world_height+15)
        yVal += world_height + 50

    new_window.protocol("WM_DELETE_WINDOW", new_window.destroy)


def draw_node(canvas:tk.Canvas, parent:world, current:world, node_num:int):        
    if current.DirtyCount == 0:        
        # If goal state, draw green button
        create_button_node(canvas, current, node_num, current.x, current.y, "green", "white")
    else:
        # If not goal state draw normal world
        create_button_node(canvas, current, node_num, current.x, current.y, "lightgray")
    
    if current.parent != None:
        canvas.create_line(parent.x, parent.y, current.x, current.y)

# BFS Program (Red)
def BFS(frame:ttk.Frame):
    ClearFrame(frame)
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack()
    create_title_label(canvas, "Uninformed BFS")
    # Create a new Vaccum World. Here we are sure that start is not the goal state, so we don't check.
    rootX = (frame.winfo_width() // 2) - BUTTON_HALF_WIDTH
    start = world(rootX, 100, 0, frame.winfo_width()-CANVAS_PADDING*2)
    create_button_node(canvas, start, 0, start.x, start.y, "lightgray")
    # canvas.create_rectangle(x1, 80, x1, 90, fill="green")
    # We also push the level of the node inside the frontier. This will help us in drawing
    # The nodes on the canvas
    frontier = [start]
    node_num = 1
    visited = []
    goal_not_found = True
    
    while len(frontier) > 0 and goal_not_found:
        parent = frontier.pop(0)
        for current in expand_world(parent, parent.col_width):             
            # Goal state check. If found, retrace steps and output the steps.
            if current.DirtyCount == 0:
                goal_not_found = False

            draw_node(canvas, parent, current, node_num)
            node_num += 1
            if current not in visited:
                visited.append(current)
                frontier.append(current)
    if goal_not_found:
        lbl = tk.Label(canvas, text="No Goal State found", font=("Arial", 16))
        lbl.place(x=200,y=50)

# Depth calculator for DFS
def get_depth(node:world) -> int:
    depth = 0
    while node.parent:
        depth += 1
        node = node.parent
    return depth

# DFS Program
def DFS(frame:ttk.Frame, max_depth=4, mode="DFS"):
    ClearFrame(frame)
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack()
    create_title_label(canvas, f"Uninformed {mode}, maximum depth is {max_depth}")
    # Create a new Vaccum World. Here we are sure that start is not the goal state, so we don't check.
    rootX = (frame.winfo_width() // 2) - BUTTON_HALF_WIDTH
    start = world(rootX, 100, 0, frame.winfo_width()-CANVAS_PADDING*2)
    # We also push the level of the node inside the frontier. This will help us in drawing
    # The nodes on the canvas
    frontier = [start]
    node_num = 0
    goal_not_found = True
    while len(frontier) > 0 and goal_not_found:        
        current = frontier.pop()        
        # Goal state check. If found, retrace steps and output the steps.
        if current.DirtyCount == 0:
            goal_not_found = False

        draw_node(canvas, current.parent, current, node_num)        
        node_num += 1

        if get_depth(current) < max_depth:
            for node in expand_world(current, current.col_width):             
                frontier.append(node)
    
    if goal_not_found and mode == "DFS":
        lbl = tk.Label(frame, text="No Goal State found", font=("Arial", 16))
        lbl.place(x=200,y=50)

    return not goal_not_found

# IDS Program
def IDS(frame:ttk.Frame):
    for i in range(1,6):
        goal_found = DFS(frame, i, mode="IDS")
        if goal_found:
            return
    
    lbl = tk.Label(frame, text="No Goal State found", font=("Arial", 16))
    lbl.place(x=200,y=10)

def ClearFrame(frame:ttk.Frame):
    for widget in frame.winfo_children():
        widget.destroy()