from modules.models.enums.token_type import TokenType
from modules.models.nodes.AST.Operands.BinaryOperators import * 
from modules.models.nodes.AST.Operands.BitwiseOperators import *
from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
from modules.models.nodes.AST.Operands.RelationalOperators import *
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.BaseNode import BaseNode
from modules.parser.Services.TokenIteratorService import TokenIteratorService


class ExpressionParser:
    token_iterator: TokenIteratorService
    
    def __init__(self, token_iterator: TokenIteratorService):
        self.token_iterator = token_iterator

    def parse_expression(self) -> BaseNode:
        return self.__parse_logical_or()
    
    def __parse_logical_or(self) -> BaseNode:
        left = self.__parse_logical_and()
        while self.token_iterator.match(TokenType.LOGICAL_OR):
            right = self.__parse_logical_and()
            left = BitwiseOr(left=left, right=right)
        return left  
    
    def __parse_logical_and(self) -> BaseNode:
        left = self.__parse_bitwise_or()
        while self.token_iterator.match(TokenType.LOGICAL_AND):
            right = self.__parse_bitwise_or()
            left = BitwiseOr(left=left, right=right)
        return left 
    
    def __parse_bitwise_or(self) -> BaseNode:
        left = self.__parse_bitwise_xor()
        while self.token_iterator.match(TokenType.BITWISE_OR):
            right = self.__parse_bitwise_xor()
            left = BitwiseOr(left=left, right=right)
        return left
     
    def __parse_bitwise_xor(self) -> BaseNode:
        left = self.__parse_bitwise_and()
        while self.token_iterator.match(TokenType.BITWISE_XOR):
            right = self.__parse_bitwise_and()
            left = BitwiseXor(left=left, right=right)
        return left
    
    def __parse_bitwise_and(self) -> BaseNode:
        left = self.__parse_relational_comparison()
        while self.token_iterator.match(TokenType.BITWISE_AND):
            right = self.__parse_relational_comparison()
            left = BitwiseAnd(left=left, right=right)
        return left
    
    def __parse_relational_comparison(self) -> BaseNode:
        left = self.__parse_relational_lt_gt_comparison()
        while self.token_iterator.match(TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            operator = self.token_iterator.lookbehind()
            right = self.__parse_relational_lt_gt_comparison()
            if operator.type == TokenType.EQ:
                left = EqualRelation(left=left, right=right)
            elif operator.type == TokenType.NEQ:
                left = NotEqualRelation(left=left, right=right)
        return left
    
    def __parse_relational_lt_gt_comparison(self) -> BaseNode:
        left = self.__parse_bitwise_shift()
        while self.token_iterator.match(TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE):
            operator = self.token_iterator.lookbehind()
            right = self.__parse_bitwise_shift()
            if operator.type == TokenType.LT:
                left = LessThanRelation(left=left, right=right)
            elif operator.type == TokenType.LTE:
                return LessThanEqualRelation(left=left, right=right)
            elif operator.type == TokenType.GT:
                return GreaterThanRelation(left=left, right=right)
            elif operator.type == TokenType.GTE:
                return GreaterThanEqualRelation(left=left, right=right)
        return left
    
    def __parse_bitwise_shift(self) -> BaseNode:
        left = self.__parse_additive()
        while self.token_iterator.match(TokenType.SHIFT_LEFT, TokenType.SHIFT_RIGHT):
            operator = self.token_iterator.lookbehind()
            right = self.__parse_additive()
            if operator.type == TokenType.SHIFT_LEFT:
                left = BitwiseLeftShift(left=left, right=right)
            elif operator.type == TokenType.SHIFT_RIGHT:
                left = BitwiseRightShift(left=left, right=right)
        return left
        
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
        if self.token_iterator.match(TokenType.NOT):
            operator = self.token_iterator.lookbehind()
            return BitwiseNot(operand=self.__parse_unary())
        return self.__parse_primary()

    def __parse_primary(self) -> BaseNode:
        if self.token_iterator.match(TokenType.CONSTANT):
            return self.__handle_constant()
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
    