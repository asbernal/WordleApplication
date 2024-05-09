import unittest
import random
from parameterized import parameterized
from src.agilec_randomWord_service import get_randomWords, parse, pick_randomWord
  
class AgileCRandomWordTests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_get_randomWords(self):
        self.assertEqual('FAVOR\nSMART\nGUIDE\nTESTS\nGRADE\nBRAIN\nSPAIN\nSPINE\nGRAIN\nBOARD\n', get_randomWords())

    def test_parse_response(self):
        self.assertEqual(['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD'], parse('FAVOR\nSMART\nGUIDE\nTESTS\nGRADE\nBRAIN\nSPAIN\nSPINE\nGRAIN\nBOARD\n'))

    def test_parse_response_throwException(self):
        self.assertRaisesRegex(ValueError, "Not correct words of list", parse, "error error error")

    def test_pick_randomWord(self):
        self.assertEqual(True, True if pick_randomWord() in ['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD'] else False)

    def test_pick_randomWord_givenSeed13(self):
        random.seed(13)
        self.assertEqual(pick_randomWord(), pick_randomWord())

if __name__ == '__main__':
    unittest.main()
    