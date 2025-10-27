from modules.models.AstNodes.BaseNode import BaseNode

class Stack(BaseNode):
	offset: int
	def toAsm(self) -> str:
		return f"-{self.offset}(%rbp)"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self