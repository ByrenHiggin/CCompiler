from abc import abstractmethod
from typing import Any, List
from pydantic import BaseModel
from typing_extensions import Self 

class VisitorModel:
    pass

class BaseNode(BaseModel):
    @abstractmethod
    def accept(self, visitor: Any, instructions:List[Any]) -> Self:
        """Accept a visitor - this is the key to the visitor pattern"""
        pass
    
class IRNode(BaseNode):
    pass

class IR_Expression(IRNode):
    pass

class Operand(IR_Expression):
    pass
