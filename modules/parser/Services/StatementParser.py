from typing import List
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenType
from modules.models.lexer.Token import Token
from modules.models.nodes.AST.Expressions import ExpressionStatementNode
from modules.models.nodes.AST.Statements.ReturnStatementNode import ReturnStatementNode
from modules.models.nodes.BaseNode import BaseNode
from modules.parser.Services.ExpressionParser import ExpressionParser
from modules.parser.Services.TokenIteratorService import TokenIteratorService


class StatementParser:
    token_iterator: TokenIteratorService
    
    def __init__(self, token_iterator: TokenIteratorService, expression_parser: ExpressionParser):
        self.token_iterator = token_iterator
        self.expression_parser = expression_parser

    def _parse_statement(self) -> BaseNode:
        if self.token_iterator.check(TokenType.KEYWORD):
            keyword = self.token_iterator.advance()
            if keyword.value == KeyWordPatterns.RETURN.name:
                st = ReturnStatementNode(value=self.expression_parser.parse_expression())
                self.token_iterator.consume(TokenType.SEMICOLON, "Expected ';' after return statement")
                return st
        
        expr = self.expression_parser.parse_expression()
        self.token_iterator.consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExpressionStatementNode(expression=expr)
    
    def parse_function_block(self) -> List[BaseNode]:
        self.token_iterator.consume(TokenType.LBRACE, "Expected '{' at start of function block")
        statements = []
        while not self.token_iterator.check(TokenType.RBRACE) and not self.token_iterator.at_end():
            statements.append(self._parse_statement())
        self.token_iterator.consume(TokenType.RBRACE, "Expected '}' at end of function block")
        return statements
    
    def __parse_keyword(self, token: Token) -> BaseNode:
        match token.value:
            case KeyWordPatterns.RETURN.name:
                expr = ReturnStatementNode(value=self.expression_parser.parse_expression())
                self.token_iterator.consume(TokenType.SEMICOLON, "Expected ';' after return statement")
                return expr
            case _:
                raise ValueError("Unknown keyword")
    

