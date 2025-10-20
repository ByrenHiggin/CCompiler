#type: ignore
import unittest
from unittest.mock import mock_open, patch
import sys
import os

# Add the project root to the path to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.lexer.LexerService import LexerService
from modules.models.LexerToken import LexerToken
from modules.models.enums.token_type import TokenPatterns
from modules.models.enums.keyword_patterns import KeyWordPatterns


class TestLexerService(unittest.TestCase):
    def setUp(self):
        self.lexer = LexerService()
    
    def test_test_token_identifier(self):
        # Test identifier recognition using the exposed method
        # In Python, double underscore methods are name-mangled with the class name
        token = self.lexer._LexerService__test_token("variable123") 
        self.assertEqual(token.type, TokenPatterns.IDENTIFIER)
        self.assertEqual(token.value, "variable123")
    
    def test_test_token_number(self):
        # Test number recognition
        token = self.lexer._LexerService__test_token("42")
        self.assertEqual(token.type, TokenPatterns.CONSTANT)
        self.assertEqual(token.value, "42")
        
        # token = self.lexer._LexerService__test_token("3.14")
        # self.assertEqual(token.type, TokenPatterns.CONSTANT)
        # self.assertEqual(token.value, "3.14")
    
    def test_test_token_operators(self):
        # Test operator recognition
        operators = ["+", "-", "*", "/", "=", "==", "!=", "<", "<=", ">", ">=", "&&", "||"]
        for op in operators:
            token = self.lexer._LexerService__test_token(op)
            self.assertEqual(token.value, op)
    
    def test_test_token_punctuation(self):
        # Test punctuation recognition
        punctuation = ["(", ")", "{", "}", "[", "]", ";", ","]
        for p in punctuation:
            token = self.lexer._LexerService__test_token(p)
            self.assertEqual(token.value, p)
    
    def test_test_token_comments(self):
        # Test single line comment
        token = self.lexer._LexerService__test_token("//This is a comment")
        self.assertEqual(token.type, TokenPatterns.COMMENT_LINE)
        self.assertEqual(token.value, "//This is a comment")
        
        # Test multi-line comment start
        token = self.lexer._LexerService__test_token("/* Comment start")
        self.assertEqual(token.type, TokenPatterns.COMMENT_MULTI_START)
        self.assertEqual(token.value, "/*")
        
        # Test comment mode handling
        self.lexer.comment_skip_mode = True
        token = self.lexer._LexerService__test_token("Comment content", True)
        self.assertEqual(token.type, TokenPatterns.COMMENT_LINE)
        self.assertEqual(token.value, "Comment content")
        
        # Test multi-line comment end
        token = self.lexer._LexerService__test_token("Comment end */", True)
        self.assertEqual(token.type, TokenPatterns.COMMENT_MULTI_END)
        self.assertEqual(token.value, "Comment end */")
        self.lexer.comment_skip_mode = False
    
    # def test_test_token_string_literal(self):
    #     # Test string literal recognition
    #     token = self.lexer._LexerService__test_token("\"Hello, world!\"")
    #     self.assertEqual(token.type, TokenPatterns.CONSTANT)
    #     self.assertEqual(token.value, "\"Hello, world!\"")
    
    def test_test_token_error(self):
        # Test error handling for unrecognized tokens
        token = self.lexer._LexerService__test_token("@")  # Assuming @ is not a valid token
        self.assertEqual(token.type, TokenPatterns.ERROR)
        self.assertEqual(token.value, "@")
    
    def test_test_for_keyword(self):
        # Test keyword recognition
        for keyword in KeyWordPatterns:
            identifier = keyword.name.lower()  # Assuming keywords are stored in uppercase
            token = self.lexer._LexerService__test_for_keyword(identifier)
            self.assertEqual(token.type, TokenPatterns.KEYWORD)
            self.assertEqual(token.value, keyword.name)
        
        # Test non-keyword identifier
        token = self.lexer._LexerService__test_for_keyword("userVariable")
        self.assertEqual(token.type, TokenPatterns.IDENTIFIER)
        self.assertEqual(token.value, "userVariable")
    
    def test_tokenize_string(self):
        # Test tokenizing a simple string
        input_str = "int main() { return 0; }"
        tokens = self.lexer._LexerService__tokenize_string(input_str)
        
        # Verify the number of tokens and specific tokens
        self.assertTrue(len(tokens) > 0)
        self.assertEqual(tokens[0].type, TokenPatterns.KEYWORD)  # "int" is identified first
        
        # Test comment handling
        input_with_comment = "int x; // variable declaration"
        tokens = self.lexer._LexerService__tokenize_string(input_with_comment)
        # Verify comments are skipped
        for token in tokens:
            self.assertNotEqual(token.type, TokenPatterns.COMMENT_LINE)
        
        # Test multi-line comment
        input_with_multiline = "int x; /* multi-line\ncomment */ int y;"
        tokens = self.lexer._LexerService__tokenize_string(input_with_multiline)
        # After parsing, comment_skip_mode should be False
        self.assertFalse(self.lexer.comment_skip_mode)
    
    @patch("builtins.open", new_callable=mock_open, read_data="int main() {\n    return 0;\n}\n")
    def test_lex_file(self, mock_file):
        # Test lexing from file
        tokens = self.lexer.lex_file("dummy_file.c")
        
        # Verify the file was read and tokens were generated
        mock_file.assert_called_once_with("dummy_file.c", "r")
        self.assertTrue(len(tokens) > 0)
        
        # Check if tokens match expected pattern
        expected_values = ["int", "main", "(", ")", "{", "return", "0", ";", "}"]
        for i, expected in enumerate(expected_values):
            if i < len(tokens):
                self.assertTrue(tokens[i].value == expected or tokens[i].value.lower() == expected)

if __name__ == "__main__":
    unittest.main()