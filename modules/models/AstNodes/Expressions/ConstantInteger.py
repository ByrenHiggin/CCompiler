from modules.models.AstNodes.Expressions.ExpressionNode import ExpressionNode

class ConstantInteger(ExpressionNode):
	value: str
	def toAsm(self) -> str:
		return f"${self.value}"
