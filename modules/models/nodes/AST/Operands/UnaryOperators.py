
from typing import Any, List
from modules.models.nodes.AST.Operands.ExpressionNode import UnaryNode
from modules.models.nodes.BaseNode import BaseNode, VisitorModel

class BitwiseNot(UnaryNode):
	operand: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_not(self, instructions)

class LogicalNot(UnaryNode):
	operand: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_logical_not(self, instructions)

class Negate(UnaryNode):
	operand: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_negate(self, instructions)