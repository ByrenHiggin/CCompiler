from modules.models.AstNodes.BaseNode import BaseNode, Operand

class Stack(Operand):
	offset: int
	def accept(self, visitor, instructions):
		"""Accept a visitor - this is the key to the visitor pattern"""
		pass