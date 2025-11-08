from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IR_Expression, VisitorModel

class UnaryOperationEnum(Enum):
	NEG = "NEG"
	NOT = "NOT"

class UnaryInstruction(IR_Expression):
	operator: UnaryOperationEnum
	operand: IR_Expression
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_unary_instruction(self,instructions)
