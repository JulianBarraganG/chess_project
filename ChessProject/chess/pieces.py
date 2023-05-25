import pygame as py
from .constants import *
from .images import *

class Piece:
    def __init__(self, win, row, col, color):
        self.x = row
        self.y = col
        self.win = win
        self.color = color
        if self.color == 'w':
            self.fen = 'P'
        elif self.color == 'b':
            self.fen = 'p'
        else:
            raise ValueError("Color parameter must be either 'w' or 'b'")

    def calc_pos(self):
        self.pos = (self.x, self.y)
        print(f"Position is: {self.pos}")

class Pawn(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_PAWN, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_PAWN, (row*SQ_SIZE, col*SQ_SIZE))

class King(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_KING, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_KING, (row*SQ_SIZE, col*SQ_SIZE))

class Queen(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_QUEEN, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_QUEEN, (row*SQ_SIZE, col*SQ_SIZE))

class Rook(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_ROOK, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_ROOK, (row*SQ_SIZE, col*SQ_SIZE))

class Bishop(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_BISHOP, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_BISHOP, (row*SQ_SIZE, col*SQ_SIZE))

class Knight(Piece):
    def __init__(self, win, row, col, color):
        super().__init__(win, row, col, color)
        if self.color == 'w':
            self.win.blit(W_KNIGHT, (row*SQ_SIZE, col*SQ_SIZE))
        elif self.color == 'b':
            self.win.blit(B_KNIGHT, (row*SQ_SIZE, col*SQ_SIZE))