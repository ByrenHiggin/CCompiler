from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.IRProgramNode import IRFunctionDefinition
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum

class x86_64_AssemblyVisitor(VisitorModel):
    lines: list[str]
    def __init__(self) -> None:
        self.lines: list[str] = []
        
    def _operand_to_asm(self, operand: BaseNode) -> str:
        if isinstance(operand, Register):
            reg_map = {
                RegisterEnum.EAX: "%eax",
                RegisterEnum.R10: "%r10d"
            }
            return reg_map[operand.value]
        elif isinstance(operand, Stack):
            return f"{operand.offset}(%rbp)"
        elif isinstance(operand, Immediate):
            return f"${operand.value}"
        else:
            raise ValueError(f"Unknown operand type: {type(operand)}")

    def visit_function_definition(self, node: IRFunctionDefinition, instructions: list[str]) -> IRNode:
        instructions.append(f".globl _{node.name}\n")
        instructions.append(f"_{node.name}:\n")
        instructions.append(f"\tpushq %rbp\n")
        instructions.append(f"\tmovq %rsp, %rbp\n")
        instructions.append(f"\tsubq ${node.offset}, %rsp\n")
        for instr in node.instructions:
            instr.accept(self, instructions)
        return node
    
    def visit_unary_instruction(self, node:UnaryInstruction, instructions: list[str]) -> IRNode:
        op_map = {
            UnaryOperationEnum.NEG: "negl",
            UnaryOperationEnum.NOT: "notl"
        }
        operand = self._operand_to_asm(node.operand)
        instructions.append(f"\t{op_map[node.operator]} {operand}\n")
        return node
    
    def visit_ir_move_value(self, node: IRMoveValue, instructions: list[str]) -> IRNode:
        src = self._operand_to_asm(node.src)
        dest = self._operand_to_asm(node.dest)
        instructions.append(f"\tmovl {src}, {dest}\n")
        return node
    
    def visit_ir_return(self, node: IRNode, instructions: list[str]) -> IRNode:
        instructions.append(f"\tmovq %rbp, %rsp\n")
        instructions.append(f"\tpopq %rbp\n")
        instructions.append("\tret\n")
        return node

