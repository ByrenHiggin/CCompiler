from typing import List
from pydantic import BaseModel

from modules.models.AstNodes.BaseNode import BaseNode

class ProgramNode(BaseModel):
	functions: List[BaseNode]