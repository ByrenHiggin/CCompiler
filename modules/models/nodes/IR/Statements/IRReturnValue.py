from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, Operand, VisitorModel


class IRreturn(IRNode):
	value: Operand

	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_return(self, instructions)

