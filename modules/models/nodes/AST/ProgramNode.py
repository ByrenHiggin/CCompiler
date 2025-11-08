from typing import List
from pydantic import BaseModel

from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode

class ProgramNode(BaseModel):
	functions: List[FunctionDefinitionNode]