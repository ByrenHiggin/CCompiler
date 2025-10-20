from modules.models.AstNodes.BaseNode import BaseNode

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
