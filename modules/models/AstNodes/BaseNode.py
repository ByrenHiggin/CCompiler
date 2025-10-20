from typing import List
from pydantic import BaseModel

class BaseNode(BaseModel):
	pass

class ProgramNode(BaseModel):
	functions: List[BaseNode]