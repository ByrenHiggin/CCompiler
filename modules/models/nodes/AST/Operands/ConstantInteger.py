from typing import Any, List
from modules.models.nodes.AST.Operands.ExpressionNode import ExpressionNode
from modules.models.nodes.BaseNode import BaseNode, Operand, VisitorModel

class ConstantInteger(ExpressionNode):
	value: str
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_constant_integer(self, instructions)