from modules.models.AstNodes.BaseNode import Operand

class Pseudo(Operand):
	value: str
	def accept(self, visitor, instructions):
		return visitor.visit_pseudo(self, instructions)