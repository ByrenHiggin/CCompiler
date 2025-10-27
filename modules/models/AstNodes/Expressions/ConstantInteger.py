from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Expressions.ExpressionNode import ExpressionNode

class ConstantInteger(ExpressionNode):
	value: str
	def toAsm(self) -> str:
		return f"${self.value}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self