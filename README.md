### Chess Project ###

# About
A project by a study group, in the KU course DIS. The project interacts with Lichess' opening database, accesing 3401 opening variations to practice in the app.
The app allows you to pick an opening you wish to train, and lets you train your opening theory, by matching your moves to the different variations of the opening, and then replies with a theory move, randomly picked from the different variations supporting said move.
  If you manage to complete an entire variation of theory, the app will congratulate you and tell you you've succesfully completed theory.
  If you make an invalid or illegal move, no moves will be projected on the board, and you're supposed to try again.
  You can register and save your favorite openings for later training.
  
  It is possible, on the 'Profile' page, to change your password and to delete openings from your list of personal favourites. 
  
# Chess notation
The app is also a great way to test your chess notation, since moves can only be played by manually entering the move in conventional pgn notation.
This is the serious way to train opening theory, since associating the moves with the PGN notation, reinforces the memorisation of the opening.

If you are unfamiliar with chess notation google PGN. Note that you are only supposed to enter the move, not the turn (i.e. black on turn 3 plays Nf6 would be 3...Nf6 in PGN, you are only to write the move Nf6 itself. Note that the move function is case sensitive.

# Tester PGN
To verify that the app works, you can try picking the Mieses opening out of the 142 unique openings in the list. This opening incidentally is a 2 move opening with no variations, so it is an easy tester. Simply reply by inputting e5 in the move box. You should be congratulated with ending the theory. In the case where the NPC plays the final move, it will tell you that you finished theory and provide the last move as well, so you can memorise this.

# Borrowed git repository
All the code in this repository is original, except for the pgntofen.py file, which comes from the: https://github.com/SindreSvendby/pgnToFen git repository. Pythons chess modules allows for similar conversions, but running time is greatly improved in SindreSvendby's implementation, and it is easier to use independently of the chess module, which came in handy since we coded the chess board/piece projections ourselves via the fen_to_board algorithm (in functions.py).

# Libraries
numpy
pandas
psycopg2
flask
pygame
os

# Setting up the server
Make sure to create a postgres database server, using you preffered method or client. We use pgAdmin4 ourselves. To connect to the server, go to the sql.py file, and modify password, name, port etc. The code is commented to help identify what needs to be changed, and the modifications should be made at the top.

# Running the app
Once you've set up your server, you can verify (i.e. with client) that the opening database is created in your schemas, after running either sql_logins.py or app.py.
  To run app.py navigate toe the ChessProject folder in your terminal, and write python app.py (you might want to create a venv and download any missing modules. i.e. pip install pygame) and then follow the local link to open the webapp in your favorite browser.
 
