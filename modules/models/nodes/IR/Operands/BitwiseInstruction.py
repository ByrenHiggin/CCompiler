from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, BinaryInstruction, IR_Expression, VisitorModel

class BitwiseOperationEnum(Enum):
    BITWISE_AND = "BITWISE_AND"
    BITWISE_OR = "BITWISE_OR"
    BITWISE_XOR = "BITWISE_XOR"
    SHIFT_LEFT = "SHIFT_LEFT"
    SHIFT_RIGHT = "SHIFT_RIGHT"
    
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
    
