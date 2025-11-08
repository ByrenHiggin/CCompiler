from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel


class IRFunctionDefinition(IRNode):
	name: str
	instructions: list[IRNode]
	offset: int = 0
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_function_definition(self, instructions)