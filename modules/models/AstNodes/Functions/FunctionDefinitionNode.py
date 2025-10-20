from modules.models.AstNodes.BaseNode import BaseNode

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
	def toAsm(self) -> str:
		return f'''	.globl _{self.name}
_{self.name}:
	{self.body.toAsm()}
'''
