from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IR_Expression, VisitorModel

class BinaryOperationEnum(Enum):
    MINUS = "MINUS"
    ADD = "ADD"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULUS = "MODULUS"
    BITWISE_AND = "BITWISE_AND"
    BITWISE_OR = "BITWISE_OR"
    BITWISE_XOR = "BITWISE_XOR"
    SHIFT_LEFT = "SHIFT_LEFT"
    SHIFT_RIGHT = "SHIFT_RIGHT"
    
class BinaryInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        pass

class AddInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_add_instruction(self, instructions)

class SubInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_sub_instruction(self, instructions)

class MulInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_mul_instruction(self, instructions)

class DivInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_div_mod_instruction(self, instructions)

class ModInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_div_mod_instruction(self, instructions)

class BitwiseAndInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_bitwise_and_instruction(self, instructions)

class BitwiseOrInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_bitwise_or_instruction(self, instructions)
    
class BitwiseXorInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_bitwise_xor_instruction(self, instructions)
    
class BitwiseLeftShiftInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_bitwise_left_shift_instruction(self, instructions)
    
class BitwiseRightShiftInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_bitwise_right_shift_instruction(self, instructions)
    
