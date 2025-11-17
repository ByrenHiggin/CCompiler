
from typing import Any, List
from modules.models.nodes.AST.Operands.ExpressionNode import BinaryNode
from modules.models.nodes.BaseNode import BaseNode, VisitorModel


class BinaryMinus(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_binary_expression(self, instructions)

class BinaryAdd(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_binary_expression(self, instructions)

class BinaryMultiply(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_binary_expression(self, instructions)

class BinaryDivide(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_binary_expression(self, instructions)

class BinaryModulus(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_binary_expression(self, instructions)

class LogicalOr(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_logical_or(self, instructions)

class LogicalAnd(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_logical_and(self, instructions)
