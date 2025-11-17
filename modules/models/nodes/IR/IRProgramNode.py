from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel 
from modules.models.nodes.IR.Functions.IRFunctionDefinition import IRFunctionDefinition
 
class IRProgramNode(IRNode):
	functions: list[IRFunctionDefinition]
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
		return visitor.visit_ir_program_node(self, instructions)



	
