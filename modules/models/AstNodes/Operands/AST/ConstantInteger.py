from modules.models.AstNodes.Operands.ExpressionNode import ExpressionNode

class ConstantInteger(ExpressionNode):
	value: str
	def accept(self, visitor, instructions):
		return visitor.visit_constant_integer(self, instructions)