from modules.models.AstNodes.BaseNode import BaseNode
from enum import Enum

class RegisterEnum(Enum):
	AX = "AX"
	R10 = "R10"

	def __str__(self) -> str:
		return self.value

class Register(BaseNode):
	value: RegisterEnum
	def toAsm(self) -> str:
		return f"${self.value.name}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self