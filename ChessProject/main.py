import pygame as py
from chess.board import board
from chess.constants import *
from chess.images import *
from chess.pieces import *

WIN = py.display.set_mode((WIDTH, HEIGHT))

py.display.set_caption("Chess")

# Test-strings for fen_reader()
test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" #Starting position
test_fen2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR" #Position after 1. e4


def draw_window():
   WIN.fill(WHITE)
   board(WIN, test_fen2)
   py.display.update()


def main():
   clock = py.time.Clock()
   run = True
   while run:

       clock.tick(FPS) #sets tickrate to 60
       for event in py.event.get():
           if event.type == py.QUIT:
               run = False
       
       draw_window()


   py.quit()

if __name__ == "__main__":
   main()