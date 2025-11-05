from enum import Enum
from modules.models.AstNodes.BaseNode import IR_Expression, IRNode, Operand

class UnaryOperationEnum(Enum):
	NEG = "NEG"
	NOT = "NOT"

class UnaryInstruction(IR_Expression):
	operator: UnaryOperationEnum
	operand: IR_Expression
	def accept(self, visitor, instructions):
		return visitor.visit_unary_instruction(self,instructions)
	def toAsm(self) -> str:
		op_map = {
			UnaryOperationEnum.NEG: "neg",
			UnaryOperationEnum.NOT: "not"
		}
		return f"{op_map[self.operator]} {self.operand.toAsm()}"