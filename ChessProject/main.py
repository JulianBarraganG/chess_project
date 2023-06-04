import pygame as py
import os
from chess.board import board
#from svglib.svglib import svg2rlg # import svg2rlg function from svglib
#from reportlab.graphics import renderPM # import renderPM function from reportlab.graphics
from chess.constants import *
from chess.images import *
from chess.pieces import *

WIN = py.display.set_mode((WIDTH, HEIGHT))

py.display.set_caption("Chess")

test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
test_fen2 = "2k2b1r/p1p2ppp/4p3/3Q4/3P4/8/P1Pq1PPP/R1R3K1"


def draw_window():
   WIN.fill(WHITE)
   board(WIN, test_fen2)
   py.display.update()


def main():
   """clock = py.time.Clock()
   run = True
   while run:
       clock.tick(FPS) #sets tickrate to 60
       for event in py.event.get():
           if event.type == py.QUIT:
               run = False"""
       
   draw_window()
   screenshot()
   pygame.quit()


   #py.quit()

def screenshot(): 
   screenshot = pygame.surfarray.array3d(pygame.display.get_surface())
   image = pygame.surfarray.make_surface(screenshot)
   script_dir = os.path.dirname(os.path.abspath(__file__))
   folder_path = os.path.join(script_dir, 'static')
   os.makedirs(folder_path, exist_ok=True)

   filename = os.path.join(folder_path, 'current_position.png')
   pygame.image.save(image, filename)


if __name__ == "__main__":
   main()
   