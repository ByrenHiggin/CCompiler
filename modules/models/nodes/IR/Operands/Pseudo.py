from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, Operand, VisitorModel

class Pseudo(Operand):
	value: str

	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_pseudo(self, instructions)