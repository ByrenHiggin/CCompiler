from modules.models.enums.GenericRegisterEnum import GenericRegisterEnum
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel
from modules.models.nodes.IR.IRProgramNode import IRFunctionDefinition
from modules.models.nodes.IR.Operands.Register import Register
from modules.models.nodes.IR.Operands.BinaryInstruction import BinaryInstruction
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Operands.RelationalInstruction import *
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Statements.IRCopy import IRCopy
from modules.models.nodes.IR.Statements.IRJump import *
from modules.codeGenerator.Registers import x86_64_Registers

class x86_64_AssemblyVisitor(VisitorModel):
    
    lines: list[str]
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.REGISTER_MAP = x86_64_Registers.map
        
    def _operand_to_asm(self, operand: BaseNode) -> str:
        if isinstance(operand, Register):
            reg = self.REGISTER_MAP[operand.value]
            return reg.as_4_bit
        elif isinstance(operand, GenericRegisterEnum):
            reg = self.REGISTER_MAP[operand]
            return reg.as_4_bit
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
            UnaryOperationEnum.BITWISE_NOT: "notl",
            UnaryOperationEnum.NOT: "notl"  #TODO: Actually implement logic
        }
        operand = self._operand_to_asm(node.operand)
        instructions.append(f"\t{op_map[node.operator]} {operand}\n")
        return node
    
    def visit_ir_copy(self, node: IRCopy, instructions: list[str]) -> IRNode:
        src = self._operand_to_asm(node.src)
        dest = self._operand_to_asm(node.dest)
        instructions.append(f"\tmovl {src}, {dest}\n")
        return node
    
    def visit_ir_return(self, node: IRNode, instructions: list[str]) -> IRNode:
        instructions.append(f"\tmovq %rbp, %rsp\n")
        instructions.append(f"\tpopq %rbp\n")
        instructions.append("\tret\n")
        return node

    def __handle_binary_instruction(self, node: BinaryInstruction, instructions: list[str], asm_op: str) -> IRNode:
        src = self._operand_to_asm(node.src)
        dest = self._operand_to_asm(node.dest)
        instructions.append(f"\t{asm_op} {dest}, {src}\n")
        return node
    
    def visit_mul_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "imull")
    
    def visit_sub_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "subl")
    
    def visit_add_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "addl")
    
    def visit_div_mod_instruction(self, node: BinaryInstruction, instructions: list[str])->IRNode:
        src = self._operand_to_asm(node.src)
        instructions.append(f"\tcdq\n")
        instructions.append(f"\tidivl {src}\n")
        return node
    
    def visit_bitwise_and_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "andl")
    
    def visit_bitwise_or_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "orl")
    
    def visit_bitwise_xor_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "xorl")
    
    def visit_bitwise_left_shift_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "shll")
    
    def visit_bitwise_right_shift_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "shrl")

    def visit_logical_and_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "andl")
    
    def visit_logical_or_instruction(self, node: BinaryInstruction, instructions: list[str]) -> IRNode:
        return self.__handle_binary_instruction(node, instructions, "orl")
    
    def visit_ir_jump(self, node: IRNode, instructions: list[str]) -> IRNode:
        if isinstance(node, IRJump):
            instructions.append(f"\tjmp {node.label}\n")
        elif isinstance(node, IRJumpIfZero):
            src = self._operand_to_asm(node.src)
            instructions.append(f"\tcmpl $0, {src}\n")
            instructions.append(f"\tje {node.label}\n")
        elif isinstance(node, IRJumpIfNotZero):
            src = self._operand_to_asm(node.src)
            instructions.append(f"\tcmpl $0, {src}\n")
            instructions.append(f"\tjne {node.label}\n")
        return node
    
    def visit_ir_label(self, node: IRNode, instructions: List[str]):
        instructions.append(f"{node.name}:\n")
        return node
    
    def visit_relational_instruction(self, node: BinaryInstruction, instructions: List[str]):
        src = self._operand_to_asm(node.src)
        dest = self._operand_to_asm(node.dest)
        intermediate = self.REGISTER_MAP[GenericRegisterEnum.AX].as_1_bit
        instructions.append(f"\tcmpl {dest}, {src}\n")
        if isinstance(node, EqualRelationInstruction):
            instructions.append(f"\tsete {intermediate}\n")
        elif isinstance(node, NotEqualRelationInstruction):
            instructions.append(f"\tsetne {intermediate}\n")
        elif isinstance(node, LessThanRelationInstruction):
            instructions.append(f"\tsetl {intermediate}\n")
        elif isinstance(node, LessThanEqualRelationInstruction):
            instructions.append(f"\tsetle {intermediate}\n")
        elif isinstance(node, GreaterThanRelationInstruction):
            instructions.append(f"\tsetg {intermediate}\n")
        elif isinstance(node, GreaterThanEqualRelationInstruction):
            instructions.append(f"\tsetge {intermediate}\n")
        return node