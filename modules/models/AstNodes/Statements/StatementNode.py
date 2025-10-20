from modules.models.AstNodes.BaseNode import BaseNode

class StatementNode(BaseNode):
	returnValue: BaseNode
	def toAsm(self) -> str:
		return f"""movl	{self.returnValue.toAsm()}, %eax
	ret
"""