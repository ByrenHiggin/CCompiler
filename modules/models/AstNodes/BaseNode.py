from typing import List
from pydantic import BaseModel

class BaseNode(BaseModel):
	def toAsm(self) -> str:
		return ";; Assembly code placeholder for BaseNode\n"
	pass
	def toTacky(self, instructions: list["BaseNode"]) -> "BaseNode": # type: ignore
		return self


class ProgramNode(BaseModel):
	functions: List[BaseNode]
	def toAsm(self) -> str:
		asm = ""
		for func in self.functions:
			asm += func.toAsm()
		return asm
	def toTacky(self) -> "ProgramNode":
		instructions: list[BaseNode] = []
		results: list[BaseNode] = []
		for func in self.functions:
			results.append(func.toTacky(instructions))
		return ProgramNode(functions=results)