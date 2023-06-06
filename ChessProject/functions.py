from chess.pieces import *
   
def fen_reader(fen, win):
    row = 0
    col = 0
    for char in fen:
        if char.isdigit():
            row += int(char)
        elif char == 'P':
            Pawn(win, row, col, 'w')
            row += 1
        elif char == 'p':
            Pawn(win, row, col, 'b')
            row += 1
        elif char == 'K':
            King(win, row, col, 'w')
            row += 1
        elif char == 'k':
            King(win, row, col, 'b')
            row += 1
        elif char == 'Q':
            Queen(win, row, col, 'w')
            row += 1
        elif char == 'q':
            Queen(win, row, col, 'b')
            row += 1
        elif char == 'R':
            Rook(win, row, col, 'w')
            row += 1
        elif char == 'r':
            Rook(win, row, col, 'b')
            row += 1
        elif char == 'B':
            Bishop(win, row, col, 'w')
            row += 1
        elif char == 'b':
            Bishop(win, row, col, 'b')
            row += 1
        elif char == 'N':
            Knight(win, row, col, 'w')
            row += 1
        elif char == 'n':
            Knight(win, row, col, 'b')
            row += 1
        elif char == '/':
            col += 1
            row = 0
        elif char.isspace(): 
            break
