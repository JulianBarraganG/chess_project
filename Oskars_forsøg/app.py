from flask import Flask, render_template, request
import chess.pgn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def display_board():
    pgn = request.form['pgn']
    game = chess.pgn.read_game(io.StringIO(pgn))
    board = game.board()
    moves = []

    for move in game.mainline_moves():
        moves.append(move.uci())
        board.push(move)

    return render_template('index.html', moves=moves, board=board)

if __name__ == '__main__':
    app.run()