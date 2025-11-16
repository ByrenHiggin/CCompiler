
from typing import List
from modules.models.nodes.AST.Operands.BinaryOperators import *
from modules.models.nodes.AST.Operands.ExpressionNode import BinaryNode
from modules.models.nodes.AST.Statements.ReturnStatementNode import StatementNode
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, LogicalNot, Negate
from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel
from modules.models.nodes.IR.Operands.BinaryInstruction import *
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Statements.IRCopy import IRCopy
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn
from modules.IntermediateGenerator.visitors.StackAllocator import StackAllocator


class ASTLowerer(VisitorModel):
    allocator: StackAllocator
    def __init__(self, allocator: StackAllocator):
        self.allocator = allocator
        
    def __visit_divisor_or_modulo(self, node: BinaryNode, instructions: List[BaseNode], op: BinaryOperationEnum):
        dividend = node.left.accept(self, instructions)
        divisor = node.right.accept(self, instructions)
        
        src_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        src_pseudo = self.allocator.allocate_pseudo(src_name)
        
        dest_pseudo = f"reg.{RegisterEnum.EAX}"
        dest_pseudo = self.allocator.allocate_pseudo(dest_pseudo)
        
        instructions.append(IRCopy(src=divisor, dest=src_pseudo))
        instructions.append(IRCopy(src=dividend, dest=dest_pseudo))
        
        if(op == BinaryOperationEnum.MODULUS):
            target_pseudo = self.allocator.allocate_pseudo(f"reg.{RegisterEnum.EDX}")
            instructions.append(ModInstruction(src=src_pseudo, dest=dest_pseudo))
            instructions.append(IRCopy(src=target_pseudo, dest=dest_pseudo))
            return dest_pseudo
        else:
            instructions.append(DivInstruction(src=src_pseudo, dest=dest_pseudo))
            return dest_pseudo
    
    def __visit_add_sub_or_mult(self, node: BinaryNode, instructions: List[BaseNode], op: BinaryOperationEnum):
        left_result = node.left.accept(self, instructions)
        right_result = node.right.accept(self, instructions)
        src_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        dest_pseudo = self.allocator.allocate_pseudo(src_name)
        scratch_name = f"reg.{RegisterEnum.R11.name}"
        scratch_pseudo = self.allocator.allocate_pseudo(scratch_name)
        instructions.append(IRCopy(src=left_result, dest=scratch_pseudo))
        match op:
            case BinaryOperationEnum.ADD:
                instructions.append(AddInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.MINUS:
                instructions.append(SubInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.MULTIPLY:
                instructions.append(MulInstruction(src=scratch_pseudo, dest=right_result))
            case _:
                raise NotImplementedError(f"Operation {op} not implemented in __visit_add_sub_or_mult")                           
        instructions.append(IRCopy(src=scratch_pseudo, dest=dest_pseudo))
        return dest_pseudo
    
    def __visit_bitwise_and_or_xor(self, node: BinaryNode, instructions: List[BaseNode], op: BinaryOperationEnum):
        left_result = node.left.accept(self, instructions)
        right_result = node.right.accept(self, instructions)
        src_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        dest_pseudo = self.allocator.allocate_pseudo(src_name)
        scratch_name = f"reg.{RegisterEnum.R11.name}"
        scratch_pseudo = self.allocator.allocate_pseudo(scratch_name)
        instructions.append(IRCopy(src=left_result, dest=scratch_pseudo))
        match op:
            case BinaryOperationEnum.BITWISE_AND:
                instructions.append(BitwiseAndInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.BITWISE_OR:
                instructions.append(BitwiseOrInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.BITWISE_XOR:
                instructions.append(BitwiseXorInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.SHIFT_LEFT:
                instructions.append(BitwiseLeftShiftInstruction(src=scratch_pseudo, dest=right_result))
            case BinaryOperationEnum.SHIFT_RIGHT:
                instructions.append(BitwiseRightShiftInstruction(src=scratch_pseudo, dest=right_result))
            case _:
                raise NotImplementedError(f"Operation {op} not implemented in __visit_add_sub_or_mult")                           
        instructions.append(IRCopy(src=scratch_pseudo, dest=dest_pseudo))
        return dest_pseudo 
     
    def visit_binary_expression(self, node: BinaryNode, instructions: List[BaseNode]):
        if isinstance(node, BinaryMinus):
            return self.__visit_add_sub_or_mult(node, instructions,BinaryOperationEnum.MINUS)
        elif isinstance(node, BinaryAdd):
            return self.__visit_add_sub_or_mult(node, instructions,BinaryOperationEnum.ADD)
        elif isinstance(node, BinaryMultiply):  
            return self.__visit_add_sub_or_mult(node, instructions,BinaryOperationEnum.MULTIPLY)
        elif isinstance(node, BinaryDivide):
            return self.__visit_divisor_or_modulo(node, instructions,BinaryOperationEnum.DIVIDE)
        elif isinstance(node, BinaryModulus):
            return self.__visit_divisor_or_modulo(node, instructions,BinaryOperationEnum.MODULUS)
        elif isinstance(node, BitwiseAnd):
            return self.__visit_bitwise_and_or_xor(node, instructions,BinaryOperationEnum.BITWISE_AND)
        elif isinstance(node, BitwiseOr):
            return self.__visit_bitwise_and_or_xor(node, instructions,BinaryOperationEnum.BITWISE_OR)
        elif isinstance(node, BitwiseXor):
            return self.__visit_bitwise_and_or_xor(node, instructions,BinaryOperationEnum.BITWISE_XOR)
        elif isinstance(node, BitwiseLeftShift):
            return self.__visit_bitwise_and_or_xor(node, instructions,BinaryOperationEnum.SHIFT_LEFT)
        elif isinstance(node, BitwiseRightShift):
            return self.__visit_bitwise_and_or_xor(node, instructions,BinaryOperationEnum.SHIFT_RIGHT)
        else:
            raise NotImplementedError(f"Binary operation for {type(node)} not implemented in ASTLowerer")
        
    def visit_conditional_expression(self, node: BaseNode, instructions: List[BaseNode]):
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        if isinstance(node, EqualRelation):
            pass
        elif isinstance(node, NotEqualRelation):
            pass
        elif isinstance(node, LessThanRelation):
            pass
        elif isinstance(node, LessThanEqualRelation):
            pass
        elif isinstance(node, GreaterThanRelation):
            pass
        elif isinstance(node, GreaterThanEqualRelation):
            pass
        else:
            raise NotImplementedError(f"Conditional operation for {type(node)} not implemented in ASTLowerer")
        return temp 

    def visit_negate(self, node: Negate, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=temp))
        return temp
    
    def visit_logical_not(self, node: LogicalNot, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NOT, operand=temp))
        return temp
    
    def visit_bitwise_not(self, node: BitwiseNot, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.BITWISE_NOT, operand=temp))
        return temp
    
    def visit_constant_integer(self, node, instructions: List[BaseNode]):
        # For constants, just return the constant value
        return Immediate(value=node.value)
    
    def visit_return_statement(self, node:StatementNode, instructions: List[BaseNode]) -> BaseNode:
        # Handle return statement
        return_value: IRNode = node.value.accept(self, instructions)
        instructions.append(IRCopy(src=return_value, dest=Register(value=RegisterEnum.EAX)))
        instructions.append(IRreturn(value=Register(value=RegisterEnum.EAX)))
        return return_value
    
    def visit_function_definition(self, node: FunctionDefinitionNode, instructions: List[BaseNode])-> BaseNode:
        # Handle function definition
        return node.body.accept(self, instructions)
    
    def visit_ir_return(self, node: IRreturn, instructions: List[BaseNode]):
        instructions.append(node)
        return node