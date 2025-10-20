from typing import List
import re
from modules.models.LexerToken import LexerToken
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenPatterns


class LexerService():
	comment_skip_mode = False

	def __test_token(self, input: str, comment_skip_mode: bool = False) -> LexerToken:
		token_type = None
		token_value = None
		if comment_skip_mode:
			for tokenPattern in [TokenPatterns.COMMENT_MULTI_END]:
				regex = tokenPattern.value
				match = re.match(regex, input)
				if match:
					token_type = tokenPattern
					token_value = match.group(0)
					return LexerToken(type=token_type, value=token_value)
			return LexerToken(type=TokenPatterns.COMMENT_LINE, value=input)
		for tokenPattern in [pattern for pattern in TokenPatterns if pattern != TokenPatterns.ERROR]:
			regex = tokenPattern.value
			match = re.match(regex, input, flags=re.DOTALL | re.MULTILINE)
			if match:
				token_type = tokenPattern
				token_value = match.group(0)
				return LexerToken(type=token_type, value=token_value)
		return LexerToken(type=TokenPatterns.ERROR, value=input[0])
	
	def __test_for_keyword(self, identifier: str)->LexerToken:
		for keyword in KeyWordPatterns:
			regex = keyword.value
			match = re.match(regex, identifier)
			if match:
				return LexerToken(type=TokenPatterns.KEYWORD, value=keyword.name)
		return LexerToken(type=TokenPatterns.IDENTIFIER, value=identifier)

	def __tokenize_string(self, data: str) -> List[LexerToken]:
		input = data
		tokens: List[LexerToken] = []

		while input:
			input = input.lstrip()
			if input == "":
				break
			lexerToken: LexerToken = self.__test_token(input, self.comment_skip_mode)
			match lexerToken.type: # type: ignore
				case TokenPatterns.COMMENT_MULTI_START:
					self.comment_skip_mode = True
					input = input[len(lexerToken.value):]
					continue
				case TokenPatterns.COMMENT_MULTI_END:
					input = input[len(lexerToken.value):]
					self.comment_skip_mode = False
					continue
				case TokenPatterns.COMMENT_LINE:
					input = input[len(lexerToken.value):]
					continue
				case TokenPatterns.IDENTIFIER:
					lexerToken = self.__test_for_keyword(lexerToken.value)
				case TokenPatterns.ERROR:
					raise ValueError(f"Unexpected character: {input[0]}")
			tokens.append(lexerToken)
			input = input[len(lexerToken.value):]
		return tokens

	def lex_file(self,file_name: str) -> List[LexerToken]:
		tokens: List[LexerToken] = []
		with open(file_name, 'r') as file:
			for line in file:
				tokens = tokens + self.__tokenize_string(line)
		return tokens
