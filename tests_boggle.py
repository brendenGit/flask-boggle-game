from unittest import TestCase
from boggle import Boggle

class BoggleTests(TestCase):

    def setUp(self):
        self.boggle = Boggle()



    def test_read_dict(self):
        words = self.boggle.read_dict("words.txt")
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
        for word in words:
            self.assertTrue(isinstance(word, str))



    def test_make_board(self):
        board = self.boggle.make_board()
        self.assertIsInstance(board, list)
        self.assertEqual(len(board), 5)
        for row in board:
            self.assertEqual(len(row), 5)
            for letter in row:
                self.assertTrue(letter.isalpha())



    def test_check_valid_word(self):
        board = [['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T']]
        
        valid_word = "test"
        invalid_word = "guess"
        not_a_word = "hjkl"

        result_valid_word = self.boggle.check_valid_word(board, valid_word)
        result_invalid_word = self.boggle.check_valid_word(board, invalid_word)
        result_not_a_word = self.boggle.check_valid_word(board, not_a_word)

        self.assertEqual(result_valid_word, "ok")
        self.assertEqual(result_invalid_word, "not-on-board")
        self.assertEqual(result_not_a_word, "not-word")



    def test_find(self):
        board = [['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T'],
                 ['T', 'E', 'S', 'T', 'T']]

        valid_word = "TEST"
        invalid_word = "XYZ"

        result_valid_word = self.boggle.find(board, valid_word)
        result_invalid_word = self.boggle.find(board, invalid_word)

        self.assertTrue(result_valid_word)
        self.assertFalse(result_invalid_word)