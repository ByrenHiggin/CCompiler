from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, Operand, VisitorModel

class Stack(Operand):
	offset: int
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return self