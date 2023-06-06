from flask import Flask, render_template, request
import main
import pgntofen

pgnConverter = pgntofen.PgnToFen()
start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)

#Herinde kigger vi på hvad der sker i inputfeltet
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #request.form['move'] er det som er skrevet i inputfeltet
        move = request.form['move']

        #lige nu laver den en fast position uanset input
        #der mangler altså at den husker hvilken position vi står i (den seneste der blev sendt til brættet)
        #den skal så lave an query baseret på den position og inputtet, og returnere en pgn fra databasen hvis det er et korrekt træk
        #eller skrive på skærmen at det var forkert, hvis det var et forkert træk
        #Lige nu crasher alt også hvis man spiller et træk den ikke kan forstå. Forhåbentligt bliver det også fikset når de eneste pgn-træk der bliver
        #sendt til pgnConverter.moves er dem som ligger inde i databasen, fordi den kun skal sende dem afsted, som matcher noget i databasen. 

        #her konverterer vi listen af pgn notation (fås fra databasen) til fen-notation
        newBoard = pgnConverter.moves('1. d4 Nf6 2. c4 e6 3. g3 d5 4. Bg2 dxc4').getFullFen()
    
        print(newBoard)
        #her kalder vi den funktion som i sidste ende gør, at brættet bliver vist på skærmen
        main.main(newBoard)


    return render_template('index.html')

#det her er bare det allerførste der sker når man kører appen
if __name__ == '__main__':
    #brættet bliver sat til at vise startpositionen i udgangspunktet
    main.main(start_fen)
    app.run()
