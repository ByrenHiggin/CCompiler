from modules.models.AstNodes.AST.Operands.ExpressionNode import ExpressionNode
from modules.models.AstNodes.BaseNode import Operand

class ConstantInteger(ExpressionNode):
	value: str
	def accept(self, visitor, instructions) -> Operand:
		return visitor.visit_constant_integer(self, instructions)