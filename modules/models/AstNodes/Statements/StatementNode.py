from modules.models.AstNodes.BaseNode import BaseNode

class StatementNode(BaseNode):
	returnValue: BaseNode
	def toAsm(self) -> str:
		return f"""mov	{self.returnValue.toAsm()}, %eax
	ret
"""