from modules.models.enums.GenericRegisterEnum import GenericRegisterEnum
from modules.models.nodes.IR.Operands.Register import Register 
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.Pseudo import Pseudo


class StackAllocator:
    def __init__(self) -> None:
        self.temp_counter = 0
        self.stack_offset = 0
        self.register_map: dict[str, int] = {}
        
    def __is_register(self, value: str) -> bool:
        if value[:4] == "reg.":
            return True
        return False

        
    def allocate_pseudo(self, name:str, size: int = 4) -> Pseudo:
        if self.__is_register(name):
            self.register_map[name] = 0
            return Pseudo(value=name)
        else:
            self.stack_offset -= size
            self.register_map[name] = self.stack_offset
            return Pseudo(value=name)
    
    def resolve_pseudo(self, pseudo: Pseudo) -> Stack | Register:
        if pseudo.value not in self.register_map:
            raise KeyError("Pseudo not registered to stack")
        if self.__is_register(pseudo.value):
            reg = pseudo.value[4:]
            regEnum = GenericRegisterEnum.from_reg_label(reg)
            return Register(value=regEnum)
        return Stack(offset=self.register_map[pseudo.value])