from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Operands.ExpressionNode import ExpressionNode
from modules.models.AstNodes.Operands.TACKY.Immediate import Immediate

class ConstantInteger(ExpressionNode):
	value: str
	def toAsm(self) -> str:
		return f"${self.value}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return Immediate(value=self.value)