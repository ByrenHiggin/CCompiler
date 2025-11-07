
from typing import List
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.BaseNode import BaseNode
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn
from modules.parser.StackAllocator import StackAllocator


class ASTLowerer:
    def __init__(self, allocator: StackAllocator):
        self.allocator = allocator

    def visit_negate(self, node: Negate, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        instructions.append(IRMoveValue(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=temp))
        return temp
    
    def visit_bitwise_not(self, node: BitwiseNot, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        instructions.append(IRMoveValue(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NOT, operand=temp))
        return temp
    
    def visit_constant_integer(self, node, instructions: List[BaseNode]):
        # For constants, just return the constant value
        return Immediate(value=node.value)
    
    def visit_return_statement(self, node: BaseNode, instructions: List[BaseNode]):
        # Handle return statement
        return_value: BaseNode = node.returnValue.accept(self, instructions)
        instructions.append(IRMoveValue(src=return_value, dest=Register(value=RegisterEnum.EAX)))
        instructions.append(IRreturn(value=Register(value=RegisterEnum.EAX)))  # Placeholder for stack cleanup
        return return_value
    
    def visit_function_definition(self, node: FunctionDefinitionNode, instructions: List[BaseNode]):
        # Handle function definition
        return node.body.accept(self, instructions)
    
    def visit_ir_return(self, node: IRreturn, instructions: List[BaseNode]):
        instructions.append(node)
        return node