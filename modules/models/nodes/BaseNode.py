from abc import abstractmethod
from pydantic import BaseModel


class BaseNode(BaseModel):
    @abstractmethod
    def accept(self, visitor, instructions):
        """Accept a visitor - this is the key to the visitor pattern"""
        pass
    
class IRNode(BaseNode):
    pass

class IR_Expression(IRNode):
    pass

class Operand(IR_Expression):
    pass
