from typing import List
from pydantic import BaseModel

class BaseNode(BaseModel):
	def toAsm(self) -> str:
		return ";; Assembly code placeholder for BaseNode\n"
	pass

class ProgramNode(BaseModel):
	functions: List[BaseNode]
	def toAsm(self) -> str:
		asm = ""
		for func in self.functions:
			asm += func.toAsm()
		return asm