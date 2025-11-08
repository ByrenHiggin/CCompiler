from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, Operand, VisitorModel
from enum import Enum

class RegisterEnum(Enum):
	EAX = "EAX"
	R10 = "R10"

	def __str__(self) -> str:
		return self.value

class Register(Operand):
	value: RegisterEnum
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_register(self, instructions)
		