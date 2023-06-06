from flask import Flask, render_template, request
import main
import pgntofen
import sql 

pgnConverter = pgntofen.PgnToFen()
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)
opning = sql.unique

#Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':


        newBoard = pgnConverter.resetBoard()
        #request.form['move'] er det som er skrevet i inputfeltet
        move = request.form['move']
        opening = request.form['selectOpening']


        print(opening)
        pgn_of_opening = sql.get_specific_opening(opening)[0][0]

        #lige nu laver den en fast position uanset input
        #der mangler altså at den husker hvilken position vi står i (den seneste der blev sendt til brættet)
        #den skal så lave an query baseret på den position og inputtet, og returnere en pgn fra databasen hvis det er et korrekt træk
        #eller skrive på skærmen at det var forkert, hvis det var et forkert træk
        #Lige nu crasher alt også hvis man spiller et træk den ikke kan forstå. Forhåbentligt bliver det også fikset når de eneste pgn-træk der bliver
        #sendt til pgnConverter.moves er dem som ligger inde i databasen, fordi den kun skal sende dem afsted, som matcher noget i databasen. 

        #her konverterer vi listen af pgn notation (fås fra databasen) til fen-notation
        newBoard = pgnConverter.moves(pgn_of_opening).getFullFen()
    
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)
        
        
    return render_template('index.html', openings = opning)


#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    
    app.run()
