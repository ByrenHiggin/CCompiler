from modules.models.AstNodes.BaseNode import BaseNode

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
	def toAsm(self) -> str:
		return f'''	.globl {self.name}
{self.name}:
	{self.body.toAsm()}
'''
