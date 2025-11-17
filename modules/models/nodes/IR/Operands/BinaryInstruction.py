from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, BinaryInstruction, IR_Expression, VisitorModel

class BinaryOperationEnum(Enum):
    MINUS = "MINUS"
    ADD = "ADD"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULUS = "MODULUS"
    

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

# class LogicalAndInstruction(BinaryInstruction):
#     src: IR_Expression
#     dest: IR_Expression
#     def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
#         return visitor.visit_logical_and_instruction(self, instructions)
    
# class LogicalOrInstruction(BinaryInstruction):
#     src: IR_Expression
#     dest: IR_Expression
#     def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
#         return visitor.visit_logical_or_instruction(self, instructions)