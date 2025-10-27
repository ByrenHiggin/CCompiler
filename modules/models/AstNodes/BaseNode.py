from pydantic import BaseModel


class BaseNode(BaseModel):
	def toAsm(self) -> str:
		return ";; Assembly code placeholder for BaseNode\n"
	pass
	def toTacky(self, instructions: list["BaseNode"]) -> "BaseNode": # type: ignore
		return self