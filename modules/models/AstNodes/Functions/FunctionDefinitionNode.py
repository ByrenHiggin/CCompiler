from modules.models.AstNodes.BaseNode import BaseNode

class FunctionDefinitionNode(BaseNode):
	name: str
	body: BaseNode
	def toAsm(self) -> str:
		raise NotImplementedError("toAsm method must be implemented by subclasses")

	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		results: list[BaseNode] = []
		body = self.body.toTacky(results)
		return TackyFunctionDefinitionNode(
			name=self.name,
			body=body,
			FunctionDefinitionPrologueNode=FunctionDefinitionPrologueNode(),
			FunctionDefinitionEpilogueNode=FunctionDefinitionEpilogueNode()
		)
  
class FunctionDefinitionPrologueNode(BaseNode):
	def toAsm(self) -> str:
		lines: list[str] = []
		lines.append(f'\tpushq %rbp')
		lines.append(f'\tmovq %rsp, %rbp')
		lines.append(f'\tsubq $8, %rsp')
		return "\n".join(lines)

	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self

class FunctionDefinitionEpilogueNode(BaseNode):
	def toAsm(self) -> str:
		lines: list[str] = []
		lines.append(f'\n\tmovq %rbp, %rsp')
		lines.append(f'\tpopq %rbp')
		lines.append(f'\tret')
		return "\n".join(lines)

	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self

class TackyFunctionDefinitionNode(FunctionDefinitionNode):
	FunctionDefinitionPrologueNode: FunctionDefinitionPrologueNode
	FunctionDefinitionEpilogueNode: FunctionDefinitionEpilogueNode
	def toAsm(self) -> str:
		lines: list[str] = []
		lines.append('\n\t.globl ' + self.name)
		lines.append(f'{self.name}:')
		lines.append(f'\t{self.FunctionDefinitionPrologueNode.toAsm()}')
		lines.append(f'\t{self.body.toAsm()}')
		lines.append(f'\t{self.FunctionDefinitionEpilogueNode.toAsm()}')
		return "\n".join(lines)

	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return self 