from flask import Flask, render_template, request, redirect
import main
import pgntofen
import sql 
import sql_logins
import random

pgnConverter = pgntofen.PgnToFen()
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)
opning = sql.unique


@app.route('/')
def home(): 
    return render_template('login.html', openings = opning, in_the_move = 'White')


@app.route('/main')
def choose_opening():
    return render_template('landingpage.html', openings = opning)


# Login til at lave en bruger. (der er brug for flere entities)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Establish connection
        cur = sql.conn.cursor()

        # Check if the username and password exist in the database
        cur.execute("SELECT * \
                     FROM Users \
                     WHERE username = %s AND password = %s;", 
                     (username, password))
        user = cur.fetchall()
        cur.close()

        if user:
            cur = sql.conn.cursor()
            cur.execute("SELECT * \
                     FROM Users \
                     WHERE username = %s AND password = %s;", 
                     (username, password))
            # Successful login
            main.current_user = cur.fetchone()[0]
            cur.close()
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
    
        #Establish connection
        cur = sql.conn.cursor()
        # Check if the username already exists in the database
        cur.execute("SELECT * FROM Users WHERE username = %s;", (username,))
        existing_user = cur.fetchone()


        if existing_user:
            # Username already exists
            return "Username already exists. Please choose a different username."

        # Create a new user
        sql_logins.create_users_table()
        cur.execute("INSERT INTO Users (username, password) VALUES (%s, %s);", (username, password))
        sql.conn.commit()
        cur.close()

        # Redirect to the login page after successful registration
        return redirect('/login')

    # Render the registration form
    return render_template('register.html')

# Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/move', methods=['GET','POST'])
def moving():
    if request.method == 'POST': 
        main.currentBoard.append(request.form['move']) # append input move to CB
        i = len(main.currentBoard)
        tempVarList : list = list(filter(lambda x: x[:i] == main.currentBoard, main.variationList)) # Filter variations to include correct move
        if tempVarList:
            if main.currentBoard == max(tempVarList, key=len):
                pgnConverter.resetBoard() # resets the board, before applying move function
                main.main(pgnConverter.moves(main.currentBoard).getFullFen())
                 # Print the pos after user finishes theory.
                print("good job, you finished theory")
                return render_template('victory.html', openings = opning, in_the_move = main.in_the_move, win_message = 'You just played the last theory move, ', win_move = main.currentBoard[i-1])
            else:
                main.currentBoard = random.choice(tempVarList)[:i+1] # pick a random response (NPC move)
                if main.currentBoard == max(tempVarList):
                    print("good job, oppenent finished theory")
                    pgnConverter.resetBoard()
                    main.main(pgnConverter.moves(main.currentBoard).getFullFen())
                    return render_template('victory.html', openings = opning, in_the_move = main.in_the_move, win_message = 'Opponent played the last theory move, ', win_move = main.currentBoard[i])
                pgnConverter.resetBoard() # resets the board, before applying move function
                main.variationList : list = tempVarList
                main.main(pgnConverter.moves(main.currentBoard).getFullFen()) # Print the pos after oppenent moves or theory is finished

        else:
            main.currentBoard : list = main.currentBoard[:i-1]
            pgnConverter.resetBoard()
            main.main(pgnConverter.moves(main.currentBoard).getFullFen()) # Print the pos after wrong input
    return render_template('index.html', openings = opning, in_the_move = main.in_the_move, selected_opening = main.current_opening)        

@app.route('/opening', methods=['GET','POST'])
def pick_opening(): 
    if request.method == 'POST':
        newBoard = pgnConverter.resetBoard()
        opening = request.form["selectOpening"]
        main.current_opening = opening
        main.currentBoard : list = sql.get_specific_opening(opening)
        main.variationList : list = sql.listOfVars(opening)
        newBoard: str = pgnConverter.moves(main.currentBoard).getFullFen()
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)
        if(len(main.currentBoard) % 2 == 0): 
            main.in_the_move = 'White'
        else: 
            main.in_the_move = 'Black'
        return render_template('index.html', openings=opning, selected_opening=opening, in_the_move = main.in_the_move)
    return render_template('index.html', openings = opning, in_the_move = main.in_the_move)

@app.route('/favorite', methods=['POST'])
def add_to_favorites():
    #åbner en cursor og henter pgn til den nuværende åbning
    cur = sql.conn.cursor()
    query = """
    SELECT pgn 
    FROM Openings 
    WHERE opening = %s
    """
    cur.execute(query, [main.current_opening])
    pgn = cur.fetchone()[0]
    
    # getting pgn
    try:
    # Insert the opening into the Fav_Open table  
        query = """
        INSERT INTO Fav_Open (opening_pgn, opening_name, userID) VALUES (%s,%s,%s)
        """
        cur.execute(query, [pgn, main.current_opening, main.current_user]) 
    except: 
        #except i tilfælde af at det er en duplicate
        print("Already in this users favourite openings")
    sql.conn.commit()
    cur.close()


    return render_template('index.html', openings = opning, in_the_move = main.in_the_move, selected_opening = main.current_opening)


#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    
    app.run()