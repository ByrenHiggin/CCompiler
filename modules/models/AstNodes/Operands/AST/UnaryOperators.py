
from modules.models.AstNodes.BaseNode import BaseNode
from modules.models.AstNodes.Operands.ExpressionNode import UnaryNode
from modules.models.AstNodes.Operands.AST.Variable import Variable

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
		lines: list[str] = []
		lines.append(f"    movq {self.src.toAsm()}, %rax")