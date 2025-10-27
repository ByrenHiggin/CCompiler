from modules.models.AstNodes.BaseNode import BaseNode, Operand

class Stack(Operand):
	offset: int
	def toAsm(self) -> str:
		return f"{self.offset}(%rbp)"
	def accept(self, visitor, instructions):
		"""Accept a visitor - this is the key to the visitor pattern"""
		pass