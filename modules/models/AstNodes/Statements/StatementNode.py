from modules.models.AstNodes.BaseNode import BaseNode

class ReturnStatementNode(BaseNode):
	instructions: list[BaseNode] | None = None
	returnValue: BaseNode
	def toAsm(self) -> str:
		# Assembly code generation for return statement
		lines: list[str] = []
		for instr in self.instructions or []:
			lines.append(instr.toAsm())
		lines.append(f"mov	{self.returnValue.toAsm()}, %eax")
		lines.append("ret")
		return "\n".join(lines)

	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		result: BaseNode = self.returnValue.toTacky(instructions)
		return ReturnStatementNode(
			instructions=instructions,
			returnValue=result
		)
  
