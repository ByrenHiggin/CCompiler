from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Expressions.ExpressionNode import UnaryNode

class BitwiseNot(UnaryNode):
	value: BaseNode
	def toAsm(self) -> str:
		return f"~{self.value.toAsm()}"

class Negate(UnaryNode):
	value: BaseNode
	def toAsm(self) -> str:
		return f"-{self.value.toAsm()}"
