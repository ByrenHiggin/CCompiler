from typing import List
from modules.models.nodes.BaseNode import BaseNode, VisitorModel

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
 
	def accept(self, visitor: VisitorModel, instructions: List[BaseNode])->BaseNode:
		return visitor.visit_function_definition(self, instructions)