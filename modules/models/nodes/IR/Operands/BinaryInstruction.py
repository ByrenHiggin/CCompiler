from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, IR_Expression, VisitorModel

class BinaryOperationEnum(Enum):
    MINUS = "MINUS"
    ADD = "ADD"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULUS = "MODULUS"

class BinaryInstruction(IR_Expression):
    left: IR_Expression 
    right: IR_Expression
    Operation: BinaryOperationEnum
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_binary_instruction(self, instructions)

class AddInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_add_instruction(self, instructions)

class SubInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_sub_instruction(self, instructions)

class MulInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_mul_instruction(self, instructions)

class DivInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_div_mod_instruction(self, instructions)

class ModInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_div_mod_instruction(self, instructions)