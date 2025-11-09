from typing import Callable, List
from modules.models.nodes.AST.Expressions import ExpressionStatementNode
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.AST.Operands.BinaryOperators import BinaryAdd, BinaryDivide, BinaryMinus, BinaryModulus, BinaryMultiply
from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.AST.Statements.ReturnStatementNode import ReturnStatementNode
from modules.models.nodes.BaseNode import BaseNode 
from modules.models.nodes.AST.ProgramNode import ProgramNode
from modules.models.lexer.LexerToken import Token
from modules.models.enums.token_type import TokenType
from modules.parser.TokenIteratorService import TokenIteratorService
from modules.models.enums.keyword_patterns import KeyWordPatterns



class ParserServiceV2():
    functions: List[BaseNode] = []
    expression_handlers: dict[TokenType, Callable[[], BaseNode]] = {}
    statement_handlers: dict[TokenType, Callable[[], BaseNode]] = {}
    declaration_handlers: dict[str, Callable[[], BaseNode]] = {}
    token_iterator: TokenIteratorService
    
    def __init__(self):
        self.__init_expression_handlers()
        self.__init_statement_handlers()
        self.__init_declaration_handlers()
    
    ##Sub Parsers

    def __parse_function_declaration(self) -> BaseNode:
        return_type = self.__consume(TokenType.IDENTIFIER, "Expected return type")
        name = self.__consume(TokenType.IDENTIFIER, "Expected function name")
        params = self.__parse_function_parameters()
        body = self.__parse_function_block()[0] # Assuming single body node for simplicity
        return FunctionDefinitionNode(name=name.value, params=params, body=body)

    def __parse_function_parameters(self) -> List[BaseNode]:
        self.__consume(TokenType.LPAREN, "Expected '(' at start of function parameters")
        parameters = []
        while not self.__check(TokenType.RPAREN):
            if self.__check(TokenType.KEYWORD):
                param_type = self.__advance()
                if param_type.value == "VOID":
                    break
                name = self.__consume(TokenType.IDENTIFIER, "Expected parameter name")
                parameters.append((param_type, name))
            elif self.__check(TokenType.IDENTIFIER):
                param_type = self.__advance()
                name = self.__consume(TokenType.IDENTIFIER, "Expected parameter name")
                parameters.append((param_type, name))
            
            if self.__check(TokenType.COMMA):
                self.__advance()
            elif not self.__check(TokenType.RPAREN):
                raise ValueError("Expected ',' or ')' in parameter list")
                
        self.__consume(TokenType.RPAREN, "Expected ')' at end of function parameters")
        return parameters

    def __parse_function_block(self) -> List[BaseNode]:
        self.__consume(TokenType.LBRACE, "Expected '{' at start of function block")
        statements = []
        while not self.__check(TokenType.RBRACE) and not self.__at_end():
            statements.append(self._parse_statement())
        self.__consume(TokenType.RBRACE, "Expected '}' at end of function block")
        return statements

    def __determine_declaration_type(self) -> str | None:
        """
        Determine if we're looking at a function or variable declaration.
        Expected patterns:
        - Function: <type> <name> ( ... )
        - Variable: <type> <name> = ... or <type> <name> ;
        """
        current_token = self.__current()  # Should be the type (e.g., "int")
        
        # Look ahead to see the pattern
        if self.token_iterator.position + 2 < len(self.token_iterator.lex_array):
            next_token = self.token_iterator.peek_ahead(self.token_iterator.position + 1)  # Should be name (e.g., "main")
            token_after_next = self.token_iterator.peek_ahead(self.token_iterator.position + 2)  # Should be "(" for function
            
            # Check for function pattern: type identifier (
            if (self.__token_in_type_set(current_token, [TokenType.IDENTIFIER, TokenType.KEYWORD]) and
                self.__token_in_type_set(next_token, [TokenType.IDENTIFIER]) and
                self.__token_in_type_set(token_after_next, [TokenType.LPAREN])):
                return "function"
        
        # Look ahead for variable pattern: type identifier = or type identifier ;
        if self.token_iterator.position + 1 < len(self.token_iterator.lex_array):
            next_token = self.token_iterator.peek_ahead(self.token_iterator.position + 1)
            if self.token_iterator.position + 2 < len(self.token_iterator.lex_array):
                token_after_next = self.token_iterator.peek_ahead(self.token_iterator.position + 2)
                
                if (self.__token_in_type_set(current_token, [TokenType.IDENTIFIER, TokenType.KEYWORD]) and
                    self.__token_in_type_set(next_token, [TokenType.IDENTIFIER]) and
                    self.__token_in_type_set(token_after_next, [TokenType.ASSIGN, TokenType.SEMICOLON])):
                    return "variable"
        
        # If we can't determine the type, return None
        return None
        
    def __parse_unary(self, token: Token) -> BaseNode:
        if token.type == TokenType.MINUS:
            return Negate(operand=self._parse_expression())
        elif token.type == TokenType.BITWISE_NOT:
            return BitwiseNot(operand=self._parse_expression())
        else:
            raise NotImplementedError("Unary or binary parsing not implemented yet")
        
    def __parse_keyword(self, token: Token) -> BaseNode:
        match token.value:
            case KeyWordPatterns.RETURN.name:
                expr = ReturnStatementNode(value=self._parse_expression())
                self.__consume(TokenType.SEMICOLON, "Expected ';' after return statement")
                return expr
            case _:
                raise ValueError("Unknown keyword")
    
    def __handle_constant(self, token: Token) -> BaseNode:
        # Placeholder implementation
        return ConstantInteger(value=token.value)
    
    def __parse_additive(self) -> BaseNode:
        left = self.__parse_multiplicative()

        while self.__match(TokenType.PLUS, TokenType.MINUS):
            operator = self.__lookbehind()
            right = self.__parse_multiplicative()
            if operator.type == TokenType.PLUS:
                left = BinaryAdd(left=left, right=right)
            elif operator.type == TokenType.MINUS:
                left = BinaryMinus(left=left, right=right)
                
        return left

    def __parse_multiplicative(self) -> BaseNode:
        left = self.__parse_unary()

        while self.__match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULUS):
            operator = self.__lookbehind()
            right = self.__parse_unary()
            if operator.type == TokenType.MULTIPLY:
                left = BinaryMultiply(left=left, right=right)
            elif operator.type == TokenType.DIVIDE:
                left = BinaryDivide(left=left, right=right)
            elif operator.type == TokenType.MODULUS:
                left = BinaryModulus(left=left, right=right)
                
        return left

    def __parse_unary(self) -> BaseNode:
        if self.__match(TokenType.MINUS):
            operator = self.__lookbehind()
            return Negate(operand=self.__parse_unary())
        if self.__match(TokenType.BITWISE_NOT):
            operator = self.__lookbehind()
            return BitwiseNot(operand=self.__parse_unary())
        return self.__parse_primary()

    def __parse_primary(self) -> BaseNode:
        if self.__match(TokenType.CONSTANT):
            return self.__handle_constant(self.__lookbehind())
        #elif self.__token_in_type_set(token, [TokenType.IDENTIFIER]):
            #return VariableReference(name=token.value)
        if self.__match(TokenType.LPAREN):
            st = self.__handle_parentheses()
            self.__consume(TokenType.RPAREN, "Expected ')' after expression")
            return st
        
        current = self.__current()
        raise ValueError(f"Unhandled token type in primary: {current.type}")
    
    def __handle_parentheses(self) -> BaseNode:
        # Placeholder implementation
        expr = self._parse_expression()
        return expr
   
    
    ##Top Level Parsers

    def _parse_expression(self) -> BaseNode:
        return self.__parse_additive()        
    
    def _parse_statement(self) -> BaseNode:
        if self.__check(TokenType.KEYWORD):
            keyword = self.__advance()
            if keyword.value == KeyWordPatterns.RETURN.name:
                st = ReturnStatementNode(value=self._parse_expression())
                self.__consume(TokenType.SEMICOLON, "Expected ';' after return statement")
                return st
        
        expr = self._parse_expression()
        self.__consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExpressionStatementNode(expression=expr)
        

    def _parse_declaration(self) -> BaseNode:
        declaration_type = self.__determine_declaration_type()
        if declaration_type is None:
            current = self.__current()
            raise ValueError(f"Unable to determine declaration type for token: {current.type}")
            
        handler = self.declaration_handlers.get(declaration_type)
        if handler:
            statement = handler()
            return statement
        else:
            raise ValueError(f"Unhandled declaration type: {declaration_type}")

    ## Entry Point
    def parse_lex(self, lex_array: List[Token]) -> ProgramNode:
        print("Parsing lex array...")
        self.token_iterator = TokenIteratorService()
        self.token_iterator.lex_array = lex_array
        self.token_iterator.position = 0
        self.functions = []
        while self.token_iterator.position < len(self.token_iterator.lex_array):
            self.functions.append(self._parse_declaration())
        return ProgramNode(functions=self.functions)
    
    ## Initialization of Handlers
    def __init_expression_handlers(self):
        self.expression_handlers = {
        }
  
    def __init_statement_handlers(self):
        self.statement_handlers = {
        }
    def __init_declaration_handlers(self):
        self.declaration_handlers = {
            "function": self.__parse_function_declaration
        }
        
    ##Utility 
    
    def __match(self, *types: TokenType) -> bool:
        """Check if current token matches any type and consume if so"""
        for token_type in types:
            if self.__check(token_type):
                self.__advance()
                return True
        return False
    
    def __current(self) -> Token:
        return self.token_iterator.current_token()
     
    def __lookahead(self) -> Token:
        return self.token_iterator.peek_ahead(self.token_iterator.position+1)
    
    def __lookbehind(self) -> Token | None:
        return self.token_iterator.peek_behind(self.token_iterator.position-1)

    def __token_in_type_set(self, token: Token, types: list[TokenType]) -> bool:
        return token.type in types
    
    def __check(self, token_type: TokenType) -> bool:
        """Check current token type without consuming"""
        if self.__at_end():
            return False
        return self.__current().type == token_type
    
    def __advance(self) -> Token:
        """Consume current token and return it"""
        current = self.__current()
        if not self.__at_end():
            self.token_iterator.position += 1
        return current
    
    def __at_end(self) -> bool:
        """Check if at end of tokens"""
        return self.token_iterator.position >= len(self.token_iterator.lex_array)

    def __consume(self, token_type: TokenType, message: str) -> Token:   
        """Consume expected token or error"""
        if self.__check(token_type):
            return self.__advance()
        
        current = self.__current()
        raise SyntaxError(f"{message}. Got: {current.type if current else 'EOF'}")