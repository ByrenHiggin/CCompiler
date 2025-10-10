from modules.models.AstNodes import AstNode
from pydantic import BaseModel

class ExpressionNode(AstNode):
	value: str
