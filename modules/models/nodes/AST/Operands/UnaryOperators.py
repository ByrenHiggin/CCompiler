
from modules.models.AstNodes.AST.Operands.ExpressionNode import UnaryNode
from modules.models.AstNodes.BaseNode import BaseNode

class BitwiseNot(UnaryNode):
	operand: BaseNode
	def accept(self, visitor, instructions):
		return visitor.visit_bitwise_not(self, instructions)

class Negate(UnaryNode):
	operand: BaseNode
	def accept(self, visitor, instructions):
		return visitor.visit_negate(self, instructions)