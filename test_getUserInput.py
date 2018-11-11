import unittest
from unittest.mock import patch

import getUserInput as ui

class TestInputMethods(unittest.TestCase):

    def test_GetUserInput(self):
        pass
    
    def test_GetYesNo_correct_input(self):
        """This tests correct inputs to the GetYesNo function"""
        with patch("builtins.input", return_value="y"):
            self.assertTrue(ui.GetYesNo("Checking y")=="y")
        
        with patch("builtins.input", return_value="n"):
            self.assertTrue(ui.GetYesNo("Checking n")=="n")
    
    def test_GetYesNo_wrong_input(self):
        
        pass
        #TEST_PROMPT = "Test Prompt"

        #with patch("builtins.input", return_value="x"):
        #    self.assertFalse(ui.GetYesNo(TEST_PROMPT)=="y")

    def test_GetTrueFalse(self):
        pass
            
    def test_GetInteger(self):
        pass
    
if __name__ == "__main__":
    unittest.main()

    #run with -v for verbose