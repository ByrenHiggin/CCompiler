from modules.models.AstNodes.BaseNode import IRNode


class IRFunctionDefinition(IRNode):
    name: str
    instructions: list[IRNode]
    offset: int = 0
    def accept(self, visitor, instructions):
        return visitor.visit_function_definition(self, instructions)