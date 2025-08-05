import tkinter as tk
from tkinter import ttk, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # For integration of of matplot in Tkinter
from LocalSearch.Chessboard import Chessboard
import random


def GetRandomChildAndFitness(current:Chessboard) -> tuple[Chessboard, int]:
    Queen = random.randint(0,7) # Get random queen to move
    moveTo = random.randint(1,8) # Move to random rank
    while moveTo == current.QueenRanks[Queen]: # Ensure that we aren't simply moving to the same square
        moveTo = random.randint(1,8)

    next = current.simulate_queen_move(Queen, moveTo)
    return (next, next.get_fitness())


def start_climbing(frame:ttk.Frame):
    ClearWidget(frame)

    board = Chessboard([8,8,8,8,8,8,8,8])

    Iterations = list(range(200))

    FitnessList:list[int] = [board.get_fitness()]
    Path = [board]

    current = Path[0]
    best_board = Path[0]
    best_fitness = FitnessList[0]
    for _ in range(len(Iterations)-1):
        current, fitness = GetRandomChildAndFitness(current)
        if fitness < best_fitness:
            best_board = current
            best_fitness = fitness
        FitnessList.append(fitness)
        Path.append(current)

    plt.clf()

    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    ax.plot(Iterations, FitnessList, label=f"{len(Iterations)} random moves", color="red")    
    
    climber = Path[0]
    cur_fitness = FitnessList[0]
    depth = 1
    
    while depth < 200: # go till max depth
        if cur_fitness <= FitnessList[depth]:
            break
        cur_fitness = FitnessList[depth]
        climber = Path[depth]
        depth += 1

    ax.plot(range(0, depth), FitnessList[:depth], label="Hill Climbing", color="#00bb00")

    ax.set_xlabel("Iteration")
    ax.set_ylabel("Attacks")
    ax.set_title("Solving the 8-Queens problem using Hill Climbing algorithm")
    ax.legend()

    graph = FigureCanvasTkAgg(fig, master=frame)
    graph.draw()
    graph_widget = graph.get_tk_widget()
    graph_widget.config(height=frame.winfo_height()*2//3)
    graph_widget.pack(fill="x", expand=1)

    board_display = tk.Canvas(frame, height=frame.winfo_height() - graph_widget.winfo_height(), background="white")
    board_display.pack(fill="x",expand=1)
    board_display.update_idletasks()
    
    board_length = board_display.winfo_height() - 30 # 50 is the space we are
    tile_length = board_length//8
    col_width = board_display.winfo_width() // 2

    yPos = 30
    Board_font = font.Font(family="Arial", size=16)
    # Drawing Best solution
    xPos = (col_width - board_length) // 2
    board_display.create_text(col_width//2, 16, text=f"Best board fitness={best_board.get_fitness()}/28", font=Board_font)
    best_board.draw_board(board_display, xPos, yPos, tile_length)

    # Drawing Hill climber solution
    xPos = (col_width - board_length) // 2 + col_width
    board_display.create_text(col_width//2+col_width, 16, text=f"Hill Climbing fitness={climber.get_fitness()}/28", font=Board_font)
    climber.draw_board(board_display, xPos, yPos, tile_length)
 

def ClearWidget(widget:tk.Widget):
    if(widget.winfo_class() == "Canvas"):
        widget.delete("all")

    for child in widget.winfo_children():
        child.destroy()