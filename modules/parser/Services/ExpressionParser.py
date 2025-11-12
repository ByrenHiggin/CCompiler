from modules.models.enums.token_type import TokenType
from modules.models.nodes.AST.Operands.BinaryOperators import BinaryAdd, BinaryDivide, BinaryMinus, BinaryModulus, BinaryMultiply
from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.BaseNode import BaseNode
from modules.parser.Services.TokenIteratorService import TokenIteratorService


class ExpressionParser:
    token_iterator: TokenIteratorService
    
    def __init__(self, token_iterator: TokenIteratorService):
        self.token_iterator = token_iterator

    def parse_expression(self) -> BaseNode:
        return self.__parse_additive()    
    
    def __parse_additive(self) -> BaseNode:
        left = self.__parse_multiplicative()

        while self.token_iterator.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.token_iterator.lookbehind()
            right = self.__parse_multiplicative()
            if operator.type == TokenType.PLUS:
                left = BinaryAdd(left=left, right=right)
            elif operator.type == TokenType.MINUS:
                left = BinaryMinus(left=left, right=right)
                
        return left

    def __parse_multiplicative(self) -> BaseNode:
        left = self.__parse_unary()

        while self.token_iterator.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULUS):
            operator = self.token_iterator.lookbehind()
            right = self.__parse_unary()
            if operator.type == TokenType.MULTIPLY:
                left = BinaryMultiply(left=left, right=right)
            elif operator.type == TokenType.DIVIDE:
                left = BinaryDivide(left=left, right=right)
            elif operator.type == TokenType.MODULUS:
                left = BinaryModulus(left=left, right=right)
                
        return left

    def __parse_unary(self) -> BaseNode:
        if self.token_iterator.match(TokenType.MINUS):
            operator = self.token_iterator.lookbehind()
            return Negate(operand=self.__parse_unary())
        if self.token_iterator.match(TokenType.BITWISE_NOT):
            operator = self.token_iterator.lookbehind()
            return BitwiseNot(operand=self.__parse_unary())
        return self.__parse_primary()

    def __parse_primary(self) -> BaseNode:
        if self.token_iterator.match(TokenType.CONSTANT):
            return self.__handle_constant()
        #elif self.__token_in_type_set(token, [TokenType.IDENTIFIER]):
            #return VariableReference(name=token.value)
        if self.token_iterator.match(TokenType.LPAREN):
            st = self.__handle_parentheses()
            self.token_iterator.consume(TokenType.RPAREN, "Expected ')' after expression")
            return st
        
        current = self.token_iterator.current()
        raise ValueError(f"Unhandled token type in primary: {current.type}")
    
    def __handle_parentheses(self) -> BaseNode:
        # Placeholder implementation
        expr = self.parse_expression()
        return expr
    
    def __handle_constant(self) -> BaseNode:
        # Placeholder implementation
        token = self.token_iterator.lookbehind()
        return ConstantInteger(value=token.value)
    