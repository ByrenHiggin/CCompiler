from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel

class IRJump(IRNode):
	label: str
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_jump(self, instructions)

class IRJumpIfZero(IRNode):
	src: BaseNode
	label: str
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_jump(self, instructions)

class IRJumpIfNotZero(IRNode):
	src: BaseNode
	label: str
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_jump(self, instructions)

class IRLabel(IRNode):
	name: str
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_label(self, instructions)