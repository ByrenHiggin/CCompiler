from typing import List

from pydantic import BaseModel
from modules.models.AstNodes.BaseNode import BaseNode, ProgramNode
from modules.models.AstNodes.Expressions.ConstantInteger import ConstantInteger
from modules.models.AstNodes.Expressions.ExpressionNode import ExpressionNode
from modules.models.AstNodes.Functions.FunctionDefinitionNode import FunctionDefinitionNode
from modules.models.AstNodes.Statements.StatementNode import StatementNode
from modules.models.LexerToken import LexerToken
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenPatterns

class ParserService(BaseModel):
	position: int = 0
	lex_array: List[LexerToken] = []
	functions: List[BaseNode] = []

	def __iterate_tokens_until_type_or_error(self, token: TokenPatterns, target_type: TokenPatterns) -> bool:
		if token == TokenPatterns.EOF or self.position > len(self.lex_array):
			return False
		return token != target_type

	def __parse_expression(self) -> ExpressionNode:
		# Placeholder implementation
		_expression_node = None
		token = self.__consume_token()
		while self.__iterate_tokens_until_type_or_error(token.type, TokenPatterns.SEMICOLON): 
			if token.type == TokenPatterns.CONSTANT:
				_expression_node = ConstantInteger(value=token.value)
			token = self.__consume_token()
		if _expression_node is None or token.type != TokenPatterns.SEMICOLON:
			raise ValueError("Invalid expression; Invalid symbols or missing Semicolon")
		return _expression_node

	def __parse_statement(self) -> StatementNode:
		# Placeholder implementation
		token = self.__consume_token()
		if token.type != TokenPatterns.LBRACE:
			raise ValueError("Expected '{' at the beginning of a statement block")
		statement = None
		while self.__iterate_tokens_until_type_or_error(token.type, TokenPatterns.RBRACE):
			_peeked_token = self.__peek_ahead()
			if _peeked_token.type == TokenPatterns.KEYWORD and _peeked_token.value == KeyWordPatterns.RETURN.name: 
				self.__consume_token()  # consume 'return' keyword
				statement = StatementNode(returnValue=self.__parse_expression())
			token = self.__consume_token()
		if statement is None or token.type != TokenPatterns.RBRACE:
			raise ValueError("Invalid statement; Missing return statement or closing '}'")
		return statement
		
	def __parse_function_parameters(self) -> List[BaseNode]:
		parameter_list: List[BaseNode] = []
		token = self.__consume_token()
		while self.__iterate_tokens_until_type_or_error(token.type, TokenPatterns.RPAREN):
			token = self.__consume_token()
			if token.type == TokenPatterns.COMMA:
				token = self.__consume_token()
			else:
				if token.type == TokenPatterns.KEYWORD and token.value == KeyWordPatterns.VOID.name:
					# Placeholder for parameter node creation
					parameter_list.append(BaseNode())
		return parameter_list

	def __parse_function(self, type: LexerToken, identifier: LexerToken) -> FunctionDefinitionNode:
		print(f"Parsing function starting with token: {identifier.value}")
		# Placeholder implementation
		parameters = self.__parse_function_parameters()
		body = self.__parse_statement()
		return FunctionDefinitionNode(name="_"+identifier.value, body=body)

	def __parse_declaration(self, type: LexerToken, identifier: LexerToken) -> BaseNode:
		type_specifier = type
		identifier = identifier
		next = self.__peek_ahead()
		if next.type == TokenPatterns.LPAREN:
			return self.__parse_function(type_specifier, identifier)
		elif next.type == TokenPatterns.ASSIGN:
			# Placeholder for variable declaration without initialization
			return BaseNode()
		else:
			raise ValueError("Unexpected token after identifier in declaration")

	def __peek_ahead(self) -> LexerToken:
		if self.position < len(self.lex_array):
			return self.lex_array[self.position]
		return LexerToken(type=TokenPatterns.ERROR, value="")
	
	def __consume_token(self) -> LexerToken:
		if self.position < len(self.lex_array):
			current_token = self.lex_array[self.position]
			self.position += 1
			return current_token
		return LexerToken(type=TokenPatterns.EOF, value="")

	def parse_lex(self, lex_array: List[LexerToken]) -> ProgramNode:
		print("Parsing lex array...")
		self.lex_array = lex_array
		self.position = 0
		self.functions = []
		while self.position < len(self.lex_array):
			current_token = self.__consume_token()	
			if current_token.type == TokenPatterns.IDENTIFIER:
				next_token = self.__consume_token()
				if next_token.type == TokenPatterns.IDENTIFIER:
					self.functions.append(self.__parse_declaration(current_token, next_token))
				else:
					raise ValueError("Unexpected token after identifier")
			elif current_token.type == TokenPatterns.EOF:
				raise ValueError("Unexpected end of file")
		return ProgramNode(functions=self.functions)