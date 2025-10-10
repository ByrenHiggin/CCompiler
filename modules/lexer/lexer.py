from enum import Enum, auto
from pydantic import BaseModel
import re

class TokenType(Enum):

	INT_KEYWORD = r'int\b'
	FLOAT_KEYWORD = r'float\b'
	CHAR_KEYWORD = r'char\b'
	RETURN_KEYWORD = r'return\b'
	IF_KEYWORD = r'if\b'
	ELSE_KEYWORD = r'else\b'
	WHILE_KEYWORD = r'while\b'
	FOR_KEYWORD = r'for\b'
	IDENTIFIER = r'[a-zA-Z_]\w*\b'
	CONSTANT = r'[0-9]+\b'
	PLUS = r'\+'
	MINUS = r'-'
	MULTIPLY = r'\*'
	DIVIDE = r'\/'
	ASSIGN = r'='
	EQ = r'=='
	NEQ = r'!='
	LT = r'<'
	GT = r'>'
	LTE = r'<='
	GTE = r'>='
	SEMICOLON = r';'
	LPAREN = r'\('
	RPAREN = r'\)'
	LBRACE = r'\{'
	RBRACE = r'\}'
	COMMA = r','
	EOF = ''
	
class LexerInstance():
	
	tokens = []

	def __tokenize_string(self, data):
		input = data
		while input:
			input = input.lstrip()
			if input == "":
				break
			token_type = None
			token_value = None
			for tokenType in TokenType:
				regex = tokenType.value
				match = re.match(regex, input, flags=0)
				if match:
					token_type = tokenType
					token_value = match.group(0)
					break
			if token_type is None:
				raise ValueError(f"Unexpected character: {input[0]}")
			self.tokens.append((token_type, token_value))
			input = input[len(token_value):]

		for token in self.tokens:
			print(token)

	def lex_file(self,file_name):
		with open(file_name, 'r') as file:
			data = file.read()
			# Simple lexer logic (for demonstration purposes)
			self.__tokenize_string(data)
		self.tokens.append((TokenType.EOF, None))
		return self.tokens
