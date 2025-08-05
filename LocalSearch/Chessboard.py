import tkinter as tk
from tkinter import font

class Chessboard:
    def __init__(self, QueenRanks:list[int]) -> None:
        self.QueenRanks = QueenRanks

    def GetCopy(self) -> 'Chessboard':
        return Chessboard(self.QueenRanks.copy())

    def draw_board(self, canvas:tk.Canvas, start_x:int, start_y:int, tile_length:int):        
        colors = ["#D8B59B", "#B35E32"]
        tile_half_length = tile_length // 2
        rank_start_color = 0
        queen_font = font.Font(family="Arial", size=tile_length//2)
        tiles_drawn = 0
        for rank in range(8):
            rank_start_color = 1 - rank_start_color # To switch between starting colors between rows
            color_idx = rank_start_color
            tileY = tile_length*rank + start_y
            for file in range(8):
                tileX = tile_length*file + start_x
                canvas.create_rectangle(tileX, tileY, tileX+tile_length, tileY+tile_length, fill=colors[color_idx], outline="", tags="tile")
                tiles_drawn+=1
                if self.QueenRanks[file] == 8-rank: # If the cell has a Queen on it
                    canvas.create_text(tileX+tile_half_length, tileY+tile_half_length, text="Q", font=queen_font, tags="Queen")                
                
                color_idx = 1 - color_idx

    # Returns a value from 0 to 28. This being the count of queens attacks.
    def get_fitness(self) -> int:
        attacking_pairs = []
        attack_count = 0
        for QueenA_file in range(8):
            for QueenB_file in range(8):
                # Skip if both queens are same
                if QueenA_file == QueenB_file:
                    continue
                # We check wether this attacking pair has already been counted
                if (QueenA_file, QueenB_file) not in attacking_pairs and (QueenB_file, QueenA_file) not in attacking_pairs:
                    QueenA_rank = self.QueenRanks[QueenA_file]
                    QueenB_rank = self.QueenRanks[QueenB_file]
                    IsAttacking = False
                    # No need to check vertical attack as we are not allowing Queens to move horizontally
                    # Check Horizontal attack
                    if QueenA_rank == QueenB_rank:
                        IsAttacking = True

                    # Check for diagonal attacks
                    # If we add or subtract the distance between the two files
                    # If the rank of QueenA is the same as QueenB after adding or subtracting the distance
                    # The Queens are attacking diagonally
                    file_distance = abs(QueenB_file - QueenA_file)
                    if QueenA_rank-file_distance == QueenB_rank or QueenA_rank+file_distance == QueenB_rank:
                        IsAttacking = True

                    if IsAttacking:
                        attack_count += 1
                        attacking_pairs.append((QueenA_file, QueenB_file))
        
        return attack_count
    
    def simulate_queen_move(self, Queen_num:int, moveToRank:int) -> 'Chessboard':
        simulated = self.GetCopy()
        simulated.QueenRanks[Queen_num] = moveToRank
        return simulated