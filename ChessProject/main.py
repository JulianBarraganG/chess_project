import pygame as py
#import os
from chess.board import board
#from svglib.svglib import svg2rlg # import svg2rlg function from svglib
#from reportlab.graphics import renderPM # import renderPM function from reportlab.graphics
from chess.constants import *
from chess.images import *
from chess.pieces import *

WIN = py.display.set_mode((WIDTH, HEIGHT))

py.display.set_caption("Chess")

test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
test_fen2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"


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