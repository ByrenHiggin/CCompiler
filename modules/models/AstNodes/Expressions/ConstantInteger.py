from modules.models.AstNodes.Expressions.ExpressionNode import ExpressionNode
from pydantic import BaseModel

class ConstantInteger(ExpressionNode):
	value: str
