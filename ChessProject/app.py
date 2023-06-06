from flask import Flask, render_template, request
import main
import pgntofen
import sql 

pgnConverter = pgntofen.PgnToFen()
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)
opning = sql.unique


@app.route('/')
def home(): 
    return render_template('index.html', openings = opning)

#Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/move', methods=['GET','POST'])
def moving():
    print(main.currentBoard)
    if request.method == 'POST': 
        move = request.form['move']
        next_move = main.currentBoard
        next_move = next_move.__add__([move])
        print(next_move)
    return render_template('index.html', openings = opning)
        

@app.route('/opening', methods=['GET','POST'])
def pick_opening(): 
    if request.method == 'POST':
        newBoard = pgnConverter.resetBoard()
        #request.form['move'] er det som er skrevet i inputfeltet
        opening = request.form['selectOpening']
        pgn_of_opening = sql.get_specific_opening(opening)[0][0]
        string_of_moves = pgnConverter.pgnToStringList(pgn_of_opening)
        main.currentBoard = string_of_moves
        newBoard = pgnConverter.moves(string_of_moves).getFullFen()
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)
    return render_template('index.html', openings = opning)


#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    
    app.run()
