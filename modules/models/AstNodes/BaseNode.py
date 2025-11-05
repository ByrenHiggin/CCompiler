from abc import abstractmethod
from pydantic import BaseModel


class BaseNode(BaseModel):
    @abstractmethod
    def accept(self, visitor, instructions):
        """Accept a visitor - this is the key to the visitor pattern"""
        pass
    
class IRNode(BaseNode):
    def toAsm(self) -> str:
        return ""  # Placeholder implementation
        pass


class IR_Expression(IRNode):
    pass

class Operand(IR_Expression):
    pass
