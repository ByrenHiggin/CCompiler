from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel

class StatementNode(BaseNode):
	value: BaseNode

class ReturnStatementNode(StatementNode):
	instructions: list[BaseNode] | None = None
	def accept(self, visitor: VisitorModel, instructions:List[Any]) -> IRNode:
		return visitor.visit_return_statement(self, instructions)