from typing import List
from modules.models.lexer.Token import Token
from modules.models.enums.token_type import TokenType

class TokenIteratorService():
    position: int = 0
    lex_array: List[Token] = []

    def at_end(self) -> bool:
        return self.position >= len(self.lex_array)
 
    def iterate_tokens_until_type_or_error(self, token: TokenType, target_type: TokenType) -> bool:
        if self.at_end():
            return False
        return token != target_type

    def consume_token(self) -> Token:
        if self.position < len(self.lex_array):
            current_token = self.lex_array[self.position]
            self.position += 1
            return current_token
        return Token(type=TokenType.EOF, lineNumber=-1, value="")

    def current(self) -> Token:
        if self.position < len(self.lex_array):
            return self.lex_array[self.position]
        return Token(type=TokenType.EOF, lineNumber=-1, value="")

    def peek_ahead(self, index: int = 0) -> Token:
        if index < len(self.lex_array):
            return self.lex_array[index]
        return Token(type=TokenType.ERROR, lineNumber=-1, value="")

    def peek_behind(self, index: int = 0) -> Token | None:
        if index >= 0:
            return self.lex_array[index]
        return None

    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any type and consume if so"""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
     
    def lookahead(self) -> Token:
        return self.peek_ahead(self.position+1)
    
    def lookbehind(self) -> Token | None:
        return self.peek_behind(self.position-1)

    def token_in_type_set(self, token: Token, types: list[TokenType]) -> bool:
        return token.type in types
    
    def check(self, *token_type: TokenType) -> bool:
        """Check current token type without consuming"""
        if self.at_end():
            return False
        return self.current().type in token_type
    
    def advance(self) -> Token:
        """Consume current token and return it"""
        current = self.current()
        if not self.at_end():
            self.position += 1
        return current
    
    def at_end(self) -> bool:
        """Check if at end of tokens"""
        return self.position >= len(self.lex_array)

    def consume(self, token_type: TokenType, message: str) -> Token:   
        """Consume expected token or error"""
        if self.check(token_type):
            return self.advance()
        
        current = self.current()
        raise SyntaxError(f"{message}. Got: {current.type if current else 'EOF'}")