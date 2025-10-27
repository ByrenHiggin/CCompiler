
from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Expressions.ExpressionNode import UnaryNode
from modules.models.AstNodes.Expressions.Variable import Variable


class BitwiseNot(UnaryNode):
	value: BaseNode
	def toAsm(self) -> str:
		return f"~{self.value.toAsm()}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		src = self.value.toTacky(instructions)
		tempVariable = Variable()
		instructions.append(TackyUnary(
			operation=self,
			src=src,
			dest=tempVariable
		))
		return tempVariable

class Negate(UnaryNode):
	value: BaseNode
	def toAsm(self) -> str:
		return f"-{self.value.toAsm()}"
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		src = self.value.toTacky(instructions)
		tempVariable= Variable()
		instructions.append(TackyUnary(
			operation=self,
			src=src,
			dest=tempVariable
		))
		return tempVariable

class TackyUnary(BaseNode):
	operation: UnaryNode
	src: BaseNode
	dest: BaseNode
	def toAsm(self) -> str:
		if self.operation.__class__ == BitwiseNot:
			return f"Not {self.src.toAsm()} -> {self.dest.toAsm()}"
		elif self.operation.__class__ == Negate:
			return f"Neg {self.src.toAsm()} -> {self.dest.toAsm()}"
		return f"{self.operation.toAsm()} {self.src.toAsm()} -> {self.dest.toAsm()}"