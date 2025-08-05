class board:
    def __init__(self) -> None:
        self.GameBoard = [
            ['','',''],
            ['','',''],
            ['','','']
        ]

    def GetCopy(self) -> 'board':
        Copy = board()
        Copy.GameBoard = [ row.copy() for row in self.GameBoard ]
        return Copy

    def GetPossibleMoves(self) -> list[tuple[int, int]]:
        moves = []
        for row in range(3):
            for col in range(3):
                if self.GameBoard[row][col] == '':
                    moves.append((row, col))

        return moves

    def simulate_set_cell(self, row:int, col:int, player:str) -> 'board':
        simulated = self.GetCopy()
        simulated.GameBoard[row][col] = player
        return simulated

    # Check the current status of the board
    # returns:  +100 for X win, -100 for O win, 0 for draw.
    #           +1 for potential of X winning, -1 for potential of O winning
    # We are checking for setups as the algorithm may not run till terminal state.
    def GetUtility(self) -> int:        
        dias = ["", ""]
        cols = ["", "", ""]
        # Traverse the Board and save relevant info along with checking row clear
        for row_idx, row in enumerate(self.GameBoard):
            # Check for row finish
            if row.count("X") == 3:
                return 1
            elif row.count("O") == 3:
                return -1
            # Prepare for column and diagonal finish check
            for col_idx, cell in enumerate(row):
                # Check if cell is not empty
                if cell != "":
                    # Diagonal top-left to bottom-right
                    if col_idx == row_idx:
                        dias[0] += cell
                    # Diagonal top-right to bottom-left
                    if 2 - col_idx == row_idx:
                        dias[1] += cell
                    cols[col_idx] += cell
        
        # Check column and diagonal clear
        if "XXX" in cols or "XXX" in dias:
            return 1
        elif "OOO" in cols or "OOO" in dias:
            return -1      
        
        return 0        
            
    def IsTerminal(self) -> bool:
        # A player won
        if abs(self.GetUtility()) == 1:
            return True
        # Check for draw
        empty_cells = 9
        for row in self.GameBoard:
            for cell in row:
                if cell != "":
                    empty_cells -= 1
        return empty_cells == 0
        
class node:
    def __init__(self, row:int, col:int, max_width:int, col_start:int, x:int, y:int) -> None:
        self.row = row
        self.col = col
        self.max_width = max_width
        self.col_start = col_start
        self.x = x
        self.y = y
        self.children: list['node'] = []
    
    def addChild(self, child:'node') -> None:
        self.children.append(child)
