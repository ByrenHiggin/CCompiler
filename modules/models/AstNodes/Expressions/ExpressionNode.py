from modules.models.AstNodes.BaseNode import BaseNode

class ExpressionNode(BaseNode):
	value: str
	def toAsm(self) -> str:
		return f"${self.value}"

class UnaryNode(BaseNode):
	value: BaseNode
	def toAsm(self) -> str:
		return f"${self.value.toAsm()}"