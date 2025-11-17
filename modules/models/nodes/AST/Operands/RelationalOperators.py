
from typing import Any, List
from modules.models.nodes.AST.Operands.ExpressionNode import BinaryNode
from modules.models.nodes.BaseNode import BaseNode, VisitorModel

class EqualRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)

class NotEqualRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)

class LessThanRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)

class LessThanEqualRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)

class GreaterThanRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)

class GreaterThanEqualRelation(BinaryNode):
	left: BaseNode
	right: BaseNode
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_conditional_expression(self, instructions)