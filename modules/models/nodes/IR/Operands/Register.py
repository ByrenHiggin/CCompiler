from typing import Any, List
from modules.models.enums.GenericRegisterEnum import GenericRegisterEnum
from modules.models.nodes.BaseNode import BaseNode, Operand, VisitorModel


class Register(Operand):
	value: GenericRegisterEnum
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_register(self, instructions)
		