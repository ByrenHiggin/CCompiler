from typing import List
from modules.models.lexer.LexerToken import Token
from modules.models.enums.token_type import TokenType

class TokenIteratorService():
	position: int = 0
	lex_array: List[Token] = []

	def at_end(self) -> bool:
		return self.position >= len(self.lex_array)
 
	def iterate_tokens_until_type_or_error(self, token: TokenType, target_type: TokenType) -> bool:
		if self.at_end():
			return False
		return token != target_type

	def consume_token(self) -> Token:
		if self.position < len(self.lex_array):
			current_token = self.lex_array[self.position]
			self.position += 1
			return current_token
		return Token(type=TokenType.EOF, lineNumber=-1, value="")

	def current_token(self) -> Token:
		if self.position < len(self.lex_array):
			return self.lex_array[self.position]
		return Token(type=TokenType.EOF, lineNumber=-1, value="")

	def peek_ahead(self, index: int = 0) -> Token:
		if index < len(self.lex_array):
			return self.lex_array[index]
		return Token(type=TokenType.ERROR, lineNumber=-1, value="")

	def peek_behind(self, index: int = 0) -> Token | None:
		if index >= 0:
			return self.lex_array[index]
		return None