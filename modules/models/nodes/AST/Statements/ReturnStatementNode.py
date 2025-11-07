from modules.models.nodes.BaseNode import BaseNode

class ReturnStatementNode(BaseNode):
    instructions: list[BaseNode] | None = None
    returnValue: BaseNode
    def accept(self, visitor, instructions):
        return visitor.visit_return_statement(self, instructions)