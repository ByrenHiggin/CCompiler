from modules.models.AstNodes.BaseNode import Operand
from enum import Enum

class RegisterEnum(Enum):
	EAX = "EAX"
	R10 = "R10"

	def __str__(self) -> str:
		return self.value

class Register(Operand):
	value: RegisterEnum
	def accept(self, visitor, instructions):
		return visitor.visit_register(self, instructions)
		