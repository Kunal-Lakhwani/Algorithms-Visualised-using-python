import tkinter as tk
from tkinter import ttk, font
from LocalSearch.Chessboard import Chessboard
from LocalSearch.Genetic import populus
import random

Population = populus(25, 900)
BUTTON_LENGTH = 30
board_length = 0

def create_title_label(canvas:tk.Canvas, title:str):
    canvas.update_idletasks()
    titleFont = font.Font(family="Arial", size=20)
    lbl = tk.Label(canvas, text=title, font=titleFont)
    xVal = (canvas.winfo_width() - titleFont.measure(title)) * 0.5
    lbl.place(x=xVal, y=10)

def place_button(canvas:tk.Canvas, gameboard:tk.Canvas, text:str, x:int, y:int, person:Chessboard, backcolor:str, forecolor:str):
    btn = tk.Button(canvas, text=text, background=backcolor, foreground=forecolor, font=("Arial", 16),
                        command=lambda cvs=gameboard, board=person: display_person(cvs, board))
    btn.place(x=x, y=y, height=BUTTON_LENGTH)
    btn.update_idletasks()
    return btn.winfo_width()

def visualise_generation(canvas:tk.Canvas, gameboards:tk.Canvas, Highlighted_people:list[int], start_y:int=0):
    # initial y(50) + 
    # [generation-1]*[label height (16) + internal padding(4) + Y-padding (20)]
    Highlighted_people.sort()
    coord_y = start_y if start_y > 0 else (50 + (Population.generation-1)*(60+BUTTON_LENGTH))
    tk.Label(canvas, text=f"Generation {Population.generation}", 
             font=("Arial",16), background="white").place(x=10, y=coord_y+10)
    
    coord_y += 40
    # Create first 5 buttons
    for i in range(5):
        backcolor, forecolor = ("#00bb00", "white") if i in Highlighted_people else ("lightgray", "black")
        place_button(canvas, gameboards, f"{i+1}", 10 + i*BUTTON_LENGTH, 
                     coord_y, Population.population[i], backcolor, forecolor)
    
    random_elite_btns = random.sample( Highlighted_people[5:], 5)
    random_elite_btns.sort()
    lbl_font = font.Font(family="Arial", size=14)
    next_x = 10 + BUTTON_LENGTH*5
    prev_btn = -10
    for btn in random_elite_btns:        
        # Edge case to check wether the next random selection is next index
        if btn != prev_btn+1:
            lbl = tk.Label(canvas, text=" . . ", font=lbl_font, background="white")
            lbl.place(x=next_x, y=coord_y)
            lbl.update_idletasks() # To update width 
            next_x += lbl.winfo_width()    
        width = place_button(canvas, gameboards, f"{btn+1}", next_x, coord_y, Population.population[btn], "#00bb00", "white")
        next_x += width  
        prev_btn = btn
    
    # Edge case to check wether last drawn button is 6th last button
    if random_elite_btns[-1] != Population.people_count-6:
        lbl = tk.Label(canvas, text=" . . ", font=lbl_font, background="white")
        lbl.place(x=next_x, y=coord_y)
        lbl.update_idletasks() # To update width 
        next_x += lbl.winfo_width()        

    # Create last 5 buttons
    for i in range( Population.people_count-5, Population.people_count):
        backcolor, forecolor = ("#00bb00", "white") if i in Highlighted_people else ("lightgray", "black")
        width = place_button(canvas, gameboards, f"{i+1}",  next_x, 
                     coord_y, Population.population[i], backcolor, forecolor)
        next_x += width

    
def display_person(canvas:tk.Canvas, person:Chessboard):
    global board_length
    person.draw_board(canvas, 10, 40, board_length//8-5)

def Evolutionary(frame:ttk.Frame):
    ClearWidget(frame)
    global board_length
    board_length = frame.winfo_height()//2 - 40 # Half the height 20 for label and 20 for padding
    board_display = tk.Canvas(frame, bg="white", width=board_length, highlightthickness=0)
    board_display.pack(fill="y", anchor="w", side="left")
    canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    canvas.pack(fill="both", expand=1)
    canvas.update_idletasks()
    board_display.create_text(100, 20, text="Chosen Board", font=("Arial",20))
    board_display.create_text(100, 20+board_length, text="Fittest Board", font=("Arial",20))
    Elites = []
    while Population.generation < 200:
        Elites = Population.get_elites()
        if Population.get_fittest(Elites).get_fitness() == 0:
            break
        # Create buttons to visualise first four generations
        if Population.generation < 5:            
            visualise_generation(canvas, board_display, Elites)
        Population.Evolve(Elites)

    canvas.create_text((canvas.winfo_width()-board_display.winfo_width())/2, 500, text=".\n.\n.\n.\n.\n.\n.\n.\n.", font=("Arial",14))
    visualise_generation(canvas, board_display, Elites, 600)
    Population.get_fittest(Elites).draw_board(board_display, 10, board_length+40, board_length//8-5)


def ClearWidget(widget:tk.Widget):
    if(widget.winfo_class() == "Canvas"):
        widget.delete("all")

    for child in widget.winfo_children():
        child.destroy()