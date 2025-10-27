from typing import Callable, List

from modules.models.AstNodes.BaseNode import BaseNode 
from modules.models.AstNodes.Operands.AST.ConstantInteger import ConstantInteger
from modules.models.AstNodes.Operands.AST.UnaryOperators import BitwiseNot, Negate
from modules.models.AstNodes.Functions.FunctionDefinitionNode import FunctionDefinitionNode
from modules.models.AstNodes.ProgramNode import ProgramNode
from modules.models.AstNodes.Statements.StatementNode import ReturnStatementNode
from modules.models.LexerToken import LexerToken
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenPatterns
from modules.parser.TokenIteratorService import TokenIteratorService

class ParserService():
	functions: List[BaseNode] = []
	expression_handlers: dict[TokenPatterns, Callable[[LexerToken], BaseNode]] = {}
	statement_handlers: dict[TokenPatterns, Callable[[LexerToken], BaseNode]] = {}
	declaration_handlers: dict[TokenPatterns, Callable[[LexerToken], BaseNode]] = {}
	token_iterator: TokenIteratorService

	def __init__(self):
		self.__init_expression_handlers()
		self.__init_statement_handlers()
		self.__init_declaration_handlers()

	def __handle_parentheses(self, token: LexerToken) -> BaseNode:
		# A parenthesized expression starts with '(' and ends with ')'
		statement = None
		while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenPatterns.RPAREN):
			statement = self.__parse_expression()
			token = self.token_iterator.consume_token()
		if statement is None or token.type != TokenPatterns.RPAREN:
			raise ValueError("Invalid statement; Missing closing ')'")
		return statement
		
	def __handle_constant(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		return ConstantInteger(value=token.value)
	
	def __handle_unary_minus(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		return Negate(value=self.__parse_expression())

	def __handle_bitwise_not(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		return BitwiseNot(value=self.__parse_expression())

	def __handle_identifier(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		raise NotImplementedError("Identifier handling not implemented yet")

	def __parse_keyword(self, token: LexerToken) -> BaseNode:
		if token.value == KeyWordPatterns.RETURN.name:
			return ReturnStatementNode(returnValue=self.__parse_expression())
		elif token.value == KeyWordPatterns.VOID.name:
			# Placeholder for VoidNode creation
			return BaseNode()
		else:
			raise ValueError("Unknown keyword")

	def __parse_assignment_expression(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		return BaseNode()

	def __parse_conditional_expression(self, token: LexerToken) -> BaseNode:
		# Placeholder implementation
		return BaseNode()

	def __parse_expression(self) -> BaseNode:
		# An Expression can start with various tokens like '(', CONSTANT, IDENTIFIER, unary operators etc.
		# And end with various tokens depending on the expression type, so we use handlers
		_expression_node = None
		token = self.token_iterator.consume_token()
		
		handler = self.expression_handlers.get(token.type)
		if handler:
			return handler(token)
		else:
			raise ValueError(f"Unhandled token type in expression: {token.type}")

	def __parse_statement(self) -> BaseNode:
		# A statement should start with something and end with ';' 
		statement = None
		token = self.token_iterator.consume_token()
		while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenPatterns.SEMICOLON):
				handler = self.statement_handlers.get(token.type)
				if handler:
					statement = handler(token)
				else:
					raise ValueError(f"Unhandled token type in statement: {token.type}")
				token = self.token_iterator.consume_token()
		if statement is None or token.type != TokenPatterns.SEMICOLON:
			raise ValueError("Invalid statement; Missing closing ';'")
		return statement

	def __parse_function_block(self) -> BaseNode:
		# A function block starts with '{' and ends with '}'
		function_body: BaseNode = BaseNode()
		token = self.token_iterator.consume_token()
		if token.type != TokenPatterns.LBRACE:
			raise ValueError("Expected '{' at the beginning of a function block")
		while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenPatterns.RBRACE):
			function_body = self.__parse_statement()
			token = self.token_iterator.consume_token()
		if token.type != TokenPatterns.RBRACE:
			raise ValueError("Invalid function block; Missing closing '}'")
		return function_body
		
	def __parse_function_parameters(self) -> List[BaseNode]:
		# A function parameter list starts with '(' and ends with ')'
		parameter_list: List[BaseNode] = []
		token = self.token_iterator.consume_token()
		while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenPatterns.RPAREN):
			token = self.token_iterator.consume_token()
			if token.type == TokenPatterns.COMMA:
				token = self.token_iterator.consume_token()
			else:
				if token.type == TokenPatterns.KEYWORD and token.value == KeyWordPatterns.VOID.name:
					# Placeholder for parameter node creation
					parameter_list.append(BaseNode())
		return parameter_list

	def __parse_function(self, type: LexerToken, identifier: LexerToken) -> FunctionDefinitionNode:
		print(f"Parsing function starting with token: {identifier.value}")
		# Placeholder implementation
		parameters = self.__parse_function_parameters()
		body = self.__parse_function_block()
		return FunctionDefinitionNode(name="_"+identifier.value, body=body)

	def __parse_declaration(self) -> BaseNode:
		type_specifier = self.token_iterator.consume_token()
		identifier = self.token_iterator.consume_token()
		next = self.token_iterator.peek_ahead()
		if next.type == TokenPatterns.LPAREN:
			return self.__parse_function(type_specifier, identifier)
		elif next.type == TokenPatterns.ASSIGN:
			return self.__parse_assignment_expression(next)
		elif next.type == TokenPatterns.EQ:
			return self.__parse_conditional_expression(next)
		else:
			raise ValueError(f"Unexpected token after identifier in declaration: {next.type}")

	def parse_lex(self, lex_array: List[LexerToken]) -> ProgramNode:
		print("Parsing lex array...")
		self.token_iterator = TokenIteratorService()
		self.token_iterator.lex_array = lex_array
		self.token_iterator.position = 0
		self.functions = []
		while self.token_iterator.position < len(self.token_iterator.lex_array):
			_peeked_initial_token = self.token_iterator.peek_ahead(0)
			_peeked_second_token = self.token_iterator.peek_ahead(1)
			if _peeked_initial_token.type == TokenPatterns.IDENTIFIER:
				if _peeked_second_token.type == TokenPatterns.IDENTIFIER:
					self.functions.append(self.__parse_declaration())
				else:
					raise ValueError(f"Unexpected token after identifier; {_peeked_second_token.type}")
			elif _peeked_initial_token.type == TokenPatterns.EOF:
				raise ValueError("Unexpected end of file")
		return ProgramNode(functions=self.functions)
	
	def __init_expression_handlers(self):
		self.expression_handlers = {
			TokenPatterns.LPAREN: self.__handle_parentheses,
			TokenPatterns.CONSTANT: self.__handle_constant,
			TokenPatterns.MINUS: self.__handle_unary_minus,
			TokenPatterns.BITWISE_NOT: self.__handle_bitwise_not,
			TokenPatterns.IDENTIFIER: self.__handle_identifier,
		}
  
	def __init_statement_handlers(self):
		self.statement_handlers = {
			TokenPatterns.KEYWORD: self.__parse_keyword
		}
	def __init_declaration_handlers(self):
		self.declaration_handlers = {
			TokenPatterns.EQ: self.__parse_conditional_expression,
			TokenPatterns.ASSIGN: self.__parse_assignment_expression,
			TokenPatterns.LT: self.__parse_conditional_expression,
			TokenPatterns.GT: self.__parse_conditional_expression,
			TokenPatterns.LTE: self.__parse_conditional_expression,
			TokenPatterns.GTE: self.__parse_conditional_expression,
		}