from modules.models.AstNodes import AstNode
from pydantic import BaseModel

class FunctionDefinitionNode(AstNode):
	name: str
	body: AstNode
