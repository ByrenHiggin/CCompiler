from modules.models.nodes.AST.Operands.ExpressionNode import ExpressionNode
from modules.models.nodes.BaseNode import Operand

class ConstantInteger(ExpressionNode):
	value: str
	def accept(self, visitor, instructions) -> Operand:
		return visitor.visit_constant_integer(self, instructions)