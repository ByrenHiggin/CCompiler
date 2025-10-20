from typing import List
from modules.models.LexerToken import LexerToken


class ParserService():
	def parse_lex(self, lex_array: List[LexerToken]) -> None:
		print("Parsing lex array...")
		for token in lex_array:
			print(f"Token Type: {token.type}, Token Value: {token.value}")