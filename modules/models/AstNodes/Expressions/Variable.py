import random
import string

from modules.models.AstNodes import BaseNode

class Variable(BaseNode):
	name: str
	def __init__(self, name: str | None = None):
		if name is not None:
			super().__init__(name=name)
		else:
			super().__init__(name="tmp." + self.generate_random_string(8))


	def toAsm(self) -> str:
		return self.name

	def generate_random_string(self, length: int):
		characters = string.ascii_letters + string.digits
		random_string = ''.join([random.choice(characters) for _ in range(length)])
		return random_string