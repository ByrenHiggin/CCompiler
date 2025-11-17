from enum import Enum
from typing import Any, List
from modules.models.nodes.BaseNode import BaseNode, BinaryInstruction, IR_Expression, VisitorModel
    
class EqualRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)

class NotEqualRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)
    
class LessThanRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)
    
class LessThanEqualRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)
    
class GreaterThanRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)
    
class GreaterThanEqualRelationInstruction(BinaryInstruction):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        return visitor.visit_relational_instruction(self, instructions)