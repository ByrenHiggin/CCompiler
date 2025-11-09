
from typing import List
from modules.models.nodes.BaseNode import IRNode, VisitorModel
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.Operands.BinaryInstruction import BinaryInstruction, BinaryOperationEnum
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction
from modules.models.nodes.IR.Operands.Pseudo import Pseudo
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn
from modules.parser.StackAllocator import StackAllocator


class ASTLegalizer(VisitorModel):
    def __init__(self, allocator: StackAllocator):
        self.allocator = allocator

    def visit_ir_move_value(self, node: IRMoveValue, instructions: List[IRNode]):
        src = self.allocator.resolve_pseudo(node.src) if isinstance(node.src, Pseudo) else node.src
        dest = self.allocator.resolve_pseudo(node.dest) if isinstance(node.dest, Pseudo) else node.dest
        
        if isinstance(src, Stack) and isinstance(dest, Stack):
            temp_reg = Register(value=RegisterEnum.R10)
            instructions.append(IRMoveValue(src=src, dest=temp_reg))
            instructions.append(IRMoveValue(src=temp_reg, dest=dest))
        else:
            instructions.append(IRMoveValue(src=src, dest=dest))
    
    def visit_unary_instruction(self, node: UnaryInstruction, instructions: List[IRNode]):
        if isinstance(node.operand, Pseudo):
            node.operand = self.allocator.resolve_pseudo(node.operand)
        instructions.append(node)
    
    def visit_ir_return(self, node: IRreturn, instructions: List[IRNode]):
        instructions.append(node)
        return node
    
    def visit_binary_instruction(self, node: BinaryInstruction, instructions: List[IRNode]):
        left = self.allocator.resolve_pseudo(node.left) if isinstance(node.left, Pseudo) else node.left
        right = self.allocator.resolve_pseudo(node.right) if isinstance(node.right, Pseudo) else node.right
        instructions.append(IRMoveValue(src=left, dest=Register(value=RegisterEnum.EAX)))
        match node.Operation:
            case BinaryOperationEnum.ADD:
                instructions.append(AddInstruction(operator=.UnaryOperationEnum.ADD, operand=right))
            case BinaryOperationEnum.SUB:
                instructions.append(SubInstruction(operator=UnaryInstruction.UnaryOperationEnum.SUB, operand=right))
            case BinaryOperationEnum.MUL:
                instructions.append(MulInstruction(operator=UnaryInstruction.UnaryOperationEnum.MUL, operand=right))
            case BinaryOperationEnum.DIV:
                instructions.append(DivInstruction(operator=UnaryInstruction.UnaryOperationEnum.DIV, operand=right))
            case BinaryOperationEnum.MOD:
                instructions.append(ModInstruction(operator=UnaryInstruction.UnaryOperationEnum.MOD, operand=right))
            case _:
                raise NotImplementedError(f"Binary operation {node.Operation} not implemented in ASTLegalizer")
        instructions.append(node)