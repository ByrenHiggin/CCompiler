from modules.models.AstNodes.BaseNode import Operand

class Immediate(Operand):
	value: str
	def accept(self, visitor, instructions):
		return visitor.visit_immediate(self, instructions)
	def toAsm(self) -> str:
		return f"${self.value}"