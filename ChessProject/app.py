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


@app.route('/')
def home(): 
    return render_template('login.html')


### OPRET PAGE BETWEEN LOGIN AND PRACTICE


@app.route('/main')
def choose_opening():
    return render_template('index.html', openings = opning, in_the_move = 'White')


# Login til at lave en bruger. (der er brug for flere entities)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password exist in the database
        sql_logins.cur.execute("SELECT * \
                     FROM Users \
                     WHERE username = %s AND password = %s;", 
                     (username, password))
        user = sql_logins.cur.fetchone()

        if user:
            # Successful login
            print(user, 'sdhfisfjdosjfiodsjfdsuihfs')
            return redirect('/main')
        else:
            # Invalid credentials
            return "Invalid username or password!"

    # Render the login form
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        sql_logins.cur.execute("SELECT * FROM Users WHERE username = %s;", (username,))
        existing_user = sql_logins.cur.fetchone()

        if existing_user:
            # Username already exists
            return "Username already exists. Please choose a different username."

        # Create a new user
        sql_logins.cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s);", (username, password))
        sql_logins.conn.commit()

        # Redirect to the login page after successful registration
        return redirect('/login')

    # Render the registration form
    return render_template('register.html')


# Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/move', methods=['GET','POST'])
def moving():
    if request.method == 'POST': 
        try:
            newBoard = pgnConverter.resetBoard() # Creates initial position??
            move = request.form['move']
            next_move = main.currentBoard
            print(next_move)
            next_move = next_move.__add__([move])
            move_number = len(next_move)
            all_responses = sql.get_check_for_variations(next_move)
            response_long = all_responses[random.randint(0, len(all_responses) -1)]
            response_long = pgnConverter.pgnToStringList(response_long)
            response_move = response_long[:move_number + 1]
            main.currentBoard = response_move
            newBoard = pgnConverter.moves(response_move).getFullFen()
            main.main(newBoard)
        except:
            if not main.currentBoard:
                main.main('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR') # If no moves have been made, reprint initial pos
            else: # If user failed from a pos, reprint pos
                retryBoard = main.currentBoard
                main.main(pgnConverter.moves(retryBoard).getFullFen())
        return render_template('index.html', openings = opning, in_the_move = main.in_the_move)
    
    return render_template('index.html', openings = opning, in_the_move = main.in_the_move)
        

@app.route('/opening', methods=['GET','POST'])
def pick_opening(): 
    if request.method == 'POST':
        newBoard = pgnConverter.resetBoard()
        opening = request.form["selectOpening"]
        
        main.currentBoard : list = sql.get_specific_opening(opening)
        main.variationList : list = sql.listOfVars(opening)
        newBoard: str = pgnConverter.moves(main.currentBoard).getFullFen()
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)
        print(len(main.currentBoard))
        print(len(main.currentBoard)%2)
        if(len(main.currentBoard)%2 == 0): 
            main.in_the_move = 'White'
        else: 
            main.in_the_move = 'Black'
        return render_template('index.html', openings=opning, selected_opening=opening, in_the_move = main.in_the_move)
    return render_template('index.html', openings = opning, in_the_move = main.in_the_move)


#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    
    app.run()
