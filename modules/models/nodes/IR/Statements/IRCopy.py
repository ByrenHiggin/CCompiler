from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel

class IRCopy(IRNode):
	src: BaseNode 
	dest: BaseNode

	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_copy(self, instructions)
