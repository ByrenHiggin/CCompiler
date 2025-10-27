from modules.models.AstNodes.BaseNode import BaseNode

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
 
	def accept(self, visitor, instructions):
		return visitor.visit_function_definition(self, instructions)