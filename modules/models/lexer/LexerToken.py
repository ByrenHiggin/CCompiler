from modules.models.enums.token_type import TokenPatterns, TokenType
from pydantic import BaseModel

class LexerToken(BaseModel):
	type: TokenPatterns
	value: str
 
class Token(BaseModel):
	type: TokenType
	lineNumber: int
	value: str