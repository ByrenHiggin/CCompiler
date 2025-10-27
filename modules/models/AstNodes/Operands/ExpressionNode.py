from modules.models.AstNodes.BaseNode import BaseNode

class ExpressionNode(BaseNode):
	value: str
	def toAsm(self) -> str:
		raise NotImplementedError("toAsm method not implemented in ExpressionNode")

class UnaryNode(BaseNode):
	value: BaseNode
	def toAsm(self) -> str:
		raise NotImplementedError("toAsm method not implemented in UnaryNode")
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self