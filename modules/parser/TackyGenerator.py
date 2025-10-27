from modules.models.AstNodes.BaseNode import BaseNode, Operand
from modules.models.AstNodes.Functions.FunctionDefinitionNode import FunctionDefinitionNode
from modules.models.AstNodes.Operands.AST.UnaryOperators import BitwiseNot, Negate
from modules.models.AstNodes.Operands.IR.Register import Register, RegisterEnum
from modules.models.AstNodes.Operands.IR.Immediate import Immediate
from modules.models.AstNodes.Operands.IR.Pesudo import Pseudo
from modules.models.AstNodes.Operands.IR.Stack import Stack
from modules.models.AstNodes.Operands.IR.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.AstNodes.ProgramNode import ProgramNode
from modules.parser.InstructionBuilder import IRFunctionDefinition, IRFunctionDefinition, IRMoveValue, IRProgramNode, IRreturn


class TackyGenerator:
    def __init__(self):
        self.first_pass_instructions: list[BaseNode] = []
        self.second_pass_instructions: list[BaseNode] = []
        self.third_pass_instructions: list[BaseNode] = []
        self.temp_counter = 0
        self.stack_offset = 0
        self.register_map: dict[str, int] = {
        }
        
    def generate_pseudo(self, value: str, offset:int) -> Pseudo:
        self.stack_offset += offset
        pseudo = Pseudo(value=value, offset=self.stack_offset)
        self.register_map[value] = self.stack_offset
        self.temp_counter += 1
        return pseudo

    def visit_pseudo(self, node: Pseudo):
        return node

    def visit_bitwise_not(self, node: BitwiseNot, instructions):
        operand_result = node.operand.accept(self, instructions)
        temp = self.generate_pseudo(value=f"tmp.{self.temp_counter}", offset=-4)
        instructions.append(IRMoveValue(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NOT, operand=temp))
        return temp

    def visit_negate(self, node: Negate, instructions):
        operand_result = node.operand.accept(self, instructions)
        temp = self.generate_pseudo(value=f"tmp.{self.temp_counter}", offset=-4)
        instructions.append(IRMoveValue(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=temp))
        return temp

    def visit_unary_instruction(self, node: UnaryInstruction, instructions):
        if isinstance(node.operand, Pseudo):
            node.operand = Stack(offset=self.register_map[node.operand.value])
        instructions.append(node)
        return node
    
    def visit_constant_integer(self, node, instructions):
        # For constants, just return the constant value
        return Immediate(value=node.value)
    
    def visit_ir_return(self, node: IRreturn, instructions):
        instructions.append(node)
        return node

    def visit_return_statement(self, node: BaseNode, instructions):
        # Handle return statement
        return_value = node.returnValue.accept(self, instructions)
        instructions.append(IRMoveValue(src=return_value, dest=Register(value=RegisterEnum.EAX)))
        instructions.append(IRreturn(value=Register(value=RegisterEnum.EAX)))  # Placeholder for stack cleanup
        return return_value

    def visit_ir_move_value(self, node: IRMoveValue, instructions):
        if isinstance(node.src, Pseudo) and isinstance(node.dest, Pseudo):
            instructions.append(IRMoveValue(src=node.src, dest=Register(value=RegisterEnum.R10)))
            instructions.append(IRMoveValue(src=Register(value=RegisterEnum.R10), dest=node.dest))
        else:
            instructions.append(node)
        if isinstance(node.src, Pseudo):
            node.src = Stack(offset=self.register_map[node.src.value])
        if isinstance(node.dest, Pseudo):
            node.dest = Stack(offset=self.register_map[node.dest.value])

    def visit_function_definition(self, node: FunctionDefinitionNode, instructions):
        # Handle function definition
        return node.body.accept(self, instructions)

    def parse_ast(self, node: ProgramNode) -> IRProgramNode:
        functions: list[IRFunctionDefinition] = []
        for func in node.functions:
            func.accept(self, instructions=self.first_pass_instructions)
            for instr in self.first_pass_instructions:
                instr.accept(self, instructions=self.second_pass_instructions)
            for instr in self.second_pass_instructions:
                instr.accept(self, instructions=self.third_pass_instructions)
            functions.append(
                IRFunctionDefinition(
                    name=func.name,
                    offset=abs(self.stack_offset),
                    instructions=self.third_pass_instructions
                )
            )
        return IRProgramNode(functions=functions)