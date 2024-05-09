import unittest
from parameterized import parameterized
from src.agilec_spellcheck_service import get_response, parse, spellcheck
  
class AgileCSpellCheckServiceTests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)

    def test_getResponse_inputFavor(self):
        self.assertEqual('true', get_response("FAVOR")) 

    def test_getResponse_inputFavor(self):
        self.assertEqual('false', get_response("FAVRO"))

    def test_parse_given_true(self):
        self.assertEqual(True, parse("true")) 

    def test_parse_given_false(self):
        self.assertEqual(False, parse("false")) 

    def test_parse_throwsException(self):
        self.assertRaisesRegex(ValueError, "Not true or false", parse, "error error error")

    def test_spellcheck(self):
        self.assertEqual(True, spellcheck("FAVOR"))
    
    def test_spellcheck(self):
        self.assertEqual(False, spellcheck("FAVRE"))

if __name__ == '__main__':
    unittest.main()
    