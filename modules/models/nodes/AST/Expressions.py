
from modules.models.nodes.BaseNode import BaseNode, VisitorModel


class ExpressionStatementNode(BaseNode):
    expression: BaseNode
    def accept(self, visitor: VisitorModel, instructions: list[BaseNode]) -> BaseNode:
        return visitor.visit_expression_statement(self, instructions)