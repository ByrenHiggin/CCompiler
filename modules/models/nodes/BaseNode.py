from typing import Any, List
from pydantic import BaseModel
from typing_extensions import Self 

class VisitorModel:
    pass

class BaseNode(BaseModel):
    def accept(self, visitor: VisitorModel, instructions: List[Any]) -> Self:
        raise NotImplementedError(f"No visitor method {self.__class__.__name__.lower()}")
    
class IRNode(BaseNode):
    pass

class IR_Expression(IRNode):
    pass

class Operand(IR_Expression):
    pass

class BinaryInstruction(IR_Expression):
    src: IR_Expression
    dest: IR_Expression
    def accept(self, visitor: VisitorModel, instructions:List[Any]) -> BaseNode:
        pass