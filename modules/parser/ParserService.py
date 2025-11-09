import logging
from typing import Callable, List
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.AST.Operands.BinaryOperators import BinaryAdd, BinaryMinus
from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.AST.Statements.ReturnStatementNode import ReturnStatementNode
from modules.models.nodes.BaseNode import BaseNode 
from modules.models.nodes.AST.ProgramNode import ProgramNode
from modules.models.lexer.LexerToken import Token
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenType
from modules.parser.TokenIteratorService import TokenIteratorService

class ParserService():
    functions: List[BaseNode] = []
    expression_handlers: dict[TokenType, Callable[[Token], BaseNode]] = {}
    statement_handlers: dict[TokenType, Callable[[Token], BaseNode]] = {}
    declaration_handlers: dict[TokenType, Callable[[Token], BaseNode]] = {}
    token_iterator: TokenIteratorService

    def __init__(self):
        self.__init_expression_handlers()
        self.__init_statement_handlers()
        self.__init_declaration_handlers()

    def __handle_parentheses(self, token: Token) -> BaseNode:
        # A parenthesized expression starts with '(' and ends with ')'
        statement = None
        while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenType.RPAREN):
            statement = self.__parse_expression()
            token = self.token_iterator.consume_token()
        if statement is None or token.type != TokenType.RPAREN:
            raise ValueError("Invalid statement; Missing closing ')'")
        return statement

    def __handle_constant(self, token: Token) -> BaseNode:
        # Placeholder implementation
        return ConstantInteger(value=token.value)
    
    def __is_unary_context(self) -> bool:
        previousToken: Token | None = self.token_iterator.peek_behind()
        if previousToken is None:
            return True  # Start of expression
        if previousToken.type not in {
            TokenType.CONSTANT,
            TokenType.IDENTIFIER
        }:
            return True
        return False
    
    def __handle_minus_token(self, token: Token) -> BaseNode:
        # Placeholder implementation
        if self.__is_unary_context():
            return Negate(operand=self.__parse_expression())
        return BinaryMinus(left=self.__parse_expression(), right=self.__parse_expression(), operand=token)

    def __handle_binary_addition(self, token: Token) -> BaseNode:
        return BinaryAdd(left=self.__parse_expression(), right=self.__parse_expression(), operand=token)

    def __handle_bitwise_not(self, token: Token) -> BaseNode:
        # Placeholder implementation
        if self.__is_unary_context():
            return BitwiseNot(operand=self.__parse_expression())
        raise NotImplementedError("bitwise not handling not implemented yet")

    def __parse_keyword(self, token: Token) -> BaseNode:
        if token.value == KeyWordPatterns.RETURN.name:
            return ReturnStatementNode(value=self.__parse_expression())
        else:
            raise ValueError("Unknown keyword")

    def __parse_expression(self) -> BaseNode:
        # An Expression can start with various tokens like '(', CONSTANT, IDENTIFIER, unary operators etc.
        # And end with various tokens depending on the expression type, so we use handlers
        _expression_node = None
        token = self.token_iterator.consume_token()
        next = self.token_iterator.peek_ahead()
        previous = self.token_iterator.peek_behind()
        
        handler = self.expression_handlers.get(token.type)
        if handler:
            return handler(token)
        else:
            raise ValueError(f"Unhandled token type in expression: {token.type}")

    def __parse_statement(self) -> BaseNode:
        # A statement should start with something and end with ';' 
        statement = None
        token = self.token_iterator.consume_token()
        while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenType.SEMICOLON):
                handler = self.statement_handlers.get(token.type)
                if handler:
                    statement = handler(token)
                else:
                    raise ValueError(f"Unhandled token type in statement: {token.type}")
                token = self.token_iterator.consume_token()
        if statement is None or token.type != TokenType.SEMICOLON:
            raise ValueError("Invalid statement; Missing closing ';'")
        return statement

    def __parse_identifier(self, token: Token) -> BaseNode:
        # Placeholder implementation
        previousToken: Token = self.token_iterator.peek_behind()
        nextPeek: Token = self.token_iterator.peek_ahead()
        match token.type:
            case TokenType.IDENTIFIER:
                if previousToken and previousToken.type == TokenType.IDENTIFIER and nextPeek.type == TokenType.LPAREN:
                    return self.__parse_function(type=previousToken, identifier=token)
                return self.__parse_declaration()
            case TokenType.LPAREN:
                raise ValueError("Unexpected token before function identifier")
            case TokenType.ASSIGN:
                return self.__parse_assignment_expression(nextPeek)
            case TokenType.EQ | TokenType.LT | TokenType.GT | TokenType.LTE | TokenType.GTE:
                return self.__parse_conditional_expression(nextPeek)
            case _:
                raise ValueError(f"Unexpected token after identifier in declaration: {nextPeek.type}")
        pass

    def __parse_function_block(self) -> BaseNode:
        # A function block starts with '{' and ends with '}'
        function_body = None
        token = self.token_iterator.consume_token()
        if token.type != TokenType.LBRACE:
            raise ValueError("Expected '{' at the beginning of a function block")
        while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenType.RBRACE):
            function_body = self.__parse_statement()
            token = self.token_iterator.consume_token()
        if function_body is None or token.type != TokenType.RBRACE:
            raise ValueError("Invalid function block; Missing closing '}'")
        return function_body
        
    def __parse_function_parameters(self) -> List[BaseNode]:
        # A function parameter list starts with '(' and ends with ')'
        parameter_list: List[BaseNode] = []
        token = self.token_iterator.consume_token()
        while self.token_iterator.iterate_tokens_until_type_or_error(token.type, TokenType.RPAREN):
            token = self.token_iterator.consume_token()
            if token.type == TokenType.COMMA:
                token = self.token_iterator.consume_token()
            else:
                if token.type == TokenType.KEYWORD and token.value == KeyWordPatterns.VOID.name:
                    # Placeholder for parameter node creation
                    logging.info("Function has void parameter list")
        return parameter_list

    def __parse_function(self, type: Token, identifier: Token) -> FunctionDefinitionNode:
        print(f"Parsing function starting with token: {identifier.value}")
        # Placeholder implementation
        params = self.__parse_function_parameters()
        body = self.__parse_function_block()
        return FunctionDefinitionNode(name="_"+identifier.value, params=params, body=body)

    def __parse_declaration(self) -> BaseNode:
        token = self.token_iterator.consume_token()
        handler = self.declaration_handlers.get(token.type)
        if handler:
            statement = handler(token)
            return statement
        else:
            raise ValueError(f"Unhandled token type in statement: {token.type}")

    def parse_lex(self, lex_array: List[Token]) -> ProgramNode:
        print("Parsing lex array...")
        self.token_iterator = TokenIteratorService()
        self.token_iterator.lex_array = lex_array
        self.token_iterator.position = 0
        self.functions = []
        while self.token_iterator.position < len(self.token_iterator.lex_array):
            self.functions.append(self.__parse_declaration())
        return ProgramNode(functions=self.functions)
    
    def __init_expression_handlers(self):
        self.expression_handlers = {
            TokenType.LPAREN: self.__handle_parentheses,
            TokenType.CONSTANT: self.__handle_constant,
            TokenType.MINUS: self.__handle_minus_token,
            TokenType.BITWISE_NOT: self.__handle_bitwise_not,
            TokenType.PLUS: self.__handle_binary_addition,
        }
  
    def __init_statement_handlers(self):
        self.statement_handlers = {
            TokenType.KEYWORD: self.__parse_keyword
        }
    def __init_declaration_handlers(self):
        self.declaration_handlers = {
            TokenType.IDENTIFIER: self.__parse_identifier,
        }