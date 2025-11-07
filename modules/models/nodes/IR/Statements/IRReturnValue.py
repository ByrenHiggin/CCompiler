from modules.models.nodes.BaseNode import IRNode, Operand


class IRreturn(IRNode):
    value: Operand

    def accept(self, visitor, instructions):
        return visitor.visit_ir_return(self, instructions)

