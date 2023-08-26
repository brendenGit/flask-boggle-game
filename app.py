from boggle import Boggle
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "debug123"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


boggle_game = Boggle()


@app.route('/')
def start_game():
    """
    Renders the 'start_game.html' template and displays the user's high score and the number of games played.

    Returns:
    The rendered template with the high score and games played.
    """
    return render_template('start_game.html', high_score=session["high_score"], games_played=session["games_played"])


@app.route('/boggle')
def display_board():
    """
    Generates a new Boggle board, stores it in the session, and renders the 'board.html' template.

    Returns:
    The rendered template displaying the Boggle board.
    """
    boggle_board = boggle_game.make_board()
    session['boggle_board'] = boggle_board
    session['guessed_words'] = []
    return render_template('board.html', board=session['boggle_board'])


@app.route('/guess', methods=['POST'])
def check_guess():
    """
    Handles a guessed word submitted via POST request, checks if the word is valid in the Boggle game,
    and responds with the result.

    Returns:
    A JSON response containing the result of the word guess.
    """
    guess_data = request.json
    guess = guess_data["guess"]
    if guess in boggle_game.words and guess not in boggle_game.correctGuesses:
        boggle_game.correctGuesses.add(guess)
        valid_word = boggle_game.check_valid_word(
            session['boggle_board'], guess)
        response_data = {"result": valid_word}
    elif guess in boggle_game.correctGuesses:
        response_data = {"result": "already-guessed"}
    else:
        response_data = {"result": "not-a-word"}
    return response_data


@app.route('/update', methods=['POST'])
def update_game_data():
    """
    Updates the game data including the score, high score, and number of games played in the session.

    Returns:
    A JSON response containing the updated high score and games played.
    """
    game_data = request.json

    boggle_game.correctGuesses.clear()

    session["score"] = game_data["score"]

    if "high_score" not in session:
        session["high_score"] = session["score"]
    elif session["score"] > session["high_score"]:
        session["high_score"] = session["score"]

    if "games_played" not in session:
        session["games_played"] = 1
    else:
        session["games_played"] += 1
    return {"high_score": session["high_score"], "games_played": session["games_played"]}


@app.route('/results')
def display_game_results():
    """
    Generates a new Boggle board, stores it in the session, and renders the 'board.html' template.

    Returns:
    The rendered template displaying the Boggle board.
    """
    return render_template('results.html', score=session["score"], high_score=session["high_score"], games_played= session["games_played"])
