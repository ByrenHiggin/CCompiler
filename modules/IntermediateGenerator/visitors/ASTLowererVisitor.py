
from typing import List
from modules.models.enums.GenericRegisterEnum import GenericRegisterEnum
from modules.models.nodes.AST.Operands.BinaryOperators import *
from modules.models.nodes.AST.Operands.BitwiseOperators import *
from modules.models.nodes.AST.Operands.RelationalOperators import * 
from modules.models.nodes.AST.Operands.UnaryOperators import *

from modules.models.nodes.AST.Operands.ExpressionNode import BinaryNode
from modules.models.nodes.AST.Statements.ReturnStatementNode import StatementNode
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode

from modules.models.nodes.BaseNode import BaseNode, IRNode, VisitorModel

from modules.models.nodes.IR.Operands.RelationalInstruction import *
from modules.models.nodes.IR.Operands.UnaryInstruction import *
from modules.models.nodes.IR.Operands.BinaryInstruction import *
from modules.models.nodes.IR.Operands.BitwiseInstruction import *

from modules.models.nodes.IR.Operands.Register import Register
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Statements.IRCopy import IRCopy
from modules.models.nodes.IR.Statements.IRJump import *
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn
from modules.IntermediateGenerator.visitors.StackAllocator import StackAllocator


class ASTLowerer(VisitorModel):
    allocator: StackAllocator
    def __init__(self, allocator: StackAllocator):
        self.allocator = allocator
       
    def __zero_out_ax(self, instructions: List[BaseNode]):
        instructions.append(IRCopy(src=Immediate(value="0"), dest=Register(value=GenericRegisterEnum.AX))) # Set EAX to 0
     
    def __visit_divisor_or_modulo(self, node: BinaryNode, instructions: List[BaseNode], op: BinaryOperationEnum):
        dividend = node.left.accept(self, instructions)
        divisor = node.right.accept(self, instructions)
        
        src_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        src_pseudo = self.allocator.allocate_pseudo(src_name)
        
        dest_pseudo = f"reg.{GenericRegisterEnum.AX}"
        dest_pseudo = self.allocator.allocate_pseudo(dest_pseudo)
        
        instructions.append(IRCopy(src=divisor, dest=src_pseudo))
        instructions.append(IRCopy(src=dividend, dest=dest_pseudo))
        
        if(op == BinaryOperationEnum.MODULUS):
            target_pseudo = self.allocator.allocate_pseudo(f"reg.{GenericRegisterEnum.DX}")
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
        scratch_name = f"reg.{GenericRegisterEnum.R11}"
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
    
    def __visit_bitwise_and_or_xor(self, node: BinaryNode, instructions: List[BaseNode], op: BitwiseOperationEnum):
        left_result = node.left.accept(self, instructions)
        right_result = node.right.accept(self, instructions)
        src_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        dest_pseudo = self.allocator.allocate_pseudo(src_name)
        scratch_name = f"reg.{GenericRegisterEnum.R11}"
        scratch_pseudo = self.allocator.allocate_pseudo(scratch_name)
        instructions.append(IRCopy(src=left_result, dest=scratch_pseudo))
        match op:
            case BitwiseOperationEnum.BITWISE_AND:
                instructions.append(BitwiseAndInstruction(src=scratch_pseudo, dest=right_result))
            case BitwiseOperationEnum.BITWISE_OR:
                instructions.append(BitwiseOrInstruction(src=scratch_pseudo, dest=right_result))
            case BitwiseOperationEnum.BITWISE_XOR:
                instructions.append(BitwiseXorInstruction(src=scratch_pseudo, dest=right_result))
            case BitwiseOperationEnum.SHIFT_LEFT:
                instructions.append(BitwiseLeftShiftInstruction(src=scratch_pseudo, dest=right_result))
            case BitwiseOperationEnum.SHIFT_RIGHT:
                instructions.append(BitwiseRightShiftInstruction(src=scratch_pseudo, dest=right_result))
            case _:
                raise NotImplementedError(f"Operation {op} not implemented in __visit_add_sub_or_mult")                           
        instructions.append(IRCopy(src=scratch_pseudo, dest=dest_pseudo))
        return dest_pseudo
    
    def visit_logical_or(self, node: BinaryNode, instructions: List[BaseNode]):
        left_result = node.left.accept(self, instructions)
        right_result = node.right.accept(self, instructions)
        dest_pseudo = self.__allocate_temp()
        scratch_name = f"reg.{GenericRegisterEnum.R11}"
        scratch_pseudo = self.allocator.allocate_pseudo(scratch_name)
        false_label = IRLabel(name=f"lbl.false.{self.allocator.temp_counter}")
        end_label = IRLabel(name=f"lbl.end.{self.allocator.temp_counter}")
        
        instructions.append(IRCopy(src=left_result, dest=scratch_pseudo))
        instructions.append(IRJumpIfNotZero(src=scratch_pseudo, label=false_label.name))
        instructions.append(IRCopy(src=right_result, dest=scratch_pseudo))
        instructions.append(IRJumpIfNotZero(src=scratch_pseudo, label=false_label.name))
        instructions.append(IRCopy(src=Immediate(value="0"), dest=dest_pseudo))
        instructions.append(IRJump(label=end_label.name))
        instructions.append(false_label)
        instructions.append(IRCopy(src=Immediate(value="1"), dest=dest_pseudo))
        instructions.append(end_label)
        return dest_pseudo
    
    def visit_logical_and(self, node: BinaryNode, instructions: List[BaseNode]):
        left_result = node.left.accept(self, instructions)
        right_result = node.right.accept(self, instructions)
        dest_pseudo = self.__allocate_temp()
        scratch_name = f"reg.{GenericRegisterEnum.R11}"
        scratch_pseudo = self.allocator.allocate_pseudo(scratch_name)
        false_label = IRLabel(name=f"lbl.false.{self.allocator.temp_counter}")
        end_label = IRLabel(name=f"lbl.end.{self.allocator.temp_counter}")
        
        instructions.append(IRCopy(src=left_result, dest=scratch_pseudo))
        instructions.append(IRJumpIfZero(src=scratch_pseudo, label=false_label.name))
        instructions.append(IRCopy(src=right_result, dest=scratch_pseudo))
        instructions.append(IRJumpIfZero(src=scratch_pseudo, label=false_label.name))
        instructions.append(IRCopy(src=Immediate(value="1"), dest=dest_pseudo))
        instructions.append(IRJump(label=end_label.name))
        instructions.append(false_label)
        instructions.append(IRCopy(src=Immediate(value="0"), dest=dest_pseudo))
        instructions.append(end_label)
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
        else:
            raise NotImplementedError(f"Binary operation for {type(node)} not implemented in ASTLowerer")
    
    def visit_bitwise_expression(self, node: BinaryNode, instructions: List[BaseNode]):
        if isinstance(node, BitwiseAnd):
            return self.__visit_bitwise_and_or_xor(node, instructions,BitwiseOperationEnum.BITWISE_AND)
        elif isinstance(node, BitwiseOr):
            return self.__visit_bitwise_and_or_xor(node, instructions,BitwiseOperationEnum.BITWISE_OR)
        elif isinstance(node, BitwiseXor):
            return self.__visit_bitwise_and_or_xor(node, instructions,BitwiseOperationEnum.BITWISE_XOR)
        elif isinstance(node, BitwiseLeftShift):
            return self.__visit_bitwise_and_or_xor(node, instructions,BitwiseOperationEnum.SHIFT_LEFT)
        elif isinstance(node, BitwiseRightShift):
            return self.__visit_bitwise_and_or_xor(node, instructions,BitwiseOperationEnum.SHIFT_RIGHT)
        else:
            raise NotImplementedError(f"Binary operation for {type(node)} not implemented in ASTLowerer")
        
    def visit_conditional_expression(self, node: BaseNode, instructions: List[BaseNode]):
        #clears and writes to the AL register
        src = node.left.accept(self, instructions)
        dest = node.right.accept(self, instructions)
        temp = self.allocator.allocate_pseudo(f"reg.{GenericRegisterEnum.R10}")
        self.__zero_out_ax(instructions)
        instructions.append(IRCopy(src=src, dest=temp))
        if isinstance(node, EqualRelation):
            instructions.append(EqualRelationInstruction(src=temp, dest=dest))
        elif isinstance(node, NotEqualRelation):
            instructions.append(NotEqualRelationInstruction(src=temp, dest=dest))
        elif isinstance(node, LessThanRelation):
            instructions.append(LessThanRelationInstruction(src=temp, dest=dest))
        elif isinstance(node, LessThanEqualRelation):
            instructions.append(LessThanEqualRelationInstruction(src=temp, dest=dest))
        elif isinstance(node, GreaterThanRelation):
            instructions.append(GreaterThanRelationInstruction(src=temp, dest=dest))
        elif isinstance(node, GreaterThanEqualRelation):
            instructions.append(GreaterThanEqualRelationInstruction(src=temp, dest=dest))
        else:
            raise NotImplementedError(f"Conditional operation for {type(node)} not implemented in ASTLowerer")
        instructions.append(IRCopy(src=Register(value=GenericRegisterEnum.AX), dest=temp)) 
        return temp
    
    def __allocate_temp(self) -> Register:
        temp_name = f"tmp.{self.allocator.temp_counter}"
        self.allocator.temp_counter += 1
        temp = self.allocator.allocate_pseudo(temp_name)
        return temp

    def visit_negate(self, node: Negate, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp = self.__allocate_temp() 
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=temp))
        return temp
    
    def visit_logical_not(self, node: LogicalNot, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp = self.__allocate_temp() 
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.NOT, operand=temp))
        return temp
    
    def visit_bitwise_not(self, node: BitwiseNot, instructions: List[BaseNode]):
        operand_result = node.operand.accept(self, instructions)
        temp = self.__allocate_temp() 
        instructions.append(IRCopy(src=operand_result, dest=temp))
        instructions.append(UnaryInstruction(operator=UnaryOperationEnum.BITWISE_NOT, operand=temp))
        return temp
    
    def visit_constant_integer(self, node, instructions: List[BaseNode]):
        # For constants, just return the constant value
        return Immediate(value=node.value)
    
    def visit_return_statement(self, node:StatementNode, instructions: List[BaseNode]) -> BaseNode:
        # Handle return statement
        return_value: IRNode = node.value.accept(self, instructions)
        instructions.append(IRCopy(src=return_value, dest=Register(value=GenericRegisterEnum.AX)))
        instructions.append(IRreturn(value=Register(value=GenericRegisterEnum.AX)))
        return return_value
    
    def visit_function_definition(self, node: FunctionDefinitionNode, instructions: List[BaseNode])-> BaseNode:
        # Handle function definition
        return node.body.accept(self, instructions)
    
    def visit_ir_return(self, node: IRreturn, instructions: List[BaseNode]):
        instructions.append(node)
        return node