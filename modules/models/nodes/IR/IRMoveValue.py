from modules.models.AstNodes.BaseNode import IRNode, Operand

class IRMoveValue(IRNode):
    src: Operand
    dest: Operand

    def accept(self, visitor, instructions):
        return visitor.visit_ir_move_value(self, instructions)
