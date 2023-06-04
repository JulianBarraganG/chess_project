from flask import Flask, render_template, request
import main

test_fen = "2k2b1r/p1p2ppp/4p3/3Q4/3P4/8/P1Pq1PPP/R1R3K1"
test_fen2 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        move = request.form['move']
        if(move == "d5"):
            main.main(test_fen2)


    return render_template('index.html')

if __name__ == '__main__':
    main.main(test_fen)
    app.run()
