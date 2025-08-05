import tkinter as tk
from tkinter import ttk
from math import ceil

class world:
    def __init__(self, nodeX:int, nodeY:int, col_start:int, col_width:int) -> None:
        self.width = 3
        self.height = 2
        self.x = nodeX
        self.y = nodeY
        self.col_start = col_start
        self.col_width = col_width
        # True or False represents wether the tile is "Dirty" or not
        # World form is like so ( C for clean D for dirty )
        #   DDD
        #   CCC
        self.grid = [
            [False, True, True],
            [False, False, False],
        ]
        self.DirtyCount = 2

        # Vaccum is placed in the bottom right corner
        self.VaccumX = 2
        self.VaccumY = 1

        # Set parent and previous action
        self.parent = None
        self.previous_act = ""

    def create_copy(self) -> 'world':
        newWorld = world(self.x, self.y, self.col_start, self.col_width)
        newWorld.width = self.width
        newWorld.height = self.height
        # Creating deep copy for grid
        newWorld.grid = [ row.copy() for row in self.grid ]
        newWorld.VaccumX = self.VaccumX
        newWorld.VaccumY = self.VaccumY
        newWorld.DirtyCount = self.DirtyCount
        return newWorld

    def get_moves(self) -> list['world']:
        moves = []
        if self.VaccumY - 1 >= 0:
            moves.append("up")
        if self.VaccumY + 1 <= self.height - 1:
            moves.append("down")
        if self.VaccumX - 1 >= 0:
            moves.append("left")
        if self.VaccumX + 1 <= self.width - 1:
            moves.append("right")
            
        return moves

    # Simulate moving to a spave and cleaning it. Return the resulting state
    def simulate_move_and_clean(self, dir:str, nodeX:int, nodeY:int, col_start:int, col_width:int) -> 'world':      
        Copy = self.create_copy()
        Copy.parent = self
        Copy.previous_act = dir
        Copy.x = nodeX
        Copy.y = nodeY
        Copy.col_start = col_start
        Copy.col_width = col_width

        if dir == "up":
            Copy.VaccumY -= 1
        elif dir == "down":
            Copy.VaccumY += 1
        elif dir == "left":
            Copy.VaccumX -= 1
        elif dir == "right":
            Copy.VaccumX += 1

        # If True, tile is dirty. Clean it.
        if Copy.grid[Copy.VaccumY][Copy.VaccumX]:
            Copy.grid[Copy.VaccumY][Copy.VaccumX] = False
            Copy.DirtyCount -= 1
        
        return Copy
    
    def draw_world(self, canvas:tk.Canvas, tile_size:int, x:int, y:int):
        # When creating dirty tile, make sure there is 10% padding from all sides to the dirty rect.
        tags = "world"
        tile_padding = ceil(tile_size * 0.1)
        colors = ["#D8B59B", "#B35E32"]
        rowStart = x
        yVal = y
        prev_start_color = 0
        for i in range(self.height):
            # Set starting color as inverse of previous row start color
            col_color = 1 - prev_start_color
            prev_start_color = col_color
            # Go to next row and set xVal to first tile
            xVal = rowStart
            for j in range(self.width):
                x2 = xVal+tile_size
                y2 = yVal+tile_size
                canvas.create_rectangle(xVal, yVal, x2, y2, fill=colors[col_color],tags=tags)
                col_color = 1 - col_color
                # If the current cell value is True, create a gray rect to show that it is dirty
                if self.grid[i][j]:
                    canvas.create_rectangle(xVal+tile_padding, yVal+tile_padding, x2-tile_padding, y2-tile_padding, fill="gray", outline="", tags=tags)
                # If current cell has Vacuum, draw a oval representing it
                if self.VaccumX == j and self.VaccumY == i:
                    canvas.create_oval(xVal+tile_padding*2, yVal+tile_padding*2, x2-tile_padding*2, y2-tile_padding*2, fill="green", tags=tags)
                xVal+=tile_size                        
            yVal += tile_size
    
        