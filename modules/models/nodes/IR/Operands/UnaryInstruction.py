from enum import Enum
from modules.models.nodes.BaseNode import IR_Expression, IRNode, Operand

class UnaryOperationEnum(Enum):
	NEG = "NEG"
	NOT = "NOT"

class UnaryInstruction(IR_Expression):
	operator: UnaryOperationEnum
	operand: IR_Expression
	def accept(self, visitor, instructions):
		return visitor.visit_unary_instruction(self,instructions)
