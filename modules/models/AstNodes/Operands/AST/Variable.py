import random
import string

from modules.models.AstNodes import BaseNode
from modules.models.AstNodes.Operands.TACKY.Pesudo import Pseudo

class Variable(BaseNode):
	name: str
	def __init__(self, name: str | None = None):
		if name is not None:
			super().__init__(name=name) # type: ignore
		else:
			super().__init__(name="tmp." + self.generate_random_string(8)) # type: ignore

	def toAsm(self) -> str:
		return self.name

	def generate_random_string(self, length: int):
		characters = string.ascii_letters + string.digits
		random_string = ''.join([random.choice(characters) for _ in range(length)])
		return random_string
	def toTacky(self, instructions: list[BaseNode]) -> BaseNode:
		return Pseudo(value=self.name)