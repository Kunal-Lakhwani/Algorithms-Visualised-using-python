import tkinter as tk
from tkinter import ttk, font
from AdversarialSearch.TicTacToe import board, node

NODE_HALF_WIDTH = 15
MAX_DEPTH = 2
BOARD_LENGTH = 250
TURNOF = ["X", "O"]
ROW_LBL = ["A", "B", "C"]

# Variable for current state of board
GameBoard = board()
turn_number = 1

def create_title_label(canvas:tk.Canvas, title:str):
    canvas.update_idletasks()
    titleFont = font.Font(family="Arial", size=20)
    lbl = tk.Label(canvas, text=title, font=titleFont)
    xVal = (canvas.winfo_width() - titleFont.measure(title)) * 0.5
    lbl.place(x=xVal, y=10)

def expand_moves(state:board, moves:list[tuple[int,int]], turn_of:str) -> list[board]:
    children = []
    for row, col in moves:
        children.append(state.simulate_set_cell(row, col, turn_of))

    return children
        
def draw_centered_label(canvas:tk.Canvas, nodeX:int, nodeY:int, text:str, forecolor="black", fontsize=8):
    lblX = nodeX + NODE_HALF_WIDTH 
    lblY = nodeY + NODE_HALF_WIDTH
    canvas.create_text(lblX, lblY, text=text, fill=forecolor, font=("Arial", fontsize))

def suggest_move(canvas:tk.Canvas, suggestion:str):
    suggestion_font = font.Font(family="Arial", size=20)
    SuggestionLBL = tk.Label(canvas, text=f"Suggestion:\n{suggestion}", foreground="white", background="#00bb00", font=suggestion_font)
    SuggestionLBL.place(x=canvas.winfo_width()//2 - BOARD_LENGTH - 30,y=BOARD_LENGTH//2 - 40)

# 0 means X, 1 means O. Consult TURNOF array
def get_turn_of(turn_num:int) -> int:
    return 1 if turn_num % 2 == 0 else 0

# Creates the tree to be used for min-max search using DFS
def get_tree(canvas_width:int, prev_row:int, prev_col:int, max_depth:int) -> node:    
    col_width = canvas_width - 100
    xPos = col_width // 2 + 50 - NODE_HALF_WIDTH
    yPos = BOARD_LENGTH + 150
    root = node(prev_row, prev_col, col_width, 70, xPos, yPos)
    frontier = [(root, GameBoard, 0)]
    while len(frontier) > 0:
        parent, current_board, depth = frontier.pop()
        current_turn = TURNOF[get_turn_of(turn_number + depth)]

        if depth == max_depth or current_board.IsTerminal():
            continue # If depth is equal to max or current state is terminal, no need to explore children
        
        moves = current_board.GetPossibleMoves()
        col_width = parent.max_width // len(moves)
        xOffset = col_width // 2 - NODE_HALF_WIDTH
        for idx, board in enumerate(expand_moves(current_board, current_board.GetPossibleMoves(), current_turn)):
            row, col = moves[idx]
            col_start = parent.col_start + (0 if idx == 0 else idx * col_width)
            xPos = col_start + xOffset
            yPos = parent.y + 100
            child = node(row, col, col_width, col_start, xPos, yPos)
            parent.addChild(child)
            frontier.append((child, board, depth+1))

    return root

# Draw tree using DFS and display suggested move
def draw_minmax_tree(canvas:tk.Canvas, root:node, max_depth:int) -> tuple[int,int]:
    # clear the canvas the tree is drawn on
    ClearWidget(canvas)
    # Run minmax to get suggested move
    cur_turn = get_turn_of(turn_number)
    suggested_row, suggested_col, util = recursive_minimax(canvas, root, GameBoard, cur_turn, 0, 2)
    suggest_move(canvas, f"{ROW_LBL[suggested_row]}{suggested_col+1}")
    colors = ["#bb0000", "white"]
    frontier = [(root, 0)]
    canvas.create_oval(root.x, root.y, root.x + NODE_HALF_WIDTH * 2, root.y + NODE_HALF_WIDTH * 2, fill=colors[1-cur_turn], tags="node")
    draw_centered_label(canvas, root.x, root.y, f"{ROW_LBL[root.row]}{root.col+1}", colors[cur_turn])
    while len(frontier) > 0:
        parent, depth = frontier.pop()
        turn = get_turn_of(turn_number + depth + 1)        
        for child in parent.children:
            canvas.create_oval(child.x, child.y, child.x + NODE_HALF_WIDTH * 2, child.y + NODE_HALF_WIDTH * 2, fill=colors[1-turn], tags="node")
            canvas.create_line(child.x + NODE_HALF_WIDTH, child.y + NODE_HALF_WIDTH, parent.x + NODE_HALF_WIDTH, parent.y + NODE_HALF_WIDTH, tags="edge")
            draw_centered_label(canvas, child.x, child.y, f"{ROW_LBL[child.row]}{child.col+1}", colors[turn])
            if len(child.children) == 0:                
                continue
            frontier.append((child, depth+1))
    
    for depth in range(max_depth+1):
        text = TURNOF[get_turn_of(turn_number + depth)]
        text += " MAX" if text == "X" else " MIN"
        canvas.create_text(40, BOARD_LENGTH + (depth*100) + 50 + NODE_HALF_WIDTH, text=text, fill="blue", font=("Arial", 12))

    canvas.tag_lower("edge")

def recursive_minimax(canvas:tk.Canvas, current:node, gamestate:board, turn_of:int, cur_depth:int, max_depth:int) -> tuple[int,int,int]:
    if cur_depth == max_depth or gamestate.IsTerminal():
        util = gamestate.GetUtility()
        lblFont = font.Font(family="Arial", size=8)
        lbl = tk.Label(canvas, text=str(util), foreground="white", background="#00bb00", font=lblFont)
        lbl.place(x=current.x + NODE_HALF_WIDTH, y=current.y + NODE_HALF_WIDTH*2 - 8)
        return (
            current.row,
            current.col,
            util
        )
    vals = []
    for child in current.children:
        vals.append(recursive_minimax(canvas, child, gamestate.simulate_set_cell(child.row, child.col, TURNOF[turn_of]), 
                           1-turn_of, cur_depth+1, max_depth))        
    
    retVal=(0,0, 2 if turn_of == 1 else -2)
    for idx, val in enumerate(vals):        
        util = val[2]
        cur_child = current.children[idx]
        # If it is turn of O, we do min function
        if turn_of == 1 and util < retVal[2]:
            retVal = (cur_child.row, cur_child.col, util)
        # If it is turn of X, we do max function
        elif turn_of == 0 and util > retVal[2]:
            retVal = (cur_child.row, cur_child.col, util)
    lblFont = font.Font(family="Arial", size=8)
    lbl = tk.Label(canvas, text=str(retVal[2]), foreground="white", background="#00bb00", font=lblFont)
    lbl.place(x=current.x + NODE_HALF_WIDTH, y=current.y + NODE_HALF_WIDTH*2 - 8)
    return retVal

# Create a new game canvas
def get_game_canvas(canvas:tk.Canvas) -> tk.Canvas:
    game_canvas = tk.Canvas(canvas, width=BOARD_LENGTH, height=BOARD_LENGTH, highlightthickness=0, bg="white")
    game_canvas.place(x=canvas.winfo_width()//2 - BOARD_LENGTH // 2, y=100)
    game_canvas.update_idletasks()
    return game_canvas

def draw_game_board(canvas:tk.Canvas, game_canvas:tk.Canvas, final_board:bool):
    # drawing border lines
    half_border_width = 3
    font_size = 20
    board_padding = font_size*2
    Effective_length = BOARD_LENGTH - board_padding
    offset = Effective_length // 3 - half_border_width
    Board_font = font.Font(family="Arial", size=font_size)

    cur_player = TURNOF[get_turn_of(turn_number)]
    for i in range(1,3):
        game_canvas.create_line(board_padding, i*offset, BOARD_LENGTH, i*offset, width=half_border_width*2)
        game_canvas.create_line(i*offset + board_padding, 0, i*offset + board_padding, BOARD_LENGTH - board_padding, width=half_border_width*2)
    
    for i in range(1,4):
        xCoord = i*offset+Board_font.measure(str(i))//2
        yCoord = Effective_length + font_size
        game_canvas.create_text(xCoord, yCoord, text=str(i), font=Board_font, fill="#00bb00")
        xCoord = 20
        yCoord = i*offset - font_size - half_border_width * 2
        game_canvas.create_text(xCoord, yCoord, text=ROW_LBL[i-1], font=Board_font, fill="#00bb00")

    for row_idx, row in enumerate(GameBoard.GameBoard):
        centerY = offset*(row_idx+1) - offset//2
        for col_idx, cell in enumerate(row):
            centerX = (offset + half_border_width)*(col_idx+1)       
            if cell != "":
                color = "red" if cell == "X" else "blue"
                game_canvas.create_text(centerX, centerY, text=cell, fill=color, font=Board_font)
            elif not final_board:              
                half_btn_len = offset//2 - 16  
                # Using default args for the button command. Otherwise, it sets the reference instead of the value and
                # all buttons call the funciton for last button click
                button = tk.Button(game_canvas, text=cur_player, command=lambda canvas=canvas,row_idx=row_idx,col_idx=col_idx,cur_player=cur_player: 
                                   set_cell_and_next_turn(canvas, row_idx, col_idx, cur_player))
                button.place(x=centerX-half_btn_len, y=centerY-half_btn_len, width=half_btn_len*2, height=half_btn_len*2)

def set_cell_and_next_turn(canvas:tk.Canvas, row:int, col:int, player:str):
    global GameBoard
    global turn_number
    GameBoard = GameBoard.simulate_set_cell(row, col, player)
    ClearWidget(canvas)
    if GameBoard.IsTerminal():
        end_text = ""
        util = GameBoard.GetUtility()
        if util == 1:
            end_text = "PLAYER X HAS WON THE GAME"
        elif util == -1:
            end_text = "PLAYER O HAS WON THE GAME"
        else:
            end_text = "THE GAME WAS DRAWN"
        lbl_font = font.Font(family="Arial", size=30)
        xPos = (canvas.winfo_width() - lbl_font.measure(end_text))//2
        yPos = BOARD_LENGTH + 150
        lbl = tk.Label(canvas, text=end_text, font=lbl_font, foreground="white", background="#00bb00")
        lbl.place(x=xPos, y=yPos)        
    else:
        turn_number += 1    
        # No need to use minimax for the first 3 turns as there can never be a terminal state here
        if turn_number < 4:
            suggestionText = ""
            if GameBoard.GameBoard[1][1] == "": # Center cell   
                suggestionText = "B2"
            elif GameBoard.GameBoard[0][0] == "": # Top left cell
                suggestionText = "A1"
            elif GameBoard.GameBoard[2][0] == "": # Bottom left cell
                suggestionText = "C1"
            
            suggest_move(canvas, suggestionText)

        elif turn_number < 9:
            root = get_tree(canvas.winfo_width(), row, col, 2)
            draw_minmax_tree(canvas, root, 2)

    game_canvas = get_game_canvas(canvas)
    draw_game_board(canvas, game_canvas, GameBoard.IsTerminal())
    create_title_label(canvas, "Min-Max using Tic-Tac-Toe")


def start_game(frame:ttk.Frame):
    ClearWidget(frame)
    canvas = tk.Canvas(frame, width=frame.winfo_width(), height=frame.winfo_height(), bg="white")
    canvas.pack()
    canvas.update_idletasks()    
    create_title_label(canvas, "Min-Max using Tic-Tac-Toe")
    global GameBoard
    global turn_number
    GameBoard = board()
    game_canvas = get_game_canvas(canvas)
    # Suggest cell B2 as starter
    suggest_move(canvas, "B2")
    draw_game_board(canvas, game_canvas, False)
    
def ClearWidget(widget:tk.Widget):
    if(widget.winfo_class() == "Canvas"):
        widget.delete("all")

    for child in widget.winfo_children():
        child.destroy()