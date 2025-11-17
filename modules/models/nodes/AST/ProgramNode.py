from typing import Any, List

from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.BaseNode import BaseNode

class ProgramNode(BaseNode):
	functions: List[FunctionDefinitionNode]
	def accept(self, visitor: Any, instructions:List[Any]) -> BaseNode:
		pass