import pygame as py
from chess.board import board
from chess.constants import *
from chess.images import *
from chess.pieces import *

WIN = py.display.set_mode((WIDTH, HEIGHT))

py.display.set_caption("Chess")

#gemmer den seneste liste af træk her. Hvis man gør det inde i app.py bliver den hele tiden reset
i = 0
if i == 0:
   currentBoard = []
   i = i + 1


#Den her funktion tegner vinduet
def draw_window(fen):
   WIN = py.display.set_mode((WIDTH, HEIGHT))
   WIN.fill(WHITE)
   board(WIN, fen)
   py.display.update()


def main(fen):
   #først bliver vinduet tegnet med den givne fen-string
   draw_window(fen)
   #så tager vi et screenshot af positionen og gemmer det
   screenshot()
   #så lukker vi spillet igen
   pygame.quit()


   #py.quit()
#den her funktion er ansvarlig for at tage et screenshot af positionen og gemme det i static mappen med navnet current_position.pgn
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
   