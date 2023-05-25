import pygame as py
import numpy as np
from chess.constants import *
from chess.images import *
from chess.pieces import *
from functions import fen_reader

class board:
    def __init__(self, win, fen):
        self.board = np.zeros((ROWS, COLS))
        self.win = win
        self.fen = fen
        #self._new_board()
        self._from_fen(fen, win)

    # Draw the squares in background
    def _bg(self):
        for i in range(ROWS):
            for j in range(COLS):
                if (j+i) % 2 == 0:
                    py.draw.rect(self.win, DSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                else:
                    py.draw.rect(self.win, LSQ, (j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
    # Starting position
    def _new_board(self):
        self._bg()
        for i in range(ROWS):
            for j in range(COLS):
                self.win.blit(W_PAWN, (i*SQ_SIZE, j*SQ_SIZE))
                
                
    # Draw board from FEN-string
    def _from_fen(self, fen, win):
        self._bg()
        row = 0
        col = 0
        fen_reader(fen, self.win)