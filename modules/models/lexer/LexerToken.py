from modules.models.enums.token_type import TokenPatterns
from pydantic import BaseModel

class LexerToken(BaseModel):
	type: TokenPatterns
	value: str