from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel

class IRMoveValue(IRNode):
	src: IRNode 
	dest: IRNode

	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_move_value(self, instructions)
