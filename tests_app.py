from unittest import TestCase
from app import app
from flask import session, render_template
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_start_game(self):
        with app.test_client() as client:
            with client.session_transaction() as set_session:
                set_session["high_score"] = 0
                set_session["games_played"] = 0

            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle!</h1>', html)



    def test_display_board(self):
        with app.test_client() as client:

            res = client.get('/boggle')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(session["guessed_words"]), 0)
            self.assertEqual(len(session['boggle_board']), 5)



    def test_check_guess(self):
        with app.test_client() as client:
            app.boggle_game = Boggle()
            board = [['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T']]
            
            with client.session_transaction() as set_session:
                set_session["boggle_board"] = board


            res = client.post('/guess', json={'guess':'test'})
            self.assertEqual(res.status_code, 200)
            self.assertNotIn('guess', app.boggle_game.correctGuesses)
            self.assertEqual(res.get_json(), {"result": "ok"})



    def test_update_game_data(self):
        with app.test_client() as client:
            score = 10
            high_score = 15
            games_played = 2

            with client.session_transaction() as set_session:
                set_session["score"] = score
                set_session["high_score"] = high_score
                set_session["games_played"] = games_played

            data = {"score": 20}

            res = client.post('/update', json=data)
            response_data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(response_data["high_score"], data["score"])
            self.assertEqual(response_data["games_played"], games_played + 1)
            self.assertEqual(session["score"], data["score"])
            self.assertEqual(session["high_score"], data["score"])
            self.assertEqual(session["games_played"], games_played + 1)



    def test_display_game_results(self):
        with app.test_client() as client:

            score = 10
            high_score = 15
            games_played = 2

            with client.session_transaction() as set_session:
                set_session["score"] = score
                set_session["high_score"] = high_score
                set_session["games_played"] = games_played

            res = client.get('/results')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p id="gameScore">Score: 10</p>', html)
            self.assertIn('<p id="highestScore">High Score: 15</p>', html)
            self.assertIn('<p id="gamesPlayed">Games Played: 2</p>', html)
