from modules.models.enums.token_type import TokenType
from pydantic import BaseModel


class Token(BaseModel):
	type: TokenType
	lineNumber: int
	value: str