from typing import List
from modules.models.LexerToken import LexerToken
from modules.models.enums.token_type import TokenPatterns

class TokenIteratorService():
	position: int = 0
	lex_array: List[LexerToken] = []
	
	def iterate_tokens_until_type_or_error(self, token: TokenPatterns, target_type: TokenPatterns) -> bool:
		if token == TokenPatterns.EOF or self.position > len(self.lex_array):
			return False
		return token != target_type

	def consume_token(self) -> LexerToken:
		if self.position < len(self.lex_array):
			current_token = self.lex_array[self.position]
			self.position += 1
			return current_token
		return LexerToken(type=TokenPatterns.EOF, value="")

	def peek_ahead(self, offset: int = 0) -> LexerToken:
		if self.position + offset < len(self.lex_array):
			return self.lex_array[self.position + offset]
		return LexerToken(type=TokenPatterns.ERROR, value="")