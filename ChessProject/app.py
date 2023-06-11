from flask import Flask, render_template, request, redirect
import psycopg2
import main
import pgntofen
import sql 
import sql_logins
import random
import time

pgnConverter = pgntofen.PgnToFen()
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)
opning = sql.unique
current_opening = start_fen
current_user = -1

# Database connection configuration
#TO BE MODIFIED
YOUR_PASSWORD = 'vxz73ptw'
YOUR_PORT = '5432'

# Establish a connection to server (that you setup yourself). OBS! Check that port, password etc. are correct.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password= YOUR_PASSWORD,
    port= YOUR_PORT
)

@app.route('/')
def home(): 
    return render_template('login.html')

@app.route('/main')
def reroute():
    return render_template('index.html', openings = opning)

# Login til at lave en bruger. (der er brug for flere entities)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password exist in the database
        cur = conn.cursor()
        cur.execute("SELECT * \
                     FROM Users \
                     WHERE username = %s AND password = %s;", 
                     (username, password))
        user = cur.fetchone()

        if user:
            # Successful login
            global current_user
            cur.execute("SELECT id \
                         FROM Users \
                         WHERE username = %s AND password = %s;", 
                                      (username, password))
            current_user = cur.fetchone()[0]
            return redirect('/main')
        else:
            # Invalid credentials
            return "Invalid username or password!"

    # Render the login form
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return "Logged out successfully!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE username = %s;", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            # Username already exists
            return "Username already exists. Please choose a different username."

        # Create a new user
        cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()

        # Redirect to the login page after successful registration
        return redirect('/login')

    # Render the registration form
    return render_template('register.html')

#Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/move', methods=['GET','POST'])
def moving():
    if request.method == 'POST': 
        try:
            newBoard = pgnConverter.resetBoard()
            move = request.form['move']
            next_move = main.currentBoard
            next_move = next_move.__add__([move])
            #print(next_move)
            move_number = len(next_move) 
            all_responses = sql.get_check_for_variations(next_move) #får en liste af mulige variationer fra position
            #print(all_responses,'12321')
            response_long = all_responses[random.randint(0,len(all_responses)-1)] #vælger en variation
            response_long = pgnConverter.pgnToStringList(response_long)
            response_move = response_long[:move_number+1]
            #print(response_move)
            main.currentBoard = response_move
            newBoard = pgnConverter.moves(response_move).getFullFen()
            main.main(newBoard)
        except:
            print('oopsiiies')
    return render_template('index.html', openings = opning)


@app.route('/opening', methods=['GET','POST'])
def pick_opening(): 
    if request.method == 'POST':
        newBoard = pgnConverter.resetBoard()
        opening = request.form['selectOpening']
        pgn_of_opening = sql.get_specific_opening(opening)[0][0]
        string_of_moves = pgnConverter.pgnToStringList(pgn_of_opening)
        main.currentBoard = string_of_moves
        newBoard = pgnConverter.moves(string_of_moves).getFullFen()
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)
    return render_template('index.html', openings = opning)

#lige nu virker dette ikke med åbninger der har apostrof...
@app.route('/favorite', methods=['POST'])
def add_to_favorites():
    if 'opening_id' in request.form:
        opening_name = request.form['opening_id']

        # getting pgn
        cur = conn.cursor()
        cur.execute(f"SELECT pgn \
                      FROM Openings \
                      WHERE opening = '{opening_name}' ",)
        pgn = cur.fetchone()[0]
        
        # Insert the opening into the Fav_Open table (example code)
        # current user global variable from login route.
        cur.execute(f"INSERT INTO Fav_Open (opening_pgn, opening_name, userID) VALUES ('{pgn}','{opening_name}',{current_user})") 
        conn.commit()

        # debug
        cur.execute("SELECT * FROM Fav_Open")
        #print(cur.fetchall())
        cur.close()

        return render_template('index.html', openings = opning)
    else:
        return render_template('index.html', openings = opning)
    

#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    
    app.run()
