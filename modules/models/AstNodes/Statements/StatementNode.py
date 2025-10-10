from modules.models.AstNodes import AstNode
from pydantic import BaseModel

class StatementNode(AstNode):
	returnValue: AstNode
