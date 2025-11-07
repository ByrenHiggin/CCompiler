from modules.models.AstNodes.BaseNode import Operand

class Immediate(Operand):
	value: str
	def accept(self, visitor, instructions):
		return visitor.visit_immediate(self, instructions)