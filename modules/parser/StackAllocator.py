from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.Pseudo import Pseudo


class StackAllocator:
    def __init__(self) -> None:
        self.temp_counter = 0
        self.stack_offset = 0
        self.register_map: dict[str, int] = {
        }
        
    def allocate_pseudo(self, name:str, size: int = 4) -> Pseudo:
        self.stack_offset -= size
        self.register_map[name] = self.stack_offset
        return Pseudo(value=name)
    
    def resolve_pseudo(self, pseudo: Pseudo) -> Stack:
        if pseudo.value not in self.register_map:
            raise KeyError("Pseudo not registered to stack")
        return Stack(offset=self.register_map[pseudo.value])