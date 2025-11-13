from modules.models.enums.token_type import TokenType
from pydantic import BaseModel

class LexerToken(BaseModel):
	type: TokenType 
	value: str
 
