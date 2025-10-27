
from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Operands.ExpressionNode import UnaryNode

class BitwiseNot(UnaryNode):
	operand: BaseNode
	def accept(self, visitor, instructions):
		return visitor.visit_bitwise_not(self, instructions)

class Negate(UnaryNode):
	operand: BaseNode
	def accept(self, visitor, instructions):
		return visitor.visit_negate(self, instructions)