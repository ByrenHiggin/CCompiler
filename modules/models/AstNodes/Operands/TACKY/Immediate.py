from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Operands.ExpressionNode import ExpressionNode

class Immediate(ExpressionNode):
	value: str
	def toAsm(self) -> str:
		return f"${self.value}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self