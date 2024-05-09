import unittest
from parameterized import parameterized
from src.wordle import tally, play, PlayerResponse, Matches, Status

globals().update(Matches.__members__)
globals().update(PlayerResponse.__members__)
globals().update(Status.__members__)

class WordleTests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)
        

    @parameterized.expand([
        ("FAVOR", "FAVOR", [EXACT_MATCH] * 5),
        ("FAVOR", "RAPID", [PARTIAL_MATCH, EXACT_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),
        ("FAVOR", "MAYOR", [NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH, EXACT_MATCH]),
        ("FAVOR", "RIVER", [NO_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH]),
        ("FAVOR", "AMAST", [PARTIAL_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH]),

        ("SKILL", "SKILL", [EXACT_MATCH] * 5),
        ("SKILL", "SWIRL", [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH]),
        ("SKILL", "CIVIL", [NO_MATCH, PARTIAL_MATCH, NO_MATCH, NO_MATCH, EXACT_MATCH]),
        ("SKILL", "SHIMS", [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, NO_MATCH]),
        ("SKILL", "SILLY", [EXACT_MATCH, PARTIAL_MATCH, PARTIAL_MATCH, EXACT_MATCH, NO_MATCH]),
        ("SKILL", "SLICE", [EXACT_MATCH, PARTIAL_MATCH, EXACT_MATCH, NO_MATCH, NO_MATCH]),
    ])

    def test_tally_Lazy(self, target, guess, expected):
        self.assertEqual(tally(target, guess), expected)

    
    @parameterized.expand([
        ("FAVOR", "FOR", "Word must be 5 letters"),
        ("FAVOR", "FERVER", "Word must be 5 letters"),
    ])
    def test_exception_length(self, target, guess, expected_exception):
        with self.assertRaisesRegex(ValueError, expected_exception):
            tally(target, guess)
    
    @parameterized.expand([
        ("FAVOR", "FAVOR", 0, {Attempts: 1, TallyResponse: [EXACT_MATCH] * 5, GameStatus: WIN, Message: "Amazing"}),
        ("FAVOR", "FEVER", 1, {Attempts: 2, TallyResponse: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH], GameStatus: IN_PROGRESS, Message: ""}),
        ("FAVOR", "TESTS", 5, {Attempts: 6, TallyResponse: [NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH, NO_MATCH], GameStatus: LOSE, Message: f"It was FAVOR, better luck next time"})
   ])
    def test_play(self, target, guess, attempt, expected):
        self.assertEqual(play(target, guess, attempt), expected)


    def test_play_with_target_FAVOR_guess_FEVER_considered_wrong_spelling(self):
        self.assertRaisesRegex(Exception, "Not a word", play, "FAVOR", "FEVER", 1, lambda word: False)

    def test_play_with_target_FAVOR_guess_FEVER_considered_correct_results(self):
        self.assertTrue(play("FAVOR", "FEVER", 1, lambda word: True), {Attempts: 2, TallyResponse: [EXACT_MATCH, NO_MATCH, EXACT_MATCH, NO_MATCH, EXACT_MATCH], GameStatus: IN_PROGRESS, Message: ""}) 

    
    def test_play_with_target_FAVOR_guess_FEVER_considered_checking_spelling_results(self):
        def spellcheck_stub(word):
                raise Exception("Network Error")
        
        self.assertRaisesRegex(Exception, "Network Error", play, "FAVOR", "FEVER", 1, lambda word: spellcheck_stub(word))

if __name__ == '__main__':
    unittest.main()
