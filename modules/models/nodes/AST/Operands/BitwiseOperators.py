
from typing import Any, List
from modules.models.nodes.AST.Operands.ExpressionNode import BinaryNode
from modules.models.nodes.BaseNode import BaseNode, VisitorModel


class BitwiseAnd(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_expression(self, instructions)

class BitwiseOr(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_expression(self, instructions)

class BitwiseXor(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_expression(self, instructions)

class BitwiseLeftShift(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_expression(self, instructions)

class BitwiseRightShift(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_bitwise_expression(self, instructions)