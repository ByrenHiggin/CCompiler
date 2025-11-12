from typing import Callable, List
from modules.models.enums.keyword_patterns import KeyWordPatterns
from modules.models.enums.token_type import TokenType
from modules.models.lexer.Token import Token
from modules.models.nodes.AST.Expressions import ExpressionStatementNode
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.AST.Statements.ReturnStatementNode import ReturnStatementNode
from modules.models.nodes.BaseNode import BaseNode
from modules.parser.Services.ExpressionParser import ExpressionParser
from modules.parser.Services.StatementParser import StatementParser
from modules.parser.Services.TokenIteratorService import TokenIteratorService


class FunctionParser:
    token_iterator: TokenIteratorService
    expression_parser: ExpressionParser
    statement_parser: StatementParser
    declaration_handlers: dict[str, Callable[[], BaseNode]] = {}
    
    def __init__(self, token_iterator: TokenIteratorService, expression_parser: ExpressionParser, statement_parser: StatementParser):
        self.token_iterator = token_iterator
        self.expression_parser = expression_parser
        self.statement_parser = statement_parser
        self.__init_declaration_handlers()
    
    def __parse_function_parameters(self) -> List[BaseNode]:
        self.token_iterator.consume(TokenType.LPAREN, "Expected '(' at start of function parameters")
        parameters = []
        while not self.token_iterator.check(TokenType.RPAREN):
            if self.token_iterator.check(TokenType.KEYWORD):
                param_type = self.token_iterator.advance()
                if param_type.value == "VOID":
                    break
                name = self.token_iterator.consume(TokenType.IDENTIFIER, "Expected parameter name")
                parameters.append((param_type, name))
            elif self.token_iterator.check(TokenType.IDENTIFIER):
                param_type = self.token_iterator.advance()
                name = self.token_iterator.consume(TokenType.IDENTIFIER, "Expected parameter name")
                parameters.append((param_type, name))
            
            if self.token_iterator.check(TokenType.COMMA):
                self.token_iterator.advance()
            elif not self.token_iterator.check(TokenType.RPAREN):
                raise ValueError("Expected ',' or ')' in parameter list")
                
        self.token_iterator.consume(TokenType.RPAREN, "Expected ')' at end of function parameters")
        return parameters
    
    def __parse_function_declaration(self) -> BaseNode:
        return_type = self.token_iterator.consume(TokenType.IDENTIFIER, "Expected return type")
        name = self.token_iterator.consume(TokenType.IDENTIFIER, "Expected function name")
        params = self.__parse_function_parameters()
        body = self.statement_parser.parse_function_block()[0] # Assuming single body node for simplicity
        return FunctionDefinitionNode(name=name.value, params=params, body=body)
    

    def determine_declaration_type(self) -> str | None:
        """
        Determine if we're looking at a function or variable declaration.
        Expected patterns:
        - Function: <type> <name> ( ... )
        - Variable: <type> <name> = ... or <type> <name> ;
        """
        current_token = self.token_iterator.current()  # Should be the type (e.g., "int")
        
        # Look ahead to see the pattern
        if self.token_iterator.position + 2 < len(self.token_iterator.lex_array):
            next_token = self.token_iterator.peek_ahead(self.token_iterator.position + 1)  # Should be name (e.g., "main")
            token_after_next = self.token_iterator.peek_ahead(self.token_iterator.position + 2)  # Should be "(" for function
            
            # Check for function pattern: type identifier (
            if (self.token_iterator.token_in_type_set(current_token, [TokenType.IDENTIFIER, TokenType.KEYWORD]) and
                self.token_iterator.token_in_type_set(next_token, [TokenType.IDENTIFIER]) and
                self.token_iterator.token_in_type_set(token_after_next, [TokenType.LPAREN])):
                return "function"
        
        # Look ahead for variable pattern: type identifier = or type identifier ;
        if self.token_iterator.position + 1 < len(self.token_iterator.lex_array):
            next_token = self.token_iterator.peek_ahead(self.token_iterator.position + 1)
            if self.token_iterator.position + 2 < len(self.token_iterator.lex_array):
                token_after_next = self.token_iterator.peek_ahead(self.token_iterator.position + 2)
                
                if (self.token_iterator.token_in_type_set(current_token, [TokenType.IDENTIFIER, TokenType.KEYWORD]) and
                    self.token_iterator.token_in_type_set(next_token, [TokenType.IDENTIFIER]) and
                    self.token_iterator.token_in_type_set(token_after_next, [TokenType.ASSIGN, TokenType.SEMICOLON])):
                    return "variable"
        
        # If we can't determine the type, return None
        return None
    
    def parse_declaration(self) -> FunctionDefinitionNode:
        declaration_type = self.determine_declaration_type()
        if declaration_type is None:
            current = self.token_iterator.current()
            raise ValueError(f"Unable to determine declaration type for token: {current.type}")
            
        handler = self.declaration_handlers.get(declaration_type)
        if handler:
            statement = handler()
            return statement
        else:
            raise ValueError(f"Unhandled declaration type: {declaration_type}")
        
    def __init_declaration_handlers(self):
        self.declaration_handlers = {
            "function": self.__parse_function_declaration
        }
        