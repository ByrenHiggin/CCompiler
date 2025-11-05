from modules.models.AstNodes.BaseNode import Operand
from modules.models.AstNodes.Operands.ExpressionNode import ExpressionNode

class ConstantInteger(ExpressionNode):
	value: str
	def accept(self, visitor, instructions) -> Operand:
		return visitor.visit_constant_integer(self, instructions)